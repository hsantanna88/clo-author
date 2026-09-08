---
paths:
  - "**/*.R"
  - "**/*.py"
  - "**/*.jl"
  - "**/*.do"
  - "**/*.tex"
  - "paper/tables/**"
  - "paper/figures/**"
  - "master_supporting_docs/**"
  - "explorations/**"
---

# Content Standards: Tables, Figures, PDFs, and Explorations

---

## 1. Table Standards

**Target:** Publication-quality tables using standard economics formatting (booktabs rules, no vertical rules). Two approaches are supported:

- **tabularray (`tblr` / `talltblr`)** — modern key-value interface. Preferred for hand-written tables in `main.tex`.
- **`tabular` + `booktabs` + `threeparttable`** — traditional stack. Required for R/Python/Julia-generated output (scripts export bare `tabular`).

Note format follows the evaluation profile in journal-profiles.md. Performance metrics never use significance stars (INV-4).

### No In-Table Titles or Notes

- **Never** embed titles inside the table body or as a table header row
- **Never** embed notes, sources, or footnotes inside the table itself
- Table numbering, titles, and notes are added in LaTeX via `\caption{}` and `\begin{tablenotes}` (or tabularray's `note{}` key)
- The file name and folder identify what the table contains

### Three-Line Format (Booktabs)

Every table uses exactly three horizontal rules and **zero vertical lines**:

**Traditional (R/Python/Julia output):**
```latex
\begin{table}[htbp]
\centering
\begin{threeparttable}
\caption{Effect of X on Y}\label{tab:main}
\begin{tabular}{lcccc}
\toprule
            & (1)     & (2)     & (3)     & (4)     \\
\midrule
...coefficients...
\bottomrule
\end{tabular}
\begin{tablenotes}\small
\item \textit{Notes:} Standard errors in parentheses.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

**Modern (hand-written in main.tex):**
```latex
\begin{talltblr}[
  caption = {Effect of X on Y},
  label = {tab:main},
  note{*} = {Standard errors in parentheses.},
]{colspec = {lcccc}, rowsep = 4pt}
\toprule
            & (1)     & (2)     & (3)     & (4)     \\
\midrule
...coefficients...
\bottomrule
\end{talltblr}
```

- `\toprule` above column headers
- `\midrule` below column headers (and to separate panels)
- `\bottomrule` at the very end
- `\cmidrule(lr){2-4}` for partial rules spanning column groups
- **R/Python/Julia output:** wrap with `threeparttable` for notes via `\begin{tablenotes}`
- **Hand-written tables:** prefer `talltblr` with `note{}` keys — unifies caption, label, and notes
- **Never** use `\hline`, `|`, or any vertical rules

### Presentación de métricas

- Una fila por métrica, una columna por controlador o configuración
- Media y dispersión en la misma celda (`12,4 ± 0,8`) o la dispersión en la fila inferior entre
  paréntesis. Declarar cuál se usa en la nota de la tabla
- **Unidades en el encabezado de fila**, no repetidas en cada celda: `IAE (°C·s)`
- Coma decimal (documento en español); usar `siunitx` con `output-decimal-marker={,}`
- La nota indica el número de corridas N y las condiciones experimentales (INV-1, INV-4)

**Sin estrellas de significancia.** Esta no es una disciplina de contraste de hipótesis sobre
datos observacionales: se reportan métricas medidas con su dispersión. Una diferencia se declara
relevante solo si supera la dispersión entre corridas de la misma configuración.

Ejemplo de nota:
```
\textit{Notas:} Media ± desviación estándar sobre N = 5 corridas por configuración.
Todas las corridas comparten perfil de setpoints, Ts = 1 s y temperatura ambiente
inicial en el rango 22–24 °C. Fuente: scripts/python/analysis/metricas.py.
```

Working paper default example:
```
Treatment        & 0.045**  & 0.038*   & 0.052*** \\
                 & (0.021)  & (0.020)  & (0.019)  \\
```

AEA journal example:
```
Treatment        & 0.045    & 0.038    & 0.052    \\
                 & (0.021)  & (0.020)  & (0.019)  \\
```

### Column and Row Structure

- **Column (1), (2), ...** headers in the first row after `\toprule`
- **Dependent variable** stated in a spanning header or the first subheader row
- **Variable names** left-aligned, human-readable (not raw R variable names)
  - `Log wages` not `ln_wage_deflated`
  - `Female` not `sex_2`
  - `Years of education` not `educ_yrs`
- **Numeric columns** right-aligned or decimal-aligned
- **N**, **R²**, **Fixed effects** (Yes/No), **Controls** (Yes/No) at the bottom before `\bottomrule`

### Panel Structure

For tables with multiple panels:

```latex
\multicolumn{5}{l}{\textit{Panel A: Full sample}} \\
\midrule
...
\\[0.5em]
\multicolumn{5}{l}{\textit{Panel B: Male workers}} \\
\midrule
...
```

- Panel labels in italics, left-aligned, spanning all columns
- `\midrule` after each panel label
- Small vertical space (`\\[0.5em]`) between panels

### Generación de tablas desde Python

Las tablas se exportan como `tabular` desnudo (INV-13). El documento las envuelve en
`threeparttable` y añade `\caption{}` y notas.

```python
def exportar_tabular(df: pd.DataFrame, ruta: Path, columnas: str) -> None:
    """Exporta un DataFrame como tabular desnudo con reglas booktabs."""
    cuerpo = df.to_latex(
        index=False,
        escape=False,
        column_format=columnas,
        float_format=lambda x: f"{x:.2f}".replace(".", ","),  # coma decimal
    )
    # to_latex ya emite toprule/midrule/bottomrule con booktabs habilitado;
    # verificar que no incluya \begin{table} ni \caption
    ruta.write_text(cuerpo)
```

Reglas al exportar:

- Nunca `\begin{table}`, `\caption{}` ni notas dentro del archivo generado (INV-13)
- Reglas `booktabs`, nunca `\hline` ni líneas verticales (INV-3)
- Coma decimal en el formato numérico
- Las unidades van en el encabezado de fila o columna, no repetidas por celda
- El nombre del archivo y su carpeta identifican qué contiene la tabla

Para tablas escritas a mano en el documento, preferir `talltblr` (tabularray), que unifica
leyenda, etiqueta y notas en una sola interfaz.

- Write to `paper/tables/`

### File Naming

```
tables/
├── identificacion/
│   ├── modelo_ss_parametros.tex
│   └── modelo_ajuste_validacion.tex
├── evaluacion/
│   ├── metricas_lqr.tex
│   ├── metricas_rl.tex
│   └── comparacion_controladores.tex
└── configuracion/
    └── hiperparam_agente.tex
```

Pattern: `{table_type}_{content_description}.tex`

- `resumen_` for descriptive summaries of a run
- `modelo_` for identified model parameters and fit criteria
- `metricas_` for controller performance metrics
- `comparacion_` for controller-vs-controller tables
- `hiperparam_` for RL hyperparameter tables

### Prohibited Patterns

| Pattern | Reason |
|---------|--------|
| Title row inside the table | Titles go in `\caption{}`, not the table body |
| Notes embedded in table body | Notes go below via `\begin{tablenotes}` |
| `\hline` | Use `\toprule` / `\midrule` / `\bottomrule` (booktabs) |
| Vertical rules (`\|` in column spec) | Never used in publication-quality tables |
| Raw variable names in labels | Human-readable labels required |
| Metric without units | A number without units is unreadable (INV-4) |
| Point decimal in a Spanish document | Use comma via `siunitx` |
| `\begin{table}` in generated output | Scripts export bare `tabular`; the float wrapper lives in `main.tex` (INV-13) |

### Table Type Templates

Use these as defaults. Adapt columns based on the paper's needs (e.g., add Min/Max, percentiles, or subgroup columns when substantively important).

**Descriptive Statistics:**
```
\toprule
                        &  Mean   &  SD     \\
\midrule
\multicolumn{3}{l}{\textit{Continuous variables}} \\
\quad Wages (USD)       &  45,230 &  12,400 \\
\quad Years of education&  13.2   &  2.8    \\
\quad Age               &  38.5   &  11.2   \\
\\[0.5em]
\multicolumn{3}{l}{\textit{Categorical variables (\%)}} \\
\quad Female            &  48.2   &         \\
\quad College degree    &  32.5   &         \\
\bottomrule
```
- Default: Mean and SD in separate columns (never stacked with parentheses — that's for regression SEs)
- Categorical/binary: percentage in Mean column, SD blank
- Sample size stated once in table notes, not as a column
- Add Min/Max only when the range is substantively important (RDD bandwidth, data coverage)

**Regression Results:**
```
\toprule
                        &  (1)    &  (2)    &  (3)    &  (4)    \\
                        &  OLS    &  OLS    &  IV     &  IV     \\
\midrule
Treatment               &  0.045**&  0.038* &  0.052**&  0.041* \\
                        & (0.021) & (0.020) & (0.025) & (0.022) \\
\midrule
Controls                &  No     &  Yes    &  No     &  Yes    \\
Fixed Effects           &  No     &  Yes    &  No     &  Yes    \\
Observations            &  10,000 &  10,000 &  10,000 &  10,000 \\
R$^2$                   &  0.05   &  0.12   &         &         \\
\bottomrule
```
- Coefficients on one row, standard errors in parentheses below
- Stars: `*` p < 0.10, `**` p < 0.05, `***` p < 0.01
- Bottom rows: Controls (Yes/No), Fixed Effects (Yes/No), Observations, R²

**Multi-Outcome (Panel Structure):**
```
\toprule
                        &  (1)    &  (2)    &  (3)    &  (4)    \\
\midrule
\multicolumn{5}{l}{\textit{Panel A: Wages}} \\
\midrule
Treatment               &  0.045**&  0.038* &  0.052**&  0.041* \\
                        & (0.021) & (0.020) & (0.025) & (0.022) \\
\\[0.5em]
\multicolumn{5}{l}{\textit{Panel B: Employment}} \\
\midrule
Treatment               &  0.021  &  0.033* &  0.015  &  0.028  \\
                        & (0.018) & (0.017) & (0.020) & (0.019) \\
\midrule
Controls                &  No     &  Yes    &  No     &  Yes    \\
Fixed Effects           &  No     &  Yes    &  No     &  Yes    \\
Observations            &  10,000 &  10,000 &  10,000 &  10,000 \\
\bottomrule
```
- Each outcome gets its own panel with same column structure
- Panel labels in italics, left-aligned, spanning all columns
- Controls/FE/Observations rows appear once at the bottom (shared across panels)

**Balance Table:**
```
\toprule
Variable                &  Treatment &  Control &  Difference &  SE     &  p-value \\
\midrule
Wages (USD)             &  45,800    &  44,650  &  1,150      &  (890)  &  0.197   \\
Years of education      &  13.4      &  13.1    &  0.3        &  (0.2)  &  0.134   \\
Female (\%)             &  47.8      &  48.6    &  -0.8       &  (1.2)  &  0.505   \\
\bottomrule
```

**Robustness:**
```
\toprule
                        &  (1)        &  (2)           &  (3)          &  (4)            \\
                        &  Baseline   &  Alt. controls &  Alt. sample  &  Alt. estimator \\
\midrule
```
- Column headers describe what changes across specifications
- Same outcome variable across all columns

---

## 2. Figure Standards

- **Never add titles or subtitles inside ggplot** — use `labs(title = NULL, subtitle = NULL)`
- **Figure information goes in two places:**
  1. **File name** — descriptive, e.g., `fig1_hispanic_enrollment_ascm.pdf`
  2. **LaTeX `\caption{}`** — the authoritative title, numbered and editable without re-running R
- **Panel labels are the exception** — "Panel A: Employment" inside multi-panel figures (via `patchwork`, `cowplot`, etc.) is fine since they identify sub-panels, not the whole figure
- **Axis labels must be publication-quality** — "Employment Rate" not "emp_rate". Clean labels stay in the figure; titles and context go in the caption
- **Use serif fonts** — figures should match the paper's body text. In ggplot, set `theme(text = element_text(family = "serif"))` or use `theme_minimal(base_family = "serif")`
- **Show all years on the x-axis** when the panel spans ~20 years or fewer — use `scale_x_continuous(breaks = min_year:max_year)`. Only thin out labels when they overlap (roughly >20 ticks)
- **Output PDF for figures** — vector graphics for LaTeX. Use `ggsave("fig.pdf")`. PNG only for raster content (maps, photos).
- **Colorblind-friendly palettes** — use `scale_color_brewer(palette = "Set2")`, `viridis`, or similar. Never rely on red/green contrast alone.
- **Color-independent design** — figures must be readable in grayscale. Combine color with shape (`shape` aesthetic) and linetype (`linetype` aesthetic) so series remain distinguishable without color.
- **Figure width** — single-panel: `width=0.8\textwidth`. Side-by-side panels: `width=0.48\textwidth` each.

---

## 3. PDF Processing

### The Safe Processing Workflow

**Step 1: Receive PDF Upload**
- User uploads PDF to `master_supporting_docs/supporting_papers/` or `supporting_slides/`
- Claude DOES NOT attempt to read it directly

**Step 2: Check PDF Properties**
```bash
pdfinfo paper_name.pdf | grep "Pages:"
ls -lh paper_name.pdf
```

**Step 3: Create Subfolder and Split**
```bash
mkdir -p paper_name/

for i in {0..9}; do
  start=$((i*5 + 1))
  end=$(((i+1)*5))
  gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dSAFER \
     -dFirstPage=$start -dLastPage=$end \
     -sOutputFile="paper_name/paper_name_p$(printf '%03d' $start)-$(printf '%03d' $end).pdf" \
     paper_name.pdf 2>/dev/null
done
```

**Step 4: Process Chunks Intelligently**
- Read chunks ONE AT A TIME using the Read tool
- Extract key information from each chunk
- Build understanding progressively
- Don't try to hold all chunks in working memory

**Step 5: Selective Deep Reading**
- After scanning all chunks, identify the most relevant sections
- Only read those sections in detail for slide development
- Skip appendices, references, or less relevant sections unless needed

### Error Handling Protocol

**If a chunk fails to process:**
1. Note the problematic chunk (e.g., "Chunk p021-025 failed")
2. Try splitting into 1-2 page pieces
3. If still failing, skip and document the gap

**If splitting fails:**
1. Check if Ghostscript is installed: `gs --version`
2. Try alternative: `pdftk paper.pdf burst output paper_%03d.pdf`
3. If all else fails, ask user to upload specific page ranges manually

**If memory/token issues persist:**
1. Process only 2-3 chunks per session
2. Focus on specific sections user identifies as most important

---

## 4. Exploration Folder Protocol

**All experimental work goes into `explorations/` first.** Never directly into production folders.

### Folder Structure

```
explorations/
├── ACTIVE_PROJECTS.md
├── [project]/
│   ├── README.md          # Goal, status, findings
│   ├── R/                 # Code (use _v1, _v2 for iterations)
│   ├── scripts/           # Test scripts
│   ├── output/            # Results
│   └── SESSION_LOG.md     # Progress notes
└── ARCHIVE/
    ├── completed_[project]/
    └── abandoned_[project]/
```

### Lifecycle

1. **Create** — `mkdir -p explorations/[name]/{R,scripts,output}` + README from `templates/exploration-readme.md`
2. **Develop** — work entirely within the exploration folder
3. **Decide:**

   - **Graduate to production** — copy to `R/`, `scripts/`; requires quality >= 80, tests pass, code clear. Move to `ARCHIVE/completed_[project]/`
   - **Keep exploring** — document next steps in README
   - **Abandon** — move to `ARCHIVE/abandoned_[project]/` with explanation (use `templates/archive-readme.md`)

### Graduate Checklist

- [ ] Quality score >= 80
- [ ] All tests pass
- [ ] Results replicate within tolerance
- [ ] Code is clear without deep context
- [ ] README explains approach and findings

---

## 5. Exploration Fast-Track

**Lightweight workflow for experimental work.** Quality threshold: 60/100 (vs 80 for production). No planning needed.

### Steps

1. **Research value check** — Does this improve the project? If NO, don't build it.
2. **Create folder** — `mkdir -p explorations/[name]/{R,scripts,output}` + README + SESSION_LOG.md
3. **Code immediately** — no plan needed. Must-haves: code runs, results correct, goal documented. Not needed: Roxygen docs, full tests, perfect style.
4. **Log progress** — append 2-3 lines to SESSION_LOG.md as you work
5. **Decision point** — keep exploring, graduate to production (upgrade to 80/100), or archive with brief explanation

### When to Stop (Kill Switch)

At any point: stop, archive with note ("Attempted X, hit blocker Y"), move on. No guilt — exploration is inherently uncertain.
