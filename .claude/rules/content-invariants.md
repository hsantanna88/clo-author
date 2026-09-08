# Invariantes de contenido

No son negociables. Todo agente verifica contra ellos. Las violaciones son deducciones, no
sugerencias. Los críticos citan el número del invariante (p. ej. "viola INV-3") en sus informes.

---

## Documento

**INV-1.** Toda tabla tiene notas que explican variables clave, condiciones del experimento y
origen de los datos — vía `threeparttable` + `tablenotes` (tradicional) o `talltblr` con `note{}`
(tabularray).

**INV-2.** Toda figura tiene `\caption{}` con nota que explica qué se muestra, cómo leerla y de
qué corrida o script proviene. Los ejes llevan **unidades**.

**INV-3.** Sin `\hline` — usar `\toprule`, `\midrule`, `\bottomrule` (booktabs). Sin líneas
verticales.

**INV-4.** Las métricas de desempeño se reportan con **unidades explícitas** (IAE en °C·s,
sobreimpulso en %, tiempo de establecimiento en s, esfuerzo de control, energía). Toda métrica
medida sobre hardware se reporta como **media ± desviación estándar sobre N corridas**, con N
declarado. Una corrida única nunca se presenta como resultado. Sin estrellas de significancia:
no es una disciplina de contraste de hipótesis sobre datos observacionales.

**INV-5.** El resumen respeta el límite del reglamento de trabajos de grado de la Universidad
Distrital.

**INV-6.** Resumen en español y *abstract* en inglés, ambos con palabras clave / *keywords*.

**INV-7.** La notación es consistente en todo el documento: el mismo símbolo significa lo mismo
en todas partes. **Atención especial a la colisión $Q$**: matriz de peso del LQR frente a potencia
de los calentadores del TCLab. Fijar la convención en preliminares y sostenerla.

**INV-8.** Toda afirmación de desempeño tiene un **protocolo experimental documentado**: setpoints,
$T_s$, condición inicial, temperatura ambiente, duración, número de repeticiones. Sin protocolo no
hay afirmación.

**INV-9.** `biblatex` + `biber`, no `natbib` + `bibtex`. Estilo de cita **IEEE numérico**.

**INV-10.** `hyperref` cargado penúltimo en el preámbulo; `cleveref` inmediatamente después.

**INV-11.** Los números en el texto coinciden exactamente con las tablas y figuras. Sin
discrepancias de redondeo ni valores obsoletos.

**INV-12.** Sin títulos dentro de las figuras de matplotlib o MATLAB. El título va en el
`\caption{}` de LaTeX. Las etiquetas de panel ("Panel A: ...") dentro de figuras múltiples sí
están bien.

**INV-13.** Los scripts exportan entornos `tabular` desnudos — sin `\begin{table}`, `\caption{}`
ni notas. `main.tex` los envuelve.

## Código

**INV-14.** `np.random.seed()` / `set_seed()` (o el equivalente del lenguaje) se llama una sola
vez, al inicio del script principal, si hay algún elemento estocástico. En experimentos de RL:
**mínimo N semillas independientes**, con la dispersión entre ellas reportada. Una sola semilla no
constituye resultado.

**INV-15.** Todos los paquetes y librerías se importan al inicio del script, antes de cargar datos
o computar.

**INV-16.** Sin rutas absolutas. Todas las rutas relativas a la raíz del proyecto vía
`pathlib.Path` (Python) o `fullfile(fileparts(mfilename('fullpath')), ...)` (MATLAB).

**INV-17.** Sin crecimiento de listas o arreglos dentro de bucles. Preasignar los contenedores de
resultados — crítico en bucles de control muestreados, donde una reasignación puede desfasar el
periodo.

**INV-18.** Los archivos de salida van a la ruta indicada por *Output Organization* en `CLAUDE.md`.

**INV-19.** Funciones prohibidas: `os.chdir()` / `cd` (MATLAB), `clear all`, `pip install` dentro
de un script, `eval` sobre entrada no controlada.

## Hardware y experimentación

**INV-20.** Toda sesión con la placa física usa gestor de contexto (`with TCLab() as lab:`) y
**apaga los calentadores en un bloque `finally`**, incluso ante excepción o interrupción del
usuario. Un script que puede dejar los calentadores encendidos no se acepta.

**INV-21.** Límites de seguridad explícitos en el código: saturación $u \in [0, 100]\%$ y corte
por sobretemperatura. Los límites se declaran como constantes con nombre, no como números sueltos.

**INV-22.** Toda corrida registra metadatos junto a los datos: fecha y hora, $T_s$, temperatura
ambiente inicial, identificador de la placa, versión del script (hash de git) y semilla.

**INV-23.** Las matrices $Q$ y $R$ del LQR y los hiperparámetros de RL viven en un archivo de
configuración versionado bajo `config/`, nunca incrustados en el cuerpo del código.

**INV-24.** Toda comparación entre controladores se ejecuta bajo condiciones idénticas: mismos
setpoints, mismo $T_s$, misma condición inicial, mismo perfil de perturbación. El baseline recibe
un esfuerzo de sintonía comparable al del método propuesto.

**INV-25.** El modelo usado para entrenar o diseñar está **validado contra datos independientes**
de los usados para identificarlo, antes de cualquier afirmación sobre la planta física.

**INV-26.** Los datos crudos de `data/raw/tclab_runs/` nunca se editan. Toda transformación
produce un archivo nuevo en `data/cleaned/` mediante un script versionado.

## Trazabilidad

**INV-27.** Toda afirmación numérica del documento tiene entrada en el mapa de trazabilidad
(`quality_reports/claim_source_map_{proyecto}.md`), rastreable hasta una línea de script y un
archivo de salida concretos.

**INV-28.** Ninguna referencia bibliográfica se inventa. Las entradas cuyos datos exactos no estén
verificados llevan `% VERIFICAR` en `Bibliography_base.bib` y no pueden citarse en el documento
hasta confirmarse.

---

## Cómo usan los agentes este archivo

| Agente | Verifica | Acción ante violación |
|--------|----------|----------------------|
| **writer-critic** | INV-1 a INV-13, INV-27, INV-28 | Deducir según la rúbrica |
| **coder-critic** | INV-13 a INV-26 | Deducir según la rúbrica |
| **storyteller-critic** | INV-7, INV-11 (notación y cifras de la sustentación coinciden con la tesis) | Deducir según la rúbrica |
| **verifier** | INV-9, INV-10, INV-14, INV-15, INV-16, INV-19, INV-20, INV-21 | FALLA si se incumple |
| **hook de lint** | INV-14, INV-15, INV-16, INV-19, INV-20 | Advertencia informativa |
