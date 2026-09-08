# CLAUDE.MD — Tesis: control LQR y aprendizaje por refuerzo sobre TCLab

**Proyecto:** Control de temperatura en la planta TCLab mediante LQR combinado con aprendizaje por refuerzo *(título provisional)*
**Institución:** Universidad Distrital Francisco José de Caldas
**Programa:** Ingeniería de Sistemas — trabajo de grado (pregrado)
**Campo:** Control automático — control óptimo, aprendizaje por refuerzo, identificación de sistemas
**Idioma del documento:** Español (resumen también en inglés)
**Rama:** main

---

## ESTADO: la pregunta de investigación aún no está definida

La forma concreta de combinar LQR y RL — RL residual sobre el LQR, ajuste automático de $Q$ y $R$,
LQR como filtro de seguridad, o estudio comparativo — es una **salida** de la fase de
descubrimiento, no un supuesto de partida. No la des por decidida.

**Siguiente paso:**

```
/discover interview control de temperatura TCLab con LQR y aprendizaje por refuerzo
```

Esa entrevista produce la especificación de investigación y el registro de decisión que fijan el
método. Hasta entonces, cualquier agente que necesite el método debe preguntar, no suponer.

---

## Principios

- **Planificar primero** — entra en modo plan antes de tareas no triviales; guarda el plan en `quality_reports/plans/`
- **Verificar después** — compila y confirma la salida al terminar cada tarea
- **Fuente única de verdad** — `paper/main.tex` es la tesis; presentaciones y anexos derivan de ella
- **La seguridad del hardware no se negocia** — ver INV-20 a INV-26 en `content-invariants.md`
- **Puertas de calidad** — puntaje agregado ponderado; nada avanza por debajo de 80/100
- **Pares creador-crítico** — todo creador tiene su crítico; los críticos nunca editan archivos

---

## Plataforma

TCLab (Temperature Control Lab): planta didáctica sobre Arduino con dos calentadores y dos
sensores de temperatura. Sistema MIMO 2x2 con acoplamiento térmico, no lineal, con retardo y
constantes de tiempo lentas.

**Modo de trabajo:** entrenamiento y sintonía en simulación (modelo identificado o balance de
energía), validación sobre la placa física. Toda afirmación de desempeño sobre hardware exige
protocolo experimental documentado (INV-8).

---

## Estructura de carpetas

```
tesis-modalidad/
├── CLAUDE.MD
├── .claude/                     # reglas, skills, agentes, hooks
├── Bibliography_base.bib        # bibliografía centralizada
├── config/                      # YAML versionado: Q, R, T_s, setpoints, hiperparámetros
├── paper/                       # la tesis en LaTeX (fuente de verdad)
│   ├── main.tex
│   ├── sections/                # capítulos
│   ├── figures/  tables/        # generados por los scripts
│   ├── talks/  quarto/          # sustentación
│   ├── preambles/               # preámbulo compartido
│   └── supplementary/  replication/
├── data/
│   ├── raw/tclab_runs/          # CSV crudos por corrida — nunca se editan
│   └── cleaned/                 # datasets procesados
├── scripts/
│   ├── python/{hardware,identification,control,rl,analysis,common}/
│   └── matlab/{identification,control}/
├── quality_reports/             # planes, especificaciones, revisiones, puntajes
├── explorations/                # sandbox de pruebas
├── templates/
└── master_supporting_docs/      # papers y documentación de referencia
```

---

## Comandos

```bash
# Entorno Python (fijado en 3.12 — torch y stable-baselines3 aún no soportan 3.14)
source .venv/bin/activate

# Compilar la tesis (latexmk resuelve las pasadas y biber)
cd paper && latexmk main.tex
cd paper && latexmk -c            # limpiar auxiliares

# Ejecutar un script
python scripts/python/identification/step_test.py

# MATLAB sin interfaz gráfica
matlab -batch "run('scripts/matlab/control/disenio_lqr.m')"
```

> `paper/latexmkrc` configura XeLaTeX, TEXINPUTS y BIBINPUTS.

---

## Stack

| Capa | Herramientas |
|------|-------------|
| Hardware / adquisición | `tclab`, `pyserial` |
| Numérico | `numpy`, `scipy`, `pandas` |
| Control | `python-control`, MATLAB (`ss`, `c2d`, `dlqr`), Simulink |
| RL | `gymnasium`, `stable-baselines3`, `torch` |
| Figuras | `matplotlib` (sin títulos internos — INV-12) |
| Documento | LaTeX (XeLaTeX + biber, estilo de cita IEEE) |

Contrato MATLAB<->Python: MATLAB exporta `.mat`/`.csv`, Python los consume con
`scipy.io.loadmat`/`pandas`. Ningún resultado cruza por copiar y pegar.

---

## Umbrales de calidad

| Puntaje | Puerta | Aplica a |
|---------|--------|----------|
| 80 | Commit | Agregado ponderado (bloqueante) |
| 90 | Pull request | Agregado ponderado (bloqueante) |
| 95 | Entrega a jurado | Agregado + todos los componentes >= 80 |
| — | Advisory | Sustentación (se reporta, no bloquea) |

Fórmula de agregación en `.claude/rules/quality.md`.

---

## Referencia de skills

| Comando | Qué hace |
|---------|---------|
| `/discover [modo] [tema]` | Descubrimiento: entrevista, literatura, datos, ideación |
| `/strategize [modo]` | Estrategia de modelado, control y diseño experimental (`theory` para garantías formales) |
| `/analyze [dataset]` | Análisis de datos de extremo a extremo |
| `/write [sección]` | Redacción de capítulos + pase de naturalidad |
| `/review [archivo]` | Revisiones de calidad (enruta según el objetivo) |
| `/revise [informe]` | Ciclo de correcciones: clasifica y enruta observaciones del jurado |
| `/talk [modo]` | Presentación de sustentación (Beamer o Quarto) |
| `/submit [modo]` | Empaquetado, auditoría y puerta final |
| `/tools [subcomando]` | Utilidades: commit, compile, validate-bib, lint |
| `/dashboard` | Regenera `project_dashboard.html` |
| `/checkpoint` | Cierre de sesión: memoria + SESSION_REPORT + bitácora |

---

## Organización de salidas

Output organization: by-script

Figuras en `paper/figures/<nombre_script>/`, tablas en `paper/tables/<nombre_script>/`.

---

## Estado actual

| Componente | Archivo | Estado | Descripción |
|-----------|---------|--------|-------------|
| Pregunta de investigación | `quality_reports/research_spec_*.md` | **pendiente** | Se define con `/discover interview` |
| Tesis | `paper/main.tex` | esqueleto | Portada y estructura de capítulos |
| Identificación | `scripts/python/identification/` | no iniciado | Ensayos de escalón y PRBS sobre TCLab |
| Diseño LQR | `scripts/python/control/` | no iniciado | Pendiente del modelo identificado |
| Agente RL | `scripts/python/rl/` | no iniciado | Pendiente de la formulación del MDP |
| Datos experimentales | `data/raw/tclab_runs/` | vacío | Ninguna corrida registrada aún |
