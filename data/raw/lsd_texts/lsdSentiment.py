import string

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False  # signals exact match
        self.is_prefix = False  # signals wildcard (prefix) match

class PhraseTrie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, phrase):
        is_prefix = phrase.endswith('*')
        words = phrase[:-1].strip().split() if is_prefix else phrase.strip().split()
        node = self.root
        for word in words:
            if word not in node.children:
                node.children[word] = TrieNode()
            node = node.children[word]
        if is_prefix:
            node.is_prefix = True
        else:
            node.is_end = True
            
    def longest_match(self, tokens, start):
        """
        Returns (match_length, match_type) where match_type is 'exact' or 'prefix'
        If no match, returns (0, None)
        """
        node = self.root
        match_len = 0
        match_type = None
        for i in range(start, len(tokens)):
            word = tokens[i].lower()
            if word in node.children:
                node = node.children[word]
                if node.is_end:
                    match_len = i - start + 1
                    match_type = 'exact'
                if node.is_prefix:
                    match_len = i - start + 1
                    match_type = 'prefix'
            else:
                break
        if match_len > 0:
            return (match_len, match_type)
        else:
            return (0, None)
            
    def get_all_phrases(self):
        """
        Returns a list of (phrase, match_type) tuples, where match_type is 'exact' or 'prefix'.
        """
        phrases = []
        def dfs(node, path):
            if node.is_end:
                phrases.append((' '.join(path), 'exact'))
            if node.is_prefix:
                phrases.append((' '.join(path) + '*', 'prefix'))
            for word, child in node.children.items():
                dfs(child, path + [word])
        dfs(self.root, [])
        return phrases

NEGATE = set([
    "aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
    "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
    "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
    "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
    "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
    "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
    "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
    "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"
])

def load_word_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip().lower() for line in f if line.strip() and not line.startswith('#')]

def has_negation(tokens, idx, window=3):
    start = max(0, idx - window)
    for i in range(start, idx):
        if tokens[i].lower() in NEGATE:
            return True
    return False

class LexicoderSentimentAnalyzer:
    def __init__(self, positive_file, negative_file, neg_positive_file, neg_negative_file):
        # Build tries for each lexicon set
        self.pos_trie = PhraseTrie()
        self.neg_trie = PhraseTrie()
        self.negpos_trie = PhraseTrie()
        self.negneg_trie = PhraseTrie()
        for phrase in load_word_list(positive_file):
            self.pos_trie.insert(phrase)
        for phrase in load_word_list(negative_file):
            self.neg_trie.insert(phrase)
        for phrase in load_word_list(neg_positive_file):
            self.negpos_trie.insert(phrase)
        for phrase in load_word_list(neg_negative_file):
            self.negneg_trie.insert(phrase)
            
    def _tokenize(self, text):
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        return text.translate(translator).split()
        
    def analyze(self, text):
        tokens = self._tokenize(text)
        pos_count = 0
        neg_count = 0
        total_words = 0
        i = 0
        while i < len(tokens):
            # Try negpos and negneg first (highest precedence)
            match_len, match_type = self.negpos_trie.longest_match(tokens, i)
            if match_len:
                neg_count += 1
                i += match_len
                total_words += match_len
                continue
            match_len, match_type = self.negneg_trie.longest_match(tokens, i)
            if match_len:
                pos_count += 1
                i += match_len
                total_words += match_len
                continue
                
            # Try pos/neg with negation window
            match_len, match_type = self.pos_trie.longest_match(tokens, i)
            if match_len:
                if has_negation(tokens, i, window=3):
                    neg_count += 1
                else:
                    pos_count += 1
                i += match_len
                total_words += match_len
                continue
            match_len, match_type = self.neg_trie.longest_match(tokens, i)
            if match_len:
                if has_negation(tokens, i, window=3):
                    pos_count += 1
                else:
                    neg_count += 1
                i += match_len
                total_words += match_len
                continue
                
            # No match, move to next token
            i += 1
            total_words += 1
            
        return {
            "pos_count": pos_count,
            "neg_count": neg_count,
            "total_words": total_words
        }
