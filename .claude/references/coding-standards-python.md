# Estándares de código: Python

Aplican a todo el código Python del proyecto. El coder-critic los hace cumplir.

---

## 1. Entorno y dependencias

- **Python 3.12** en `.venv/` — el intérprete del sistema (3.14) no tiene ruedas de `torch` ni
  `stable-baselines3`
- `requirements.txt` versionado con versiones fijadas
- Sin `pip install` dentro de los scripts (INV-19)

### Stack

| Paquete | Uso |
|---------|-----|
| `numpy` | Álgebra lineal, arreglos |
| `scipy` | Optimización, señales, `scipy.io` para intercambio con MATLAB |
| `pandas` | Series temporales de las corridas |
| `matplotlib` | Todas las figuras |
| `control` (python-control) | Espacio de estados, `lqr`/`dlqr`, `c2d`, controlabilidad |
| `tclab` | Interfaz con la placa física y con su simulador |
| `pyserial` | Transporte serial subyacente |
| `gymnasium` | Entorno de RL |
| `stable-baselines3` | Algoritmos de RL (PPO, SAC, TD3, DDPG) |
| `torch` | Backend de redes neuronales |
| `pyyaml` | Lectura de la configuración de `config/` |

### Prohibido

| Práctica | Motivo | En su lugar |
|----------|--------|-------------|
| `time.sleep(Ts)` como reloj del lazo | Acumula deriva: el periodo real es `Ts` + tiempo de cómputo | Reloj de deadline absoluto (ver sección 4) o `tclab.clock()` |
| Matrices `Q`, `R` o hiperparámetros incrustados en el código | Rompe INV-23 | `config/*.yaml` |
| Escribir en `data/raw/` | Los datos crudos son evidencia inmutable (INV-26) | Escribir en `data/cleaned/` |
| Rutas absolutas | Rompe INV-16 | `pathlib.Path` relativa a la raíz |

## 2. Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Archivos y módulos | `snake_case.py` | `disenio_lqr.py` |
| Funciones | `snake_case` | `identificar_fopdt()` |
| Variables | `snake_case` | `n_pasos`, `t_muestreo` |
| Constantes | `MAYUS_SNAKE_CASE` | `TS`, `LIMITE_TEMPERATURA` |
| Clases | `PascalCase` | `EntornoTCLab` |
| Alias de tipo | `PascalCase` | `ArregloFloat` |
| Booleanos | prefijo `es_`, `hay_`, `usa_` | `es_hardware`, `hay_saturacion` |
| Auxiliares privados | `_guion_bajo_inicial` | `_validar_config()` |

Matrices del sistema en mayúscula, siguiendo la notación de control: `A`, `B`, `C`, `D`, `Q`, `R`,
`K`, `P`. Es la excepción deliberada a `snake_case` — la legibilidad frente a las ecuaciones de la
tesis pesa más que la convención de PEP 8.

**Cuidado con la colisión `Q`:** la matriz de peso del LQR y la potencia de los calentadores del
TCLab comparten letra. En código, la matriz es `Q` y las potencias son `u1`, `u2` (o el arreglo
`u`). Nunca `Q1` para una potencia si `Q` ya es la matriz de peso.

---

## 3. Estilo

- **Formateador:** `black` (obligatorio, antes de cada commit)
- **Linter:** `ruff` (obligatorio, cero advertencias)
- **Orden de importaciones:** `isort` (estándar → terceros → local)
- **Ancho de línea:** 88 caracteres
- **Docstrings:** formato NumPy, en español
- **Anotaciones de tipo:** obligatorias en toda firma de función

```python
from pathlib import Path

import numpy as np
import control
from numpy.typing import NDArray

ArregloFloat = NDArray[np.float64]


def disenar_lqr(
    A: ArregloFloat,
    B: ArregloFloat,
    Q: ArregloFloat,
    R: ArregloFloat,
    *,
    ts: float,
) -> tuple[ArregloFloat, ArregloFloat]:
    """Diseña el regulador LQR discreto para el sistema dado.

    Parameters
    ----------
    A, B : ArregloFloat
        Matrices del sistema en tiempo discreto, muestreado a `ts`.
    Q, R : ArregloFloat
        Matrices de peso del estado y del esfuerzo de control.
    ts : float
        Tiempo de muestreo en segundos, solo para verificación de consistencia.

    Returns
    -------
    K : ArregloFloat
        Ganancia de realimentación, u = -K x.
    P : ArregloFloat
        Solución de la ecuación algebraica de Riccati.

    Raises
    ------
    ValueError
        Si el par (A, B) no es controlable.
    """
```

---

## 4. Bucle de control en tiempo real

El TCLab es hardware: un lazo que se desfasa produce datos inválidos, no solo lentos.

### Reloj de deadline absoluto

```python
# CORRECTO: el periodo no acumula deriva
t0 = time.perf_counter()
for k in range(n_pasos):
    deadline = t0 + (k + 1) * TS
    y = leer_salida(lab)
    u = controlador(y)
    aplicar_entrada(lab, u)
    registrar(k, y, u)
    retraso = deadline - time.perf_counter()
    if retraso < 0:
        n_desbordes += 1          # se cuenta y se reporta, no se ignora
    else:
        time.sleep(retraso)

# INCORRECTO: el periodo real es TS + tiempo de computo, y crece con el
for k in range(n_pasos):
    ...
    time.sleep(TS)
```

- **Contar y reportar los desbordes de periodo.** Un lazo que perdió deadlines invalida las
  métricas temporales; ocultarlo es peor que tenerlos.
- `tclab.clock(tfinal, tstep)` es aceptable y es lo idiomático de la librería; si se usa, verificar
  igualmente el jitter registrando la marca de tiempo real de cada muestra.
- **Registrar el tiempo real de cada muestra**, no el nominal `k * TS`. La columna `t_s` del CSV
  contiene el instante medido.

### Preasignación

```python
# CORRECTO
T1 = np.empty(n_pasos, dtype=np.float64)
u1 = np.empty(n_pasos, dtype=np.float64)

# INCORRECTO: reasignar dentro de un lazo muestreado puede costar un deadline
T1 = []
T1.append(lab.T1)
```

### Reproducibilidad

```python
# CORRECTO: objeto RNG explícito, semilla desde configuración
rng = np.random.default_rng(seed=cfg["semilla"])

# INCORRECTO: estado global
np.random.seed(42)
```

Para RL, fijar la semilla en los tres lugares: `numpy`, `torch` y el entorno de `gymnasium`.
Ejecutar **N semillas independientes** y reportar la dispersión (INV-14).

---

## 5. Seguridad del hardware

**Es la regla más importante del proyecto.** Los calentadores siguen encendidos si el proceso
muere sin apagarlos.

```python
LIMITE_POTENCIA = 100.0        # %
LIMITE_TEMPERATURA = 65.0      # °C — corte de seguridad

def experimento(cfg: dict) -> pd.DataFrame:
    lab = tclab.TCLab()
    try:
        for k in range(n_pasos):
            if lab.T1 > LIMITE_TEMPERATURA or lab.T2 > LIMITE_TEMPERATURA:
                raise RuntimeError(f"Corte por sobretemperatura en el paso {k}")
            u = np.clip(controlador(...), 0.0, LIMITE_POTENCIA)
            lab.Q1(u[0]); lab.Q2(u[1])
            ...
    finally:
        lab.Q1(0); lab.Q2(0)   # se ejecuta ante excepción, Ctrl-C o retorno normal
        lab.close()
```

Reglas (INV-20, INV-21):

- El apagado va en `finally`, nunca solo al final del camino feliz.
- Los límites son constantes con nombre en mayúsculas, nunca números sueltos en el cuerpo.
- La saturación se aplica **siempre** antes de escribir al actuador, aunque el controlador ya
  debiera respetarla. El actuador es la última línea de defensa.
- `KeyboardInterrupt` es una excepción: `finally` la cubre. No atraparla con `except` para
  "limpiar" y luego re-lanzarla — basta con `finally`.
- La misma disciplina aplica al simulador (`tclab.setup(connected=False)`), para que el código de
  experimento sea idéntico en ambos modos.

### Simulación y hardware con el mismo código

```python
TCLab = tclab.setup(connected=cfg["hardware"], speedup=cfg.get("speedup", 1))
```

Un solo camino de código para ambos modos. Si el script de simulación y el de hardware divergen,
la validación sim-to-real deja de significar algo.

---

## 6. Registro de corridas

Cada experimento produce dos archivos con el mismo nombre base en `data/raw/tclab_runs/`:

- `AAAA-MM-DD_HHMMSS_<experimento>_<variante>.csv` — columnas
  `t_s, T1_C, T2_C, Q1_pct, Q2_pct, SP1_C, SP2_C`
- `..._meta.json` — metadatos de INV-22: `Ts`, temperatura ambiente inicial, id de placa,
  hash de git, semilla, modo (hardware/simulación), configuración usada, desbordes de periodo

```python
meta = {
    "ts_s": TS,
    "ambiente_inicial_C": T_amb,
    "placa": cfg["id_placa"],
    "git_hash": subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                               capture_output=True, text=True).stdout.strip(),
    "semilla": cfg["semilla"],
    "modo": "hardware" if cfg["hardware"] else "simulacion",
    "desbordes_periodo": n_desbordes,
}
```

Los archivos de `data/raw/` no se editan jamás (INV-26).

---

## 7. Diseño de funciones y manejo de errores

- Tipos en todas las firmas; docstrings en formato NumPy
- Fallar rápido y ruidoso: `ValueError` para entradas inválidas, `RuntimeError` para fallas de
  cómputo o de hardware. Nunca devolver `None` en silencio
- Verificar `nan`/`inf` tras operaciones numéricas, especialmente al resolver Riccati:

```python
K, P, autovalores = control.dlqr(A_d, B_d, Q, R)
if np.any(np.abs(autovalores) >= 1.0):
    raise RuntimeError("El lazo cerrado no es estable: hay polos fuera del círculo unitario")
```

- Verificar controlabilidad **antes** de diseñar el LQR:

```python
if np.linalg.matrix_rank(control.ctrb(A_d, B_d)) < A_d.shape[0]:
    raise ValueError("El par (A, B) no es controlable: el LQR no está definido")
```

---

## 8. Patrones prohibidos

| Patrón | Motivo | En su lugar |
|--------|--------|-------------|
| `os.chdir()` | Rompe la portabilidad | `pathlib.Path` relativa a la raíz |
| Rutas absolutas | Rompe la portabilidad | `pathlib.Path` o módulo de configuración |
| `from modulo import *` | Contamina el espacio de nombres | Importaciones explícitas |
| `sum`/`min`/`max` de Python sobre arreglos | Lento y con semántica distinta | `np.sum`, `np.min`, `np.max` |
| `np.random.seed()` global | No es seguro en paralelo ni reproducible por partes | `np.random.default_rng(semilla)` |
| Listas que crecen en el lazo de control | Puede costar un deadline | Preasignar con `np.empty()` |
| `except:` desnudo | Se traga todos los errores, incluidos los de hardware | `except ErrorEspecifico:` |
| Argumentos por defecto mutables | Estado compartido entre llamadas | `None` por defecto y crear dentro |
| `time.sleep(TS)` como reloj del lazo | Acumula deriva de periodo | Deadline absoluto o `tclab.clock()` |
| Apagar los calentadores fuera de `finally` | Deja el hardware encendido ante excepción | Bloque `finally` (INV-20) |
| Constantes de sintonía en el cuerpo del código | Rompe INV-23 | `config/*.yaml` |
