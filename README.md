# Control LQR y aprendizaje por refuerzo sobre TCLab

Trabajo de grado en Ingeniería de Sistemas, Universidad Distrital Francisco José de Caldas.

El proyecto estudia el control de temperatura de la planta didáctica **TCLab** (Temperature
Control Lab, sobre Arduino: dos calentadores, dos sensores, acoplamiento térmico) combinando un
regulador **LQR** con **aprendizaje por refuerzo**. El trabajo se apoya en dos modos: entrenamiento
y sintonía sobre un modelo identificado de la planta, y validación experimental sobre el hardware
físico.

**La pregunta de investigación está en definición.** La forma concreta de combinar ambos enfoques
—corrección residual sobre el LQR, ajuste automático de las matrices de costo, LQR como filtro de
seguridad, o estudio comparativo— se establece en la fase de descubrimiento.

## Estructura

| Carpeta | Contenido |
|---------|-----------|
| `paper/` | La tesis en LaTeX (`main.tex` es la fuente de verdad) |
| `scripts/python/` | Adquisición, identificación, diseño de control, RL y análisis |
| `scripts/matlab/` | Identificación y diseño LQR en MATLAB/Simulink |
| `config/` | Matrices Q y R, tiempo de muestreo, setpoints, hiperparámetros |
| `data/raw/tclab_runs/` | Corridas experimentales crudas (evidencia, nunca se editan) |
| `quality_reports/` | Planes, especificaciones, revisiones y bitácora de investigación |

## Puesta en marcha

```bash
sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended texlive-latexextra \
               texlive-bibtexextra texlive-fontsrecommended texlive-mathscience \
               texlive-langspanish texlive-binextra biber
python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

El flujo de trabajo asistido está descrito en `CLAUDE.md`. El andamiaje de agentes proviene de la
plantilla [clo-author](https://github.com/hugosantanna/clo-author), adaptada de economía empírica
a control automático.
