# Paper Organization — House Style (Tables, Figures, Structure)

> **MANDATORY — non-negotiable.** Every agent, and Claude itself, MUST follow this rule whenever a
> paper is drafted, edited, or reviewed. It is enforced as blocking content invariants **INV-23,
> INV-24, INV-25** (`content-invariants.md`): the writer-critic deducts on violations and the verifier
> FAILs on them. This is not advisory style guidance. Do not deviate without explicit user instruction.

The canonical organization for tables, figures, and paper structure. Where this rule and
`working-paper-format.md` disagree on float placement, **this rule wins**.

**Reference exemplars.** Keep one or two well-organized prior papers as the local gold standard and open
them when a case isn't covered here (set the paths in `.claude/state/` if you want them remembered).

---

## 1. Float placement — collect at the END, never inline

Section files (`sections/*.tex`) contain **only prose and `\cref{}` cross-references — no floats.**
All tables and figures live in `main.tex` in two dedicated blocks placed **after** the body
(after `\printbibliography`, or after the last text section), in this order:

```
... \input{sections/...} ...        % all text, no floats
\clearpage
\small \printbibliography
% ============================================================
% TABLES
% ============================================================
\clearpage
\begin{table}[p] ... \end{table}    % each table, separated by \clearpage when large
% ============================================================
% FIGURES
% ============================================================
\clearpage
\begin{figure}[p] ... \end{figure}  % each figure
\begin{appendices} ... \end{appendices}   % appendix floats follow the same conventions
```

- Big exhibits use `[p]` (own page); smaller ones `[htbp]`. Insert `\clearpage` between full-page floats.
- Wide tables/figures use `\begin{landscape} ... \end{landscape}` (pdflscape).
- The reader navigates by `\cref{tab:x}` / `\cref{fig:y}` from the text; LaTeX places the floats at the end.

## 2. Table 1 is always pre-treatment characteristics (treated vs. control)

The first table describes the experimental sample as a **two-group comparison at baseline**:

- **Two value columns only: the treated group and the control group. NO difference column, NO SD column, NO p-value.** (Group means / percentages, one value per cell. This is intentional house style — a difference/test column is *not* used here.)
- Rows grouped into **thematic panels** via `\multicolumn{ncol}{l}{\textit{Panel name}}` + `\midrule`
  (e.g. *Firm dynamics*, *Labor & demographics*, *Sector composition (\%)*, *Education (\%)*).
- **Bottom rows:** unit counts (e.g. `Workers`, `Municipalities`) — the N lives here, not in a column.
- Caption names the baseline window: e.g. `Pre-Treatment Characteristics, 2014`.

Model (bare `tabular` exported by R, wrapped in `main.tex`):

```latex
\begin{tabular}{@{}l cc@{}}
\toprule
 & Treated Group & Control Group \\
\midrule
\multicolumn{3}{l}{\textit{Demographics}} \\
Log hourly wage & 0.807 & 0.835 \\
Age             & 34.1  & 34.4  \\
\midrule
\multicolumn{3}{l}{\textit{Sector composition (\%)}} \\
Manufacturing   & 17.1  & 20.4  \\
\midrule
Workers         & 549,598 & 4,826,901 \\
Municipalities  & 194     & 659       \\
\bottomrule
\end{tabular}
```

## 3. Canonical table wrapper

R/Julia/Python export a **bare `tabular`** (no float, no caption, no notes). `main.tex` wraps it:

```latex
\begin{table}[p]                      % [htbp] for small tables
\small
\centering
\begin{threeparttable}
\captionsetup{font=small, skip=1em}
\caption{Descriptive Title (Cohort/Method)}
\label{tab:xxx}
\input{tables/scriptNN_name/file.tex} % bare tabular
\begin{tablenotes}[flushleft]
\small
\setlength{\leftskip}{0em}
\item \footnotesize\textit{Notes:} <sample> <variable definitions> <specification columns>
  <SE clustering> <significance stars>.
\end{tablenotes}
\end{threeparttable}
\end{table}
```

**Notes are exhaustive** (4–8 sentences): the estimating sample and N, what each variable is, what
each numbered specification adds, the FE structure, the SE clustering level, and the star thresholds.

- **tabularray variant** (hand-written multi-panel with interactions): use
  `\inputtblr{\input{...}}` then `\par\vspace{0.3em}\parbox{\linewidth}{\scriptsize \textit{Notes:} ...}`
  instead of `threeparttable`/`tablenotes`.
- Booktabs rules only (`\toprule/\midrule/\bottomrule`), no `\hline`, no vertical rules.
- Stars `^{*}p<0.10, ^{**}p<0.05, ^{***}p<0.01` (omit stars for AEA targets — see `content-standards.md`).
- "Total effect" rows (sums of base + interaction) report **delta-method SEs in brackets**.

## 4. Canonical figure wrapper (multi-panel)

```latex
\begin{figure}[p]
    \centering \singlespacing
    \caption{Descriptive Title (Method)}\label{fig:xxx}   % caption ABOVE the panels
    \begin{subfigure}[b]{0.48\linewidth}                  % 0.32 for 3-up, 0.48 for 2-up
        \centering
        \caption{Panel Title}                             % short panel label
        \includegraphics[width=\textwidth]{figures/scriptNN_name/panel_a.pdf}
    \end{subfigure}
    \begin{subfigure}[b]{0.48\linewidth}
        \centering
        \caption{Panel Title}
        \includegraphics[width=\textwidth]{figures/scriptNN_name/panel_b.pdf}
    \end{subfigure}
\end{figure}
```

- The overall `\caption{}`+`\label{}` sit at the **top** of the figure; panel sub-captions are short.
- Exported PDFs are **bare** — no titles/subtitles inside the plot (INV-12). Axis labels publication-quality.
- Single-panel: `\includegraphics[width=0.8\textwidth]`. Vector PDF (PNG only for maps/rasters).

## 5. Section order

Standard applied-micro structure (omit/merge as the paper needs):

1. Introduction (Related Literature as a subsection or folded in)
2. Background / Institutional Setting
3. Data (Data Sources, Descriptive Statistics subsections)
4. Identification / Empirical Strategy (Design, Specification, Event Study subsections)
5. Results (Main Results first, then Event Study, Heterogeneity, ...)
6. Mechanism (when present)
7. Robustness
8. Discussion / Policy Implications
9. Conclusion

## 6. Caption and naming conventions

- Captions are **full descriptive titles in title case**, method/cohort in parentheses:
  *"Main Results: Wages and Job Separations (2014 Cohort)"*, *"Event Study: Establishment Dynamics
  (Sun-Abraham)"*, *"Pre-Treatment Characteristics, 2014"*.
- Floats organized **by-script** in subfolders: `tables/scriptNN_name/file.tex`,
  `figures/scriptNN_name/panel.pdf`. R writes the bare exhibit; `main.tex` owns numbering/caption/notes.

## 7. Exhibit numbering convention

- **Table 1:** pre-treatment characteristics (§2).
- **Table 2:** main results.
- Then mechanism → heterogeneity → robustness/welfare.
- **Figures:** context/maps first, then main event studies, then heterogeneity / dose-response / placebo.
