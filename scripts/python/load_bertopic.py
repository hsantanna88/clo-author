#!/usr/bin/env python3
"""
load_bertopic.py — Local backup: fit BERTopic c-TF-IDF from cached files.

Loads pre-computed UMAP embeddings and HDBSCAN labels (downloaded from Colab),
runs BERTopic's c-TF-IDF topic extraction, and saves the fitted model to DATA_DIR.
UMAP and HDBSCAN are both short-circuited via cache wrappers — the only real
work is the string groupby + CountVectorizer on ~300–500 topic documents.

Required files in DATA_DIR (download from Colab before session ends):
  umap_{MODEL_NAME}.npy            (~336 MB for minilm)
  hdbscan_labels_{MODEL_NAME}.npy  (~67 MB)
  news_proc/  OR  americanstories_civilwar/   (HuggingFace dataset, ~13 GB)

Run (Windows):
  python scripts/load_bertopic.py

Run (WSL — recommended if you need a large swap file):
  python3 scripts/load_bertopic.py

WSL2 swap on external drive (edit %USERPROFILE%\\.wslconfig, then wsl --shutdown):
  [wsl2]
  swap=512000          # 500 GB in MB
  swapFile=D:\\wsl-swap.vhd

Note: accessing data/ through WSL's /mnt/c/ is slow (Windows filesystem bridge).
If performance matters, copy the data folder to the WSL native filesystem first:
  cp -r /mnt/c/Users/Patrick/Documents/Projects/Dissertation/Civil-War-News/data ~/cw-data
  Then point DATA_DIR at ~/cw-data in the config below.

pip install bertopic datasets sentence-transformers scikit-learn numpy
"""

import gc
import logging
import sys
import time
from pathlib import Path

import numpy as np
from datasets import load_from_disk
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

logging.basicConfig(
    format='%(asctime)s %(levelname)s  %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO,
)
log = logging.getLogger('load_bertopic')

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION — edit to match your Colab run
# ══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).resolve().parent.parent if '__file__' in dir() else Path.cwd()
DATA_DIR     = PROJECT_ROOT / 'data'

# Must match the Colab run exactly.
# minilm | macberth | bert_newspapers | mpnet | e5_large | bge_large | nomic
MODEL_NAME   = 'minilm'
SAMPLE_FRAC  = 1.0    # fraction of corpus used in the Colab run

# BERTopic settings (match Colab run)
N_TOPICS     = None   # None = auto from HDBSCAN
TOP_N_WORDS  = 20

# Truncate articles before c-TF-IDF to cap the ' '.join spike in _extract_topics.
# 512 chars is sufficient for vocabulary extraction; set to 0 to disable.
FIT_MAX_CHARS = 512

# ══════════════════════════════════════════════════════════════════════════════
# DERIVED PATHS
# ══════════════════════════════════════════════════════════════════════════════

_EMBEDDING_MODEL_IDS = {
    'minilm':          'sentence-transformers/all-MiniLM-L6-v2',
    'macberth':        'emanjavacas/MacBERTh',
    'bert_newspapers': 'Livingwithmachines/bert_1760_1900',
    'mpnet':           'sentence-transformers/all-mpnet-base-v2',
    'e5_large':        'intfloat/e5-large-v2',
    'bge_large':       'BAAI/bge-large-en-v1.5',
    'nomic':           'nomic-ai/nomic-embed-text-v1.5',
}
EMBEDDING_MODEL_ID = _EMBEDDING_MODEL_IDS.get(MODEL_NAME, MODEL_NAME)

# Dataset — Notebook 1 saves as 'news_proc'; local copy may have a different name.
_DATASET_CANDIDATES = ['news_proc', 'americanstories_civilwar', 'news_proc_sub']
NEWS_PROC_PATH = next(
    (DATA_DIR / name for name in _DATASET_CANDIDATES if (DATA_DIR / name).exists()),
    None,
)

UMAP_PATH    = DATA_DIR / f'umap_{MODEL_NAME}.npy'
HDBSCAN_PATH = DATA_DIR / f'hdbscan_labels_{MODEL_NAME}.npy'
MODEL_PATH   = DATA_DIR / f'bertopic_model_{MODEL_NAME}'
TOPICS_PATH  = DATA_DIR / f'topics_{MODEL_NAME}.npy'
TOPIC_CSV    = DATA_DIR / f'topic_info_{MODEL_NAME}.csv'

# ══════════════════════════════════════════════════════════════════════════════
# VALIDATE INPUTS
# ══════════════════════════════════════════════════════════════════════════════

def _check_inputs():
    ok = True
    if NEWS_PROC_PATH is None:
        log.error(f'Dataset not found in {DATA_DIR}')
        log.error(f'Expected one of: {_DATASET_CANDIDATES}')
        ok = False
    else:
        log.info(f'Dataset         {NEWS_PROC_PATH}')
    for path, label in [
        (UMAP_PATH,    'UMAP cache    '),
        (HDBSCAN_PATH, 'HDBSCAN labels'),
    ]:
        if not path.exists():
            log.error(f'{label} not found: {path}')
            ok = False
        else:
            log.info(f'{label} {path.name}  ({path.stat().st_size / 1e6:.0f} MB)')
    if not ok:
        log.error('One or more required files are missing — see above.')
        sys.exit(1)

_check_inputs()

# ══════════════════════════════════════════════════════════════════════════════
# CACHE-ONLY UMAP WRAPPER
# ══════════════════════════════════════════════════════════════════════════════

class UMAPWithPCA:
    """Returns pre-loaded cached output; raises immediately if cache is not set."""

    def __init__(self):
        self._is_fitted     = False
        self._cached_output = None

    def fit_transform(self, X, y=None):
        if self._is_fitted and self._cached_output is not None:
            log.info(f'[UMAP] Cache hit — returning {self._cached_output.shape}')
            return self._cached_output
        raise RuntimeError('UMAP cache not loaded.')

    def fit(self, X, y=None):
        self.fit_transform(X, y)
        return self

    def transform(self, X):
        return self.fit_transform(X)

    def get_params(self, deep=True):
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# CACHE-ONLY HDBSCAN WRAPPER
# ══════════════════════════════════════════════════════════════════════════════

class HDBSCANWithCache:
    """Returns pre-loaded cached labels; raises immediately if cache is not set."""

    def __init__(self):
        self._is_fitted     = False
        self._cached_labels = None
        self.labels_        = None
        self.probabilities_ = None

    def fit(self, X, y=None):
        if self._is_fitted and self._cached_labels is not None:
            log.info(f'[HDBSCAN] Cache hit — {len(self._cached_labels):,} docs')
            self.labels_ = self._cached_labels
            return self
        raise RuntimeError('HDBSCAN cache not loaded.')

    def fit_predict(self, X, y=None):
        return self.fit(X, y).labels_

    def __getattr__(self, name):
        # BERTopic probes optional HDBSCAN attributes (condensed_tree_, etc.).
        # Return None for any unknown attribute so BERTopic skips those paths.
        if name.startswith('__'):
            raise AttributeError(name)
        return None


# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATASET
# ══════════════════════════════════════════════════════════════════════════════

log.info(f'Loading dataset from {NEWS_PROC_PATH} ...')
news_proc = load_from_disk(str(NEWS_PROC_PATH))
n_sample  = int(len(news_proc) * SAMPLE_FRAC)
news_sub  = news_proc.shuffle(seed=42).select(range(n_sample))
articles  = news_sub['article']
log.info(f'Corpus: {len(news_proc):,} total → {len(news_sub):,} used ({SAMPLE_FRAC*100:.0f}%)')

# Article length diagnostic — tells you how much RAM the c-TF-IDF join will need.
_s = min(10_000, len(articles))
_lens = sorted(len(a) for a in articles[:_s])
log.info(
    f'Article length (first {_s:,} docs): '
    f'mean={sum(_lens)/_s:.0f}  '
    f'median={_lens[_s // 2]:.0f}  '
    f'p95={_lens[int(_s * 0.95)]:.0f} chars'
)
log.info(
    f'Estimated peak RAM for c-TF-IDF join: '
    f'~{len(articles) * (sum(_lens)/_s) * 2 / 1e9:.1f} GB '
    f'(articles × mean_len × 2 for join copy)'
)

# ══════════════════════════════════════════════════════════════════════════════
# LOAD + INJECT UMAP CACHE
# ══════════════════════════════════════════════════════════════════════════════

log.info(f'Loading UMAP cache from {UMAP_PATH} ...')
umap_embeddings = np.load(str(UMAP_PATH))
log.info(f'  shape={umap_embeddings.shape}')

umap_model                = UMAPWithPCA()
umap_model._cached_output = umap_embeddings
umap_model._is_fitted     = True

# ══════════════════════════════════════════════════════════════════════════════
# LOAD + INJECT HDBSCAN CACHE
# ══════════════════════════════════════════════════════════════════════════════

log.info(f'Loading HDBSCAN cache from {HDBSCAN_PATH} ...')
_labels     = np.load(str(HDBSCAN_PATH))
_n_clusters = len(set(_labels.tolist())) - (1 if -1 in _labels else 0)
_n_noise    = int((_labels == -1).sum())
log.info(f'  {_n_clusters} clusters, {_n_noise:,} noise docs ({_n_noise/len(_labels)*100:.1f}%)')

hdbscan_model                = HDBSCANWithCache()
hdbscan_model._cached_labels = _labels
hdbscan_model._is_fitted     = True
hdbscan_model.labels_        = _labels
del _labels
gc.collect()

# ══════════════════════════════════════════════════════════════════════════════
# TRUNCATE ARTICLES
# ══════════════════════════════════════════════════════════════════════════════

if FIT_MAX_CHARS > 0:
    log.info(f'Truncating {len(articles):,} articles to {FIT_MAX_CHARS} chars ...')
    _trunc   = [a[:FIT_MAX_CHARS] for a in articles]
    del articles
    gc.collect()
    articles = _trunc
    del _trunc
    gc.collect()
    log.info(f'Truncation done — peak RAM for join now ~{len(articles) * FIT_MAX_CHARS * 2 / 1e9:.1f} GB')
else:
    log.info('Truncation disabled (FIT_MAX_CHARS=0).')

_n_docs = len(articles)

# ══════════════════════════════════════════════════════════════════════════════
# VECTORIZER + c-TF-IDF
# ══════════════════════════════════════════════════════════════════════════════

# CountVectorizer runs on N_topics concatenated topic-documents (~300–500 docs),
# not on 8.4M individual articles. min_df=2 means a term must appear in ≥2 topics.
vectorizer_model = CountVectorizer(
    stop_words='english',
    ngram_range=(1, 2),
    min_df=2,
    max_features=50_000,
)
ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)

# ══════════════════════════════════════════════════════════════════════════════
# FIT BERTOPIC
# ══════════════════════════════════════════════════════════════════════════════

bertopic_model = BERTopic(
    embedding_model=EMBEDDING_MODEL_ID,  # string ID — saved as reference, not weights
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    representation_model=None,
    nr_topics=N_TOPICS,
    top_n_words=TOP_N_WORDS,
    low_memory=True,
    calculate_probabilities=False,
    verbose=True,
)

# Dummy embeddings: UMAP and HDBSCAN caches ignore their input, so we never need
# the real 13 GB embeddings array. The only data consumed is the articles list.
_dummy = np.zeros((_n_docs, 1), dtype=np.float16)

log.info(f'Fitting BERTopic on {_n_docs:,} docs (UMAP + HDBSCAN from cache)...')
t0 = time.time()
topics, probs = bertopic_model.fit_transform(articles, embeddings=_dummy)
del _dummy
gc.collect()
elapsed = time.time() - t0

topic_info = bertopic_model.get_topic_info()
n_found    = topic_info.shape[0] - 1
log.info(
    f'Done in {elapsed:.0f}s ({elapsed/60:.1f} min) — '
    f'{n_found} topics, {sum(t == -1 for t in topics):,} noise docs'
)
print(topic_info.head(20).to_string())

# ══════════════════════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════════════════════

log.info(f'Saving model → {MODEL_PATH}')
bertopic_model.save(
    str(MODEL_PATH),
    serialization='safetensors',
    save_ctfidf=True,
    save_embedding_model=False,  # string ID stored in model config; load with embedding_model=...
)

np.save(str(TOPICS_PATH), np.array(topics))
topic_info.to_csv(str(TOPIC_CSV), index=False)

log.info(f'Model      → {MODEL_PATH}')
log.info(f'Topics     → {TOPICS_PATH}')
log.info(f'Topic info → {TOPIC_CSV}')
log.info(
    f'\nTo load the saved model:\n'
    f'  from bertopic import BERTopic\n'
    f'  model = BERTopic.load("{MODEL_PATH}", embedding_model="{EMBEDDING_MODEL_ID}")'
)
