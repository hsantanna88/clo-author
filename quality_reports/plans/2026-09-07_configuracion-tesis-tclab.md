# Configuración del repositorio para la tesis: LQR + RL sobre TCLab

## Contexto

Este repositorio es un fork de **clo-author**, una plantilla de Claude Code calibrada para
**investigación empírica en economía**: 21 agentes que hablan de inferencia causal (DiD,
variables instrumentales, parallel trends), perfiles de referees de AER/QJE, R como lenguaje
principal, códigos JEL y estrellas de significancia como invariantes obligatorios.

El proyecto real es otro: una **tesis de pregrado en Ingeniería de Sistemas** (Universidad
Distrital Francisco José de Caldas) sobre **control LQR combinado con aprendizaje por refuerzo
en la planta TCLab**, con hardware físico y simulación, escrita en español, con código en
Python y MATLAB/Simulink.

La plantilla contempla esta adaptación —`.claude/references/domain-profile.md` es el punto de
extensión diseñado para ello— pero nadie la ha ejecutado todavía: todos los archivos siguen con
placeholders `[BRACKETED]` o con contenido de economía.

**Un punto importante:** la pregunta de investigación aún no existe, y eso es correcto. La
combinación concreta de LQR y RL (RL residual, auto-tuning de Q/R, LQR como filtro de seguridad,
o comparación) es una *salida* de la fase de descubrimiento, no una entrada de la configuración.
Este plan deja ese espacio de diseño abierto y deliberadamente no lo cierra.

**Resultado esperado:** un repositorio donde `/discover interview` pueda arrancar de inmediato y
donde cada agente que se despache hable de control automático, no de econometría.

---

## Hallazgo previo: la cadena de herramientas no está instalada

Verificado en esta máquina (CachyOS/Arch):

| Herramienta | Estado |
|---|---|
| `python3` | 3.14.7 — presente |
| `numpy`, `matplotlib` | presentes |
| `scipy`, `pandas`, `control`, `tclab`, `gymnasium`, `stable-baselines3`, `torch` | **ausentes** |
| `latexmk`, `xelatex`, `biber` | **ausentes** |
| `matlab`, `octave` | **ausentes** |

Dos consecuencias que condicionan el plan:

1. El principio "verificar después — compilar y confirmar" de `CLAUDE.md` **no puede cumplirse**
   hasta instalar TeX Live. Lo dejo como paso 1 con el comando exacto.
2. **Python 3.14 es demasiado nuevo** para `torch` y `stable-baselines3` (aún sin ruedas
   precompiladas). El entorno del proyecto debe fijarse en **Python 3.11 o 3.12** dentro de un
   `venv` propio, no en el intérprete del sistema.

---

## Decisiones ya tomadas

| Decisión | Elección |
|---|---|
| Producto | Tesis de grado (pregrado) |
| Institución | Universidad Distrital Francisco José de Caldas — Ing. de Sistemas |
| Plataforma | TCLab físico + simulación (entrenar en modelo, validar en placa) |
| Idioma / stack | Español; Python + MATLAB/Simulink |
| Método LQR+RL | **Abierto** — se define en `/discover interview` |
| Artefactos de la plantilla | Archivar en `.template-reference/` (ignorada por git) |
| Profundidad | Puntos de extensión + recalibrar los 6 agentes críticos |

---

## Fase 1 — Prerrequisitos de entorno (los ejecuta el usuario)

No los corro yo: requieren `sudo` y descargan varios GB.

```bash
# TeX Live (compilación de la tesis)
sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended \
               texlive-latexextra texlive-bibtexextra texlive-fontsrecommended \
               texlive-mathscience texlive-langspanish texlive-binextra biber

# Entorno Python fijado en 3.12 (torch/SB3 no soportan 3.14)
sudo pacman -S python312
python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

MATLAB no está instalado. Preparo igualmente los estándares y el **contrato de interoperación**
(MATLAB exporta `.mat`/`.csv`, Python los consume con `scipy.io.loadmat`/`pandas`), de modo que
sirva tanto si instalas MATLAB aquí como si trabajas en el laboratorio de la universidad.

---

## Fase 2 — Archivar los artefactos de la plantilla

Mover a `.template-reference/` (nueva entrada en `.gitignore`), sin borrar nada:

`guide/`, `docs/`, `.github/workflows/`, `CHANGELOG.md`, `README.md` (el de clo-author),
`quality_reports/demo/`, `quality_reports/mas-evolution-v2-changelog.md`,
`quality_reports/session_logs/*` y `quality_reports/plans/*` (todos son del desarrollo de la
plantilla, ninguno de tu tesis), `scripts/generate_dashboard.py`, `scripts/generate_html_report.py`
y `templates/html/` **se quedan** — el dashboard sí lo vas a usar.

Después, `README.md` nuevo describiendo la tesis en tres párrafos.

---

## Fase 3 — Identidad del proyecto

| Archivo | Cambio |
|---|---|
| `CLAUDE.md` | Reescritura completa. Título provisional, institución, programa, campo (control automático + RL), idioma, stack, comandos reales (`latexmk`, `python`, `matlab -batch`), estructura de carpetas nueva, tabla de estado inicial. **Bloque destacado: "Pregunta de investigación: POR DEFINIR → `/discover interview`"**. Bajo 150 líneas. |
| `MEMORY.md` | Reset. Las ~25 entradas `[LEARN]` actuales son del desarrollo de la plantilla (guías Quarto, gobernanza constitucional, dogfooding) — cero relevancia. Siembro 4-5 entradas del proyecto real: stack fijado, restricción de Python 3.12, contrato MATLAB↔Python, seguridad de hardware. |
| `SESSION_REPORT.md` | Reset con encabezado del proyecto nuevo. |
| `.claude/settings.json` | Quitar `additionalDirectories` que apuntan a `/Users/hsantanna/repos/clo-author/...` — rutas de macOS de otra persona, inexistentes aquí. Purgar permisos one-off (`find ~/Desktop -iname *ABDC*`, el `echo` de meta-governance, el `mv` de journal-profiles). Añadir permisos de Python/venv/pytest/MATLAB. |
| `.gitignore` | Añadir `.template-reference/`, `.venv/`, `runs/`, `wandb/`, `*.slxc`, `slprj/`, checkpoints de modelos (`*.zip`, `*.pth`), y política sobre `data/raw/` (los CSV crudos **sí** se versionan: son pequeños y son la evidencia experimental de la tesis). |

---

## Fase 4 — Calibración de dominio (el núcleo del trabajo)

### `.claude/references/domain-profile.md` — reescritura completa

Todos los agentes leen este archivo para calibrarse. Mapeo de secciones:

| Sección de la plantilla | Se convierte en |
|---|---|
| Campo / subcampos | Control automático; adyacentes: control óptimo, RL, identificación de sistemas, control de procesos |
| Revistas objetivo | Criterios de jurado de tesis (UD) + venues para el paper derivado |
| Fuentes de datos comunes | Protocolos de excitación: escalón, PRBS, multi-seno; corridas propias del TCLab; modelo de balance de energía de Hedengren |
| Estrategias de identificación | Identificación de sistemas: FOPDT, ARX/ARMAX, subespacios (N4SID), balance de energía de primeros principios |
| Convenciones de campo | Tiempo de muestreo declarado siempre; saturación del actuador 0–100 %; anti-windup; límite térmico de seguridad; reporte de media ± desviación sobre N repeticiones |
| Convenciones de notación | $x$ estado, $u$ entrada, $y$ salida, $(A,B,C,D)$, $Q,R$ pesos, $K$ ganancia, $P$ solución de Riccati, $J$ costo, $T_s$ muestreo, $\pi_\theta$ política |
| Referencias seminales | Kalman (1960); Åström & Murray; Anderson & Moore; Sutton & Barto (2018); Bradtke (LQR vía Q-learning); Fazel et al. (2018); Dean et al. (2020); Recht (2019); DDPG/SAC/PPO; Johannink et al. (RL residual); Berkenkamp et al. (RL seguro con garantías de estabilidad); literatura de TCLab de Hedengren |
| Preocupaciones del evaluador | Brecha sim-to-real; sobreajuste al simulador; garantías de estabilidad del componente aprendido; recompensa mal especificada; repeticiones insuficientes; comparación injusta contra el LQR base; observabilidad y controlabilidad |
| Umbrales de tolerancia | IAE/ISE/ITAE, sobreimpulso, tiempo de establecimiento, error en estado estacionario, esfuerzo de control — con tolerancias numéricas explícitas |

**Restricción de honestidad:** las referencias seminales se escriben solo con los datos que
pueda verificar. Nada de citas inventadas — cualquier entrada dudosa se marca `% VERIFICAR` en
el `.bib` y se confirma con `/tools validate-bib` antes de usarse.

### `.claude/references/journal-profiles.md` — reemplazo

Perfil **por defecto**: "Jurado de tesis — Universidad Distrital, Ing. de Sistemas (pregrado)",
calibrado al nivel real de exigencia de un trabajo de grado (no un referee de Automatica).
Más perfiles de venues de control para el eventual artículo derivado: IEEE TCST, Control
Engineering Practice, ISA Transactions, Journal of Process Control, IFAC-PapersOnLine, IEEE
Access. Los perfiles de economía/finanzas/marketing (40 KB) se van a `.template-reference/`.

### `.claude/rules/content-invariants.md` — reescritura de los invariantes de economía

| Invariante | Acción |
|---|---|
| INV-1,2,3,7,9–13,15–19 | Se conservan (tablas booktabs, notas de figuras, biblatex, rutas relativas, sin `setwd()`) |
| INV-4 estrellas de significancia | → **métricas de desempeño con unidades**: IAE, ISE, ITAE, sobreimpulso (%), tiempo de establecimiento (s), esfuerzo de control; media ± desviación sobre N repeticiones |
| INV-6 códigos JEL | → **palabras clave + resumen en español e inglés** (requisito de tesis) |
| INV-8 afirmaciones causales | → **toda afirmación de desempeño exige protocolo experimental documentado**: setpoints, $T_s$, condiciones iniciales, temperatura ambiente, número de repeticiones |
| INV-14 semilla | Reforzado para RL: semilla fija por corrida y **mínimo N semillas reportadas**, no una sola |

Invariantes nuevos, específicos de control con hardware:

- **INV-23** Toda sesión con hardware usa gestor de contexto y **apaga los calentadores en `finally`**, incluso ante excepción.
- **INV-24** Límites de seguridad explícitos en código: $Q_1,Q_2 \in [0,100]\%$ y corte por sobretemperatura.
- **INV-25** Toda corrida registra metadatos: fecha, $T_s$, ambiente, identificador de placa, hash de git del script.
- **INV-26** Matrices $Q,R$ del LQR e hiperparámetros de RL viven en archivo de configuración versionado, nunca incrustados en el código.
- **INV-27** Toda comparación LQR vs. RL se ejecuta bajo condiciones idénticas (mismos setpoints, mismo $T_s$, misma temperatura inicial).
- **INV-28** El modelo usado para entrenar está documentado y **validado contra datos reales** antes de cualquier afirmación sim-to-real.

### `.claude/rules/working-paper-format.md` → formato de tesis

Reescritura: `\documentclass[12pt]{report}` o `book`, `babel` en español, portada de la
Universidad Distrital, estructura por capítulos, y **estilo de cita IEEE numérico**
(`biblatex` con `style=ieee`) en lugar de `authoryear` de economía. Se conserva la disciplina
que sí aplica: booktabs, `hyperref` penúltimo, `cleveref` después, `microtype`, notas en todas
las tablas y figuras.

### Estándares de código

- `.claude/references/coding-standards-python.md` — sustituir el stack econométrico
  (`linearmodels`, `statsmodels`) por el de control/RL: `numpy`, `scipy`, `control`, `tclab`,
  `gymnasium`, `stable-baselines3`, `torch`, `pandas`, `matplotlib`. Levantar la prohibición de
  `sklearn`/`seaborn` (era una regla de inferencia causal, aquí no aplica). Añadir sección de
  **bucle de control en tiempo real** y de **seguridad de hardware**.
- `.claude/references/coding-standards-matlab.md` — **archivo nuevo**: convenciones MATLAB, uso
  de `ss`/`c2d`/`dlqr`/`lqr`, prohibición de `clear all` y rutas absolutas, versionado de `.slx`
  (binario: exigir exportar parámetros a `.m`/`.json`), y el contrato de interoperación con Python.
- `.claude/references/coding-standards-r.md` → `.template-reference/` (R sale del proyecto).

---

## Fase 5 — Recalibrar los 6 agentes críticos

Reescritura del vocabulario, conservando la estructura y las rúbricas de puntuación:

| Agente | Reorientación |
|---|---|
| `strategist` | "Estrategia de identificación causal" → **estrategia de modelado, control y diseño experimental**: identificación del sistema, diseño LQR ($Q$, $R$, discretización, observador de Kalman si el estado no se mide), formulación del MDP (estado, acción, recompensa, episodio), protocolo experimental y criterios de éxito |
| `strategist-critic` | Amenazas propias del dominio: controlabilidad/observabilidad, sobreajuste al simulador, brecha sim-to-real, reward hacking, saturación del actuador, ruido y deriva térmica, repeticiones insuficientes, comparación sesgada |
| `coder` | Stack Python/MATLAB, patrón de bucle de control con muestreo determinista, capa de hardware segura, estructura de experimentos y registro |
| `coder-critic` | Las 16 categorías recalibradas a control/RL/hardware, incluidos INV-23 a INV-28 |
| `domain-referee` | Perspectiva de un ingeniero de control, no de un economista de campo |
| `methods-referee` | Rigor experimental, validez de la comparación, garantías de estabilidad, reproducibilidad de RL (semillas, hiperparámetros, varianza entre corridas) |

Los 15 agentes restantes (librarian, explorer, writer, storyteller, theorist, editor, verifier y
sus críticos) **no se tocan ahora**: se calibran solos leyendo `domain-profile.md`, y ajustarlos
antes de conocer el método sería trabajo en buena parte desperdiciado.

---

## Fase 6 — Andamiaje del proyecto

```
config/                      # YAML versionado: Q, R, T_s, setpoints, hiperparámetros (INV-26)
scripts/
  python/
    hardware/                # capa TCLab: adquisición, seguridad, apagado garantizado
    identification/          # escalón, PRBS, ajuste FOPDT y espacio de estados
    control/                 # diseño LQR, discretización, observador
    rl/                      # entorno Gymnasium, entrenamiento, evaluación
    analysis/                # métricas, figuras, tablas
    common/                  # rutas, configuración, utilidades de graficado
  matlab/
    identification/
    control/
data/
  raw/tclab_runs/            # CSV crudos por corrida, nunca editados
  raw/README.md              # esquema de logging y convención de nombres
  cleaned/
paper/                       # ← se conserva el nombre: las reglas y skills lo tienen cableado
  main.tex                   # la tesis
  sections/                  # capítulos en español
```

- `scripts/R/` se elimina.
- Esquema de registro documentado: `t_s, T1_C, T2_C, Q1_pct, Q2_pct, SP1_C, SP2_C, run_id`
  más un `.json` acompañante con los metadatos de INV-25.
- Nomenclatura de corridas: `AAAA-MM-DD_HHMMSS_<experimento>_<variante>.csv`.
- `requirements.txt` con versiones fijadas.
- Esqueleto LaTeX de la tesis: `paper/main.tex` con portada de la UD, `babel` español,
  estructura de capítulos y el preámbulo del nuevo formato.
- `Bibliography_base.bib`: sustituir los dos ejemplos de economía (Angrist & Pischke, Imbens)
  por la bibliografía canónica de control óptimo y RL, **solo con entradas verificadas**.

---

## Fase 7 — Verificación

1. `cd paper && latexmk main.tex` compila sin errores y produce PDF (requiere Fase 1).
2. `source .venv/bin/activate && python -c "import numpy, scipy, control, gymnasium, stable_baselines3"` sin error.
3. `grep -rniE 'JEL|parallel trends|difference-in-differences|AER|instrumental variable' .claude/ CLAUDE.md` → sin coincidencias fuera de `.template-reference/`.
4. `.claude/settings.json` es JSON válido y sin rutas de macOS: `python3 -m json.tool .claude/settings.json`.
5. Los hooks siguen ejecutándose (`protect-files.sh`, `post-edit-lint.sh` no rompen con el árbol nuevo).
6. `/dashboard` genera `project_dashboard.html` con el estado inicial.
7. Commit único en rama `config/adaptacion-control` con todo lo anterior.

---

## Siguiente paso, ya fuera de este plan

```
/discover interview control de temperatura TCLab con LQR y aprendizaje por refuerzo
```

Esa entrevista produce la pregunta de investigación, la especificación y el registro de decisión
que determinan *cuál* de las cuatro combinaciones LQR+RL persigues. Solo entonces tiene sentido
recalibrar el resto de agentes y arrancar la fase de estrategia.

---

## Qué NO hace este plan

- No define la pregunta de investigación ni el método (es la salida de `/discover`).
- No instala TeX Live, Python 3.12 ni MATLAB (requieren `sudo` o licencia).
- No toca los 15 agentes no críticos.
- No borra nada: todo lo de la plantilla queda en `.template-reference/`.
