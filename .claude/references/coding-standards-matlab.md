# Estándares de código: MATLAB / Simulink

Aplican al código MATLAB del proyecto, usado para identificación de sistemas y diseño del LQR.
El coder-critic los hace cumplir.

---

## 1. Alcance y división de trabajo

MATLAB no es el lenguaje principal del proyecto: Python lo es. MATLAB se usa donde aporta algo que
Python no da con la misma comodidad:

| Tarea | Herramienta |
|-------|-------------|
| Identificación paramétrica (`iddata`, `tfest`, `ssest`, `n4sid`) | MATLAB (System Identification Toolbox) |
| Validación de modelos (`compare`, `resid`) | MATLAB |
| Diseño y análisis del LQR (`dlqr`, `c2d`, `ctrb`, `obsv`) | Cualquiera de los dos |
| Simulación de diagramas de bloques | Simulink |
| Adquisición desde el TCLab | **Python** (`tclab`) |
| Entrenamiento de RL | **Python** (`stable-baselines3`) |
| Figuras de la tesis | **Python** (`matplotlib`), para un estilo único |

**Regla:** el lazo de control en tiempo real y la adquisición viven en Python. MATLAB produce
modelos y ganancias, no datos experimentales.

---

## 2. Contrato de interoperación con Python

Los dos lenguajes intercambian **archivos**, nunca valores copiados a mano.

```
data/cleaned/*.csv        →  MATLAB (readtable)      # datos de identificación
scripts/matlab/...        →  results/*.mat           # modelo identificado, ganancia K
results/*.mat             →  Python (scipy.io.loadmat)
```

- MATLAB escribe `.mat` **versión 7 o superior** (`save(archivo, 'var', '-v7')`), que
  `scipy.io.loadmat` lee sin problema. La versión `-v7.3` (HDF5) requiere `h5py`; evitarla salvo
  necesidad.
- Alternativa preferida para resultados simples (matrices `A`, `B`, `Q`, `R`, `K`): exportar a
  `.csv` o `.json`. Es legible, versionable y produce diffs útiles en git.
- Todo archivo intercambiado incluye las unidades y el tiempo de muestreo en su nombre o en un
  campo de metadatos. Una matriz `A` sin su `Ts` es inservible.

**Prohibido:** copiar una ganancia `K` de la consola de MATLAB y pegarla en un script de Python.
Rompe la trazabilidad (INV-27) y no sobrevive a un cambio del modelo.

---

## 3. Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Archivos de función | `snake_case.m` | `identificar_fopdt.m` |
| Scripts | `snake_case.m` con verbo | `disenio_lqr.m` |
| Funciones | `snake_case` | `validar_modelo()` |
| Variables | `snake_case` | `n_pasos`, `t_muestreo` |
| Constantes | `MAYUS_SNAKE_CASE` | `TS`, `LIMITE_TEMPERATURA` |
| Matrices del sistema | Mayúscula, notación de control | `A`, `B`, `C`, `Q`, `R`, `K`, `P` |
| Modelos de `ident` | sufijo del tipo | `sys_ss`, `sys_fopdt`, `sys_arx` |

Discreto y continuo se distinguen en el nombre: `A_c` / `A_d`, `sys_c` / `sys_d`. Confundirlos es
el error más costoso del proyecto.

---

## 4. Estructura de un script

```matlab
function K = disenio_lqr(archivo_modelo, archivo_config)
%DISENIO_LQR Calcula la ganancia LQR discreta a partir del modelo identificado.
%
%   K = DISENIO_LQR(archivo_modelo, archivo_config) carga el modelo en espacio
%   de estados y las matrices de peso, verifica controlabilidad y devuelve la
%   ganancia de realimentacion.
%
%   Entradas:
%       archivo_modelo - ruta al .mat con el sistema discreto sys_d
%       archivo_config - ruta al .json con las matrices Q y R
%
%   Salida:
%       K - ganancia de realimentacion, u = -K*x

    raiz = fileparts(fileparts(fileparts(mfilename('fullpath'))));
    datos = load(fullfile(raiz, archivo_modelo));
    cfg   = jsondecode(fileread(fullfile(raiz, archivo_config)));

    sys_d = datos.sys_d;
    Q = cfg.lqr.Q;
    R = cfg.lqr.R;

    % Controlabilidad antes de disenar: sin ella el LQR no esta definido
    if rank(ctrb(sys_d.A, sys_d.B)) < size(sys_d.A, 1)
        error('disenio_lqr:noControlable', ...
              'El par (A,B) no es controlable; el LQR no esta definido.');
    end

    [K, P, polos] = dlqr(sys_d.A, sys_d.B, Q, R);

    if any(abs(polos) >= 1)
        error('disenio_lqr:inestable', ...
              'Lazo cerrado con polos fuera del circulo unitario.');
    end

    save(fullfile(raiz, 'results', 'ganancia_lqr.mat'), 'K', 'P', 'polos', '-v7');
end
```

Puntos que el crítico verifica en este patrón:

- **Función, no script suelto**, cuando produce un resultado reutilizable. Los scripts se reservan
  para orquestar.
- **Ruta relativa** derivada de `mfilename('fullpath')`, nunca absoluta (INV-16).
- **Configuración desde archivo**, no incrustada (INV-23).
- **Verificación de controlabilidad antes de diseñar**, y de estabilidad después.
- **Errores con identificador** (`componente:motivo`), para poder atraparlos por tipo.

---

## 5. Prohibido

| Patrón | Motivo | En su lugar |
|--------|--------|-------------|
| `clear all`, `close all`, `clc` al inicio de una función | Borra el estado del llamador; señal de script disfrazado de función | Escribir funciones con entradas y salidas explícitas |
| `cd` dentro de un script | Rompe la portabilidad (INV-19) | `fullfile` desde `mfilename('fullpath')` |
| Rutas absolutas (`C:\Users\...`, `/home/...`) | No funciona en otra máquina (INV-16) | Rutas relativas a la raíz del proyecto |
| Variables globales | Estado oculto, imposible de rastrear | Parámetros de función |
| `eval` | Ilegible y sin verificación | Indexación o `struct` |
| Crecer arreglos en un bucle | O(n²) por reasignación (INV-17) | `zeros(n,1)` antes del bucle |
| `i` o `j` como índice de bucle | Sombrean la unidad imaginaria | `k`, `idx`, `n` |
| Ganancias o matrices de peso escritas en el cuerpo | Rompe INV-23 | `config/*.json` o `*.yaml` |
| Figuras finales generadas en MATLAB | Dos estilos distintos en la misma tesis | Exportar datos y graficar en `matplotlib` |

---

## 6. Simulink

Los archivos `.slx` son **binarios**: git no puede mostrar diferencias ni fusionar cambios. En
consecuencia:

- **Ningún parámetro numérico vive dentro del bloque.** Los bloques leen variables del workspace,
  cargadas desde un `.m` o `.json` versionado. El `.slx` define la estructura; el archivo de
  configuración define los valores.
- Cada `.slx` va acompañado de un `.m` que lo configura y ejecuta:
  `sim_lazo_lqr.slx` + `configurar_sim_lazo_lqr.m`.
- Un solo autor edita un `.slx` a la vez. No hay resolución de conflictos posible.
- Exportar una imagen del diagrama (`print -dpdf`) al preparar la tesis: el diagrama de bloques va
  en el documento, y el PDF sí es revisable.
- Al hacer commit de un `.slx`, describir el cambio en el mensaje con detalle: es lo único que
  quedará como registro de qué cambió.

---

## 7. Verificación antes de entregar un resultado

Antes de que una ganancia o un modelo salga de MATLAB hacia la tesis:

- [ ] El modelo se validó contra una corrida distinta de la de identificación (INV-25)
- [ ] Se reporta el criterio de ajuste (FIT, `compare`) con su valor
- [ ] El tiempo de muestreo del modelo coincide con el del lazo de Python
- [ ] Se verificó controlabilidad y, si hay observador, observabilidad
- [ ] Los polos de lazo cerrado están dentro del círculo unitario
- [ ] El resultado se guardó en archivo, no se copió de la consola
- [ ] Las matrices `Q` y `R` usadas provienen de `config/`, y quedan registradas junto al resultado
