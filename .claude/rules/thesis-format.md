# Formato del documento de grado

Todo documento LaTeX generado o revisado por este sistema se ajusta a este estándar. Aplica a los
agentes writer, writer-critic y verifier.

## Clase de documento y diseño

- `\documentclass[12pt,letterpaper,oneside]{report}` — capítulos, hoja carta (norma colombiana)
- Márgenes: 3 cm izquierdo, 2.5 cm restantes (deja espacio para el empastado)
- Interlineado: `\onehalfspacing` (1.5) en el cuerpo — estándar de trabajos de grado
- Referencias y notas al pie: `\singlespacing`
- Números de página centrados en el pie vía `fancyhdr`
- Idioma: `babel` con `spanish` — activa partición de palabras, "Capítulo", "Cuadro", "Figura",
  "Índice" y comillas latinas

## Preámbulo de referencia

Este preámbulo es el estándar del proyecto. El writer-critic verifica contra él.

```latex
\documentclass[12pt,letterpaper,oneside]{report}

% ====== Idioma (primero: condiciona el resto) ======
\usepackage[spanish,es-tabla,es-noquoting]{babel}
% es-tabla: "Tabla" en lugar de "Cuadro"
\usepackage{csquotes}

% ====== Diseño de página ======
\usepackage[left=3cm,right=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}

% ====== Tipografía (XeLaTeX) ======
\usepackage{fontspec}
\setmainfont{Latin Modern Roman}
\usepackage{microtype}

% ====== Títulos de sección ======
\usepackage{titlesec}
\usepackage[title]{appendix}

% ====== Matemáticas ======
\usepackage{amssymb, amsmath, amsfonts, mathtools}
\usepackage{amsthm}
\theoremstyle{plain}
\newtheorem{teorema}{Teorema}[chapter]
\newtheorem{proposicion}[teorema]{Proposición}
\newtheorem{lema}[teorema]{Lema}
\newtheorem{corolario}[teorema]{Corolario}
\theoremstyle{definition}
\newtheorem{definicion}[teorema]{Definición}
\newtheorem{supuesto}[teorema]{Supuesto}
\DeclareMathOperator*{\argmax}{arg\,max}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator{\tr}{tr}
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}
\newcommand{\transpose}{^{\mathsf{T}}}

% ====== Tablas ======
\usepackage{array, booktabs, makecell}
\usepackage{siunitx}
\sisetup{output-decimal-marker={,}}   % coma decimal en español
\usepackage[flushleft]{threeparttable}
\usepackage{tabularx, rotating}
\usepackage{tabularray}
\UseTblrLibrary{booktabs, siunitx}

% ====== Figuras y leyendas ======
\usepackage{graphicx, subcaption}
\usepackage{float}
\usepackage{caption}
\captionsetup{font=small, labelfont=bf, justification=justified}

% ====== Diagramas de control ======
\usepackage{tikz}
\usetikzlibrary{shapes, arrows.meta, positioning, calc}

% ====== Código fuente ======
\usepackage{listings}
\lstset{basicstyle=\ttfamily\small, breaklines=true, frame=single,
        showstringspaces=false, captionpos=b}

% ====== Listas ======
\usepackage{enumitem}

% ====== Bibliografía: biblatex + biber, estilo IEEE ======
\usepackage{xurl}
\usepackage{xcolor}
\definecolor{citationcolor}{RGB}{0, 90, 160}
\usepackage[backend=biber,
            style=ieee,
            sorting=none,
            maxbibnames=99]{biblatex}
\addbibresource{Bibliography_base.bib}

% ====== Notas al pie ======
\interfootnotelinepenalty=10000

% ====== hyperref (penúltimo) ======
\usepackage[breaklinks, colorlinks=true,
            linkcolor=citationcolor, citecolor=citationcolor,
            urlcolor=citationcolor]{hyperref}

% ====== cleveref (después de hyperref) ======
\usepackage[spanish,nameinlink]{cleveref}
```

## Decisiones clave

Los elementos **obligatorios** son bloqueantes: el writer-critic deduce puntos. Los
**recomendados** mejoran la calidad pero no bloquean.

| Decisión | Estándar | Justificación |
|----------|----------|---------------|
| `report` con capítulos | Obligatorio | Un trabajo de grado se organiza por capítulos, no por secciones |
| `babel` español | Obligatorio | Partición de palabras y nomenclatura en español |
| `es-tabla` | Obligatorio | Sin él, babel rotula "Cuadro" en vez de "Tabla" |
| `\onehalfspacing` | Obligatorio | Interlineado estándar de trabajos de grado |
| `biblatex` + `biber`, `style=ieee` | Obligatorio | Citación numérica, convención de ingeniería |
| `booktabs` + `threeparttable` | Obligatorio | Tablas con notas, sin líneas verticales (INV-3) |
| `hyperref` penúltimo, `cleveref` después | Obligatorio | Evita conflictos de paquetes (INV-10) |
| `microtype` | Obligatorio | Espaciado y kerning correctos |
| `siunitx` con coma decimal | Obligatorio | El separador decimal en español es la coma |
| `fontspec` (XeLaTeX) | Obligatorio | El proyecto compila con XeLaTeX (ver `latexmkrc`) |
| `listings` | Recomendado | Solo si se incluye código en anexos |
| `tikz` | Recomendado | Diagramas de bloques del lazo de control |

## Portada

La portada sigue el formato de trabajos de grado de la Universidad Distrital: título, autor(es)
con código estudiantil, tipo de documento ("Trabajo de grado para optar al título de Ingeniero de
Sistemas"), director, facultad, programa, ciudad y año.

Reglas:
- Sin numeración en la portada: `\thispagestyle{empty}`
- Páginas preliminares (dedicatoria, agradecimientos, resumen, índices) en romanos minúsculos
- El contador se reinicia en 1 arábigo al comenzar el primer capítulo
- Verificar el formato exacto contra el reglamento vigente del programa antes de la entrega final

## Resumen y metadatos

```latex
\chapter*{Resumen}
\addcontentsline{toc}{chapter}{Resumen}
Texto del resumen.

\vspace{1em}
\noindent\textbf{Palabras clave:} control óptimo, LQR, aprendizaje por refuerzo, TCLab

\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
Abstract text.

\vspace{1em}
\noindent\textbf{Keywords:} optimal control, LQR, reinforcement learning, TCLab
```

Resumen en español y *abstract* en inglés, ambos con palabras clave (INV-6).

## Estructura de capítulos

Orden habitual en un trabajo de grado de ingeniería:

1. Introducción — problema, justificación, objetivos general y específicos, alcance
2. Marco teórico — control óptimo, LQR, aprendizaje por refuerzo, lo necesario y nada más
3. Estado del arte — trabajos relacionados y posicionamiento
4. Metodología — plataforma, identificación, diseño del controlador, protocolo experimental
5. Implementación — arquitectura de software, bucle de control, adquisición
6. Resultados — identificación, desempeño en simulación, desempeño en hardware, comparación
7. Discusión — interpretación, limitaciones, brecha sim-to-real
8. Conclusiones y trabajo futuro
9. Referencias
10. Anexos — código, datos, planos, deducciones extensas

Cada capítulo usa `\chapter{}` con `\label{cap:nombre}`. Las secciones usan `\section{}` con
`\label{sec:nombre}`.

**Los objetivos específicos son un contrato.** El jurado los verifica uno a uno. El capítulo de
conclusiones debe cerrar explícitamente cada objetivo declarado.

## Tablas y figuras

- Colocadas cerca de su primera mención
- **Tablas escritas a mano:** preferir `tblr` / `talltblr` (tabularray)
- **Tablas generadas por script:** exportar `tabular` desnudo (reglas booktabs) y envolverlo en
  `threeparttable` desde el documento (INV-13)
- Reglas `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), nunca `\hline` (INV-3)
- Los ejes de toda figura llevan **magnitud y unidad**: "Temperatura (°C)", "Tiempo (s)",
  "Potencia del calentador (%)"
- Sin títulos dentro de la figura: el título va en `\caption{}` (INV-12)
- Las figuras de series temporales de control muestran la referencia (setpoint), la salida y la
  señal de control, esta última típicamente en un panel inferior compartiendo el eje de tiempo

## Bibliografía

```latex
\cleardoublepage
\printbibliography[heading=bibintoc, title={Referencias}]
```

Citación numérica IEEE: `\cite{clave}` produce [1]. Con `sorting=none` las entradas se numeran por
orden de aparición, como es habitual en ingeniería.

## Compilación

```bash
cd paper && latexmk main.tex     # resuelve pasadas y biber automáticamente
cd paper && latexmk -c           # limpiar auxiliares

# Alternativa manual:
xelatex main.tex && biber main && xelatex main.tex && xelatex main.tex
```

## Qué verifica el writer-critic

**Obligatorio (deducciones bloqueantes):**
- Clase o tamaño de fuente incorrectos (-5)
- Falta `babel` español o falta `es-tabla` (-5)
- Falta `\onehalfspacing` en el cuerpo (-5)
- Uso de `natbib`/`bibtex` en vez de `biblatex`/`biber` (-3)
- Estilo de cita distinto de IEEE sin justificación (-3)
- Falta configuración de numeración con `fancyhdr` (-2)
- Falta resumen en español o abstract en inglés (-5)
- Faltan palabras clave (-5)
- `\hline` en vez de reglas booktabs (-3)
- Tabla sin notas (-5 por tabla)
- Figura sin notas o con ejes sin unidades (-5 por figura)
- `hyperref` no cargado penúltimo (-2)
- Falta `cleveref` después de `hyperref` (-2)
- `Figura~\ref{}` manual en vez de `\cref{}` (-1 cada una, máximo -5)
- Falta `microtype` (-2)
- Punto decimal en vez de coma en cifras del texto en español (-2)
- Un objetivo específico declarado sin cierre en conclusiones (-10 por objetivo)

**Recomendado (se reporta, no se deduce):**
- Falta `listings` cuando hay código en anexos
- Diagrama de bloques del lazo ausente en la metodología
- Color de citación distinto del estándar del proyecto
