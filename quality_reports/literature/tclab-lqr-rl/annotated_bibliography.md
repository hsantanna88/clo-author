# Bibliografía anotada — LQR + aprendizaje por refuerzo sobre TCLab

**Proyecto:** tclab-lqr-rl
**Fecha de la búsqueda:** 2026-09-07 · **Revisada:** 2026-09-08 (ronda 1 de corrección)
**Agente:** librarian
**Estado de la pregunta de investigación:** NO DEFINIDA. La búsqueda cubre deliberadamente las
cuatro variantes en consideración (residual, sintonía de $Q$/$R$, filtro de seguridad, comparativo).

---

## 0. Cómo leer este documento

### Escala de proximidad (la usada aquí)

| Valor | Significado |
|-------|-------------|
| **1** | Compite directamente: misma pregunta, método similar |
| **2** | Muy relacionado: misma pregunta, distinto método o distinta planta |
| **3** | Relacionado: tema solapado, ángulo distinto |
| **4** | Fondo: aporta teoría, método o contexto |
| **5** | Tangencial: solo útil como encuadre |

### Proximidad condicionada al eje (añadida en la ronda 1)

Con cuatro ejes vivos y la pregunta de investigación sin definir, un escalar único subestima a los
competidores más directos. Las entradas de proximidad **1 y 2** llevan además un **vector de cuatro
proximidades**, una por eje, con el formato:

`Proximidad por eje: (a)=N · (b)=N · (c)=N · (d)=N`

El escalar general es el mínimo del vector, es decir, la proximidad bajo el eje en que la obra
compite más de cerca. La tabla consolidada está en §11.

### Nivel de lectura (declaración de honestidad)

Cada entrada declara **qué leí realmente**. Ninguna entrada de esta bibliografía fue leída en
texto completo. Los niveles son:

- **[META]** — metadatos bibliográficos verificados contra Crossref o contra la página oficial de
  actas (PMLR, NeurIPS Proceedings, AAAI OJS). No leí el contenido más allá del título.
- **[ABS]** — además de los metadatos, leí el resumen (abstract) del artículo.
- **[WEB]** — abrí y leí una página web que no es un artículo (documentación, tutorial).
  *(Nivel añadido en la ronda 1.)*
- **[SERP]** — solo dispongo de lo que apareció en páginas de resultados de búsqueda o en
  síntesis de esos resultados. **Menor confianza.**

**Consecuencia directa:** los campos *Validación* (número de corridas y semillas) y *Resultado
principal con magnitud* están **vacíos o marcados como no leídos** en la mayoría de entradas,
porque esa información vive en el cuerpo del artículo y no en el resumen. Rellenarlos requiere
descargar y leer los PDF. **No inventé ninguna cifra.** Donde aparece un número, viene del
resumen del propio artículo o de la síntesis de búsqueda, y así se indica.

**Regla de disciplina reforzada en la ronda 1.** El crítico señaló que al menos nueve entradas
`[META]` hacían afirmaciones de contenido que el título no sostiene. La regla que ahora se aplica:
*una entrada `[META]` puede describir el objeto de estudio que su título nombra, pero no puede
atribuir resultados, mecanismos ni taxonomías que solo estén en el cuerpo.* Donde la afirmación era
necesaria para el argumento, leí el resumen y subí el nivel; donde no lo era, recorté la afirmación.

---

## 1. Plataforma TCLab — qué se ha publicado sobre este banco concreto

Este es el eje que define el contexto de la tesis. La literatura publicada y revisada por pares
sobre el TCLab es **escasa y mayoritariamente docente**. El corpus técnico se reduce a un puñado
de trabajos.

### 1.1 Park, Martin, Kelly y Hedengren (2020) — el artículo de referencia del banco

> Park, J., Martin, R. A., Kelly, J. D., y Hedengren, J. D. (2020). *Benchmark temperature
> microcontroller for process dynamics and control*. **Computers & Chemical Engineering**, 135,
> 106736. DOI: 10.1016/j.compchemeng.2020.106736

- **Proximidad: 2** — misma planta, distinto método (MPC, no RL, no LQR). Es la cita obligatoria
  para justificar el TCLab como banco de pruebas legítimo y no como juguete docente.
- **Proximidad por eje: (a)=3 · (b)=3 · (c)=3 · (d)=2** — compite más de cerca con el eje
  comparativo, porque contrasta tres estructuras de modelo bajo MPC.
- **Pregunta/método:** propone el TCLab como *benchmark* estándar de hardware para métodos de
  modelado y control, contemplando restricciones reales (tiempo de ciclo, muestreo discreto,
  sobrecarga de comunicación, desajuste de modelo). Compara MPC con tres estructuras de modelo:
  basado en física, series temporales lineales (ARX) y Hammerstein con red neuronal.
- **Planta/banco:** TCLab, **hardware físico** (Arduino, 2 calentadores, 2 sensores, MIMO 2×2).
- **Validación:** no leída. El resumen no declara número de corridas.
- **Resultado principal:** no leído con magnitud. El resumen afirma que el TCLab tiene potencial
  como *benchmark* estándar y menciona una distribución de ~3000 unidades; no da cifras de
  desempeño comparativo de los tres modelos en el resumen.
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref).
- **Ronda 1:** este artículo fue la semilla del encadenamiento de citas. Tiene **84 obras citantes
  en OpenAlex**, todas revisadas por título. Ver `frontier_map.md` §5.4.

### 1.2 Patel (2023) y Patel (2022) — RL online sobre TCLab, sin simulador

> Patel, K. M. (2023). *A practical Reinforcement Learning implementation approach for continuous
> process control*. **Computers & Chemical Engineering**, 174, 108232.
> DOI: 10.1016/j.compchemeng.2023.108232

> Patel, K. M. (2022). *Safe, Fast and Explainable Online Reinforcement Learning for Continuous
> Process Control*. En **2022 IEEE International Symposium on Advanced Control of Industrial
> Processes (AdCONIP)**, pp. 54–60. DOI: 10.1109/ADCONIP55568.2022.9894195

- **Proximidad: 1** — es el trabajo publicado más cercano al núcleo de la tesis: RL sobre TCLab
  físico. **Riesgo de solapamiento alto** para cualquier variante que se plantee como
  "aplicar RL al TCLab".
- **Proximidad por eje: (a)=2 · (b)=3 · (c)=2 · (d)=1** — compite de frente con el eje comparativo
  y de cerca con el de seguridad, dado que el artículo de 2022 se titula explícitamente "Safe".
- **Pregunta/método:** formulación sistemática del problema de RL incorporando conocimiento de
  dominio sobre restricciones y objetivos del proceso, lo que reduce dimensionalidad; más
  modificaciones al proceso de exploración. Se declara agnóstico al algoritmo (aplicable a
  cualquier RL libre de modelo con estados y acciones continuos). **Explícitamente busca evitar
  el simulador** ("without requiring a simulation model").
- **Algoritmo:** DDPG.
- **Planta/banco:** dos procesos multivariables — una columna de destilación **simulada** y el
  **TCLab físico**.
- **Validación:** no leída. Sin dato de corridas ni semillas.
- **Resultado principal:** no leído con magnitud. El resumen reclama mejoras en *seguridad,
  velocidad y explicabilidad* de la implementación online, sin cifras en el resumen.
- **Nivel de lectura: [ABS]** para el artículo de 2023; **[META]** para el de 2022.
- **Hallazgo de la ronda 1:** la **versión de congreso de 2022 es precursora** del artículo de
  2023, mismo autor único (Saudi Aramco). No apareció en ninguna búsqueda por palabras clave de la
  ronda 0; la encontré por encadenamiento de citas desde Park et al. (2020). Es relevante porque su
  título antepone "Safe": si el esquema incluye algún mecanismo de seguridad explícito, toca
  también el eje (c).
- **Nota de honestidad:** no logré acceder al texto completo de ninguno de los dos (ScienceDirect y
  ResearchGate devolvieron 403). El estudiante debe conseguirlos por la biblioteca.

### 1.3 Soza Mamani y Prado Romo (2025) — NMPC + DRL sobre TCLab con retardos largos

> Soza Mamani, K. M., y Prado Romo, A. J. (2025). *Integrating Model Predictive Control with Deep
> Reinforcement Learning for Robust Control of Thermal Processes with Long Time Delays*.
> **Processes**, 13(6), 1627. DOI: 10.3390/pr13061627

- **Proximidad: 1** — TCLab físico + control óptimo/predictivo + DRL, con estudio comparativo.
  **Este es el principal riesgo de scooping identificado.**
- **Proximidad por eje: (a)=3 · (b)=1 · (c)=2 · (d)=1** — si su agente adapta las funciones de
  costo del NMPC, como sugiere el resumen, compite de frente con el eje (b).
- **Pregunta/método:** estrategia híbrida en la que las funciones de costo del NMPC se formulan
  como funciones de aprendizaje, y un agente actor-crítico ajusta dinámicamente las acciones de
  control mediante una política adaptativa alimentada por datos en tiempo real. El marco elimina
  la necesidad de sintonizar el costo terminal y de imponer restricciones estrictas en tiempo de
  ejecución.
- **Algoritmos:** DDPG y TD3, comparados contra NMPC.
- **Planta/banco:** **TCLab hardware**, con retardos largos y variables. Validación experimental
  declarada en el resumen.
- **Validación:** no leída. Sin dato de corridas ni semillas en el resumen.
- **Resultado principal:** el resumen afirma **desempeño de seguimiento comparable al NMPC**, con
  mayor adaptabilidad y robustez ante incertidumbre y perturbaciones. **Sin magnitud numérica en
  el resumen.**
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref; MDPI devolvió 403 al texto).
- **Nota:** la síntesis de una búsqueda web atribuyó erróneamente este artículo a otros autores
  (Onyenanu et al.). **Los autores correctos son los de Crossref: Soza Mamani y Prado Romo.**

### 1.4 Trabajos docentes y de control clásico sobre TCLab

> Rossiter, J. A., Pope, S. A., Jones, B. Ll., y Hedengren, J. D. (2019). *Evaluation and
> demonstration of take home laboratory kit*. **IFAC-PapersOnLine**, 52(9), 56–61.
> DOI: 10.1016/j.ifacol.2019.08.124

- **Proximidad: 4** — fondo institucional del banco. **Nivel de lectura: [META]** (Crossref).

> de Moura Oliveira, P. B., Hedengren, J. D., y Rossiter, J. A. (2020). *Introducing Digital
> Controllers to Undergraduate Students using the TCLab Arduino Kit*. **IFAC-PapersOnLine**,
> 53(2), 17524–17529. DOI: 10.1016/j.ifacol.2020.12.2662

- **Proximidad: 4** — controladores **digitales** sobre TCLab. Relevante porque la tesis diseñará
  el LQR en discreto: este trabajo establece precedente sobre el muestreo en esta planta.
- **Nivel de lectura: [META]** (Crossref; el PDF de White Rose muestra en cabecera la referencia
  completa).

> Insuasti, S., Paredes, J. L., y Camacho, O. (2022). *Controllers and Compensators Design for
> Undergraduate Control Students: Testing with TCLab Arduino kit*. En **2022 IEEE Sixth Ecuador
> Technical Chapters Meeting (ETCM)**, pp. 1–6. DOI: 10.1109/ETCM56276.2022.9935740

- **Proximidad: 3** — diseño de controladores clásicos validado sobre TCLab. Precedente
  metodológico latinoamericano para el flujo simulación → hardware.
- **Nivel de lectura: [META]** (Crossref).

> Páez Ardila, D., Martínez Reyes, D., Valencia Niño, C., Tanscheit, R., y Vellasco, M. (2022).
> *Comparative Study of PID, DMC, and Fuzzy PD+I Controllers in a Control Laboratory Kit*. En
> **2022 IEEE Latin American Conference on Computational Intelligence (LA-CCI)**, pp. 1–6.
> DOI: 10.1109/LA-CCI54402.2022.9981589

- **Proximidad: 3** — comparativa de tres controladores sobre el kit de laboratorio.
  *(Hallazgo de la ronda 1, vía encadenamiento de citas.)* Doble utilidad: documenta la densidad
  del eje (d) y es literatura latinoamericana.
- **Nivel de lectura: [META]** (Crossref).

> Tan, W., Han, W., y Xu, J. (2022). *State-Space PID: A Missing Link Between Classical and Modern
> Control*. **IEEE Access**, 10, 116540–116553. DOI: 10.1109/ACCESS.2022.3218657

- **Proximidad: 3** — *(hallazgo de la ronda 1)*. Cita a Park et al. (2020), luego pertenece al
  entorno de literatura del TCLab. Conecta el PID con el espacio de estados, que es exactamente el
  puente que la tesis necesita entre su línea base clásica y el LQR.
- **Nivel de lectura: [META]** (Crossref). No leí el resumen; la relevancia se infiere del título.

### 1.5 Recurso no publicado pero relevante

- **APMonitor, "TCLab with Reinforcement Learning"** (`apmonitor.com/do/index.php/Main/RLTCLab`).
  **No es una publicación revisada por pares.** Se cita, si acaso, como recurso de software, nunca
  como evidencia.
- **Nivel de lectura: [WEB]** — *(corregido en la ronda 1: la ronda 0 declaraba "no la abrí" y acto
  seguido afirmaba tres hechos técnicos. Ahora sí la abrí.)* Confirmado: usa **DDPG en PyTorch**,
  con un **entorno Gymnasium** personalizado que interfaz con TCLab. Dato nuevo y pertinente:
  el código corre por defecto sobre `tclab.TCLabModel()`, es decir **el simulador**, con la línea
  del hardware (`TCLab()`) comentada.
- **Consecuencia:** el solapamiento con este tutorial es con la parte de **simulación**, no con la
  experimental. Sigue siendo cierto que "DDPG sobre TCLab en simulación" está hecho y el jurado
  puede conocerlo. Proximidad **2 en cuanto a solapamiento práctico**.

### Vacío detectado en este eje

**No encontré ninguna publicación revisada por pares que aplique LQR al TCLab**, ni sola ni
combinada con RL. En la ronda 1 este vacío se sometió a la prueba decisiva: **las 84 obras que
citan a Park et al. (2020) fueron revisadas por título y ninguna menciona LQR, regulador lineal
cuadrático ni control óptimo** (`frontier_map.md` §5.4). Lo más cercano son Tan et al. (2022), sobre
PID en espacio de estados, y Manurung et al. (2021), sobre estimación con EKF (§9.2).

**Este vacío es real**, con la advertencia de que un vacío puede indicar tanto oportunidad como
falta de interés de la comunidad: aplicar LQR a una planta térmica no es novedoso *en sí mismo*.

---

## 2. RL en control de procesos — revisiones, benchmarks y guías

### 2.1 Faria, Capron, Secchi y de Souza (2022) — revisión con guías

> de Rezende Faria, R., Capron, B. D. O., Secchi, A. R., y de Souza Jr., M. B. (2022). *Where
> Reinforcement Learning Meets Process Control: Review and Guidelines*. **Processes**, 10(11),
> 2311. DOI: 10.3390/pr10112311

- **Proximidad: 4** — revisión de encuadre. **Nivel de lectura: [META]** (Crossref).

### 2.2 Park, Jung, Kim y Lee (2025) — revisión con problemas de referencia

> Park, J., Jung, H., Kim, J. W., y Lee, J. M. (2025). *Reinforcement Learning for Process
> Control: Review and Benchmark Problems*. **International Journal of Control, Automation and
> Systems**, 23(1), 1–40. DOI: 10.1007/s12555-024-0990-1

- **Proximidad: 3** — revisión reciente y extensa (40 páginas) que además define problemas de
  referencia. Punto de partida natural para el capítulo de estado del arte.
- **Nivel de lectura: [META]** (Crossref). No leí el resumen: lo que se afirma arriba (extensión,
  que define benchmarks) se deriva del título y del rango de páginas.

### 2.3 Bloor et al. (2026) — PC-Gym

> Bloor, M., Torraca, J., Sandoval, I. O., Ahmed, A., White, M., Mercangöz, M., Tsay, C.,
> del Río-Chanona, E. A., y Mowbray, M. (2026). *PC-Gym: Benchmark environments for process
> control problems*. **Computers & Chemical Engineering**, 204, 109363.
> DOI: 10.1016/j.compchemeng.2025.109363

- **Proximidad: 3** — infraestructura de benchmark en simulación para RL en control de procesos,
  con comparación contra un oráculo NMPC. Relevante metodológicamente: define cómo se compara
  RL contra control basado en modelo de forma justa.
- **Planta/banco:** **solo simulación** (CSTR, extracción multietapa, reactor de cristalización).
- **Resultado principal:** el resumen reporta que existen *brechas de desempeño* entre los
  algoritmos de RL y el oráculo NMPC, sin magnitud en el resumen.
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref).

### 2.4 Reiter et al. (2026) — síntesis MPC + RL

> Reiter, R., Hoffmann, J., Reinhardt, D., Messerer, F., Baumgärtner, K., Sawant, S.,
> Boedecker, J., Diehl, M., y Gros, S. (2026). *Synthesis of model predictive control and
> reinforcement learning: Survey and classification*. **Annual Reviews in Control**, 61, 101045.
> DOI: 10.1016/j.arcontrol.2026.101045

- **Proximidad: 3** — taxonomía de las formas de combinar control basado en modelo y RL.
- **CORRECCIÓN DE LA RONDA 1.** La ronda 0 afirmaba, desde nivel `[META]`, que *"la clasificación
  (RL sobre el controlador, RL que parametriza el controlador, controlador como filtro) mapea casi
  uno a uno sobre las cuatro variantes"*. **Esa afirmación era una extrapolación mía, no del
  artículo.** Leí el resumen del preprint (arXiv:2502.02133) y la taxonomía real se describe así:
  *"we focus on the versatile actor-critic RL approach as a basis for our categorization and examine
  how the online optimization approach of MPC can be used to improve the overall closed-loop
  performance of a policy."* Es decir: la base de la categorización es la **estructura
  actor-crítico**, y el eje examinado es **dónde entra la optimización en línea del MPC**.
- **Qué sí se puede decir con eso:** el trabajo confirma que la combinación de control basado en
  modelo con RL es un campo con taxonomía propia, y que el punto de entrada del componente clásico
  (en el actor, en el crítico, o filtrando la salida) es el eje discriminante. Eso **es** afín al
  marco de los cuatro ejes, pero la correspondencia "uno a uno" no está en la fuente y se retira.
- **Nivel de lectura: [ABS]** *(elevado desde `[META]` en la ronda 1)*.

### 2.5 Lin, Chen, Xie, Su y Huang (2024) — transferencia para RL en procesos

> Lin, R., Chen, J., Xie, L., Su, H., y Huang, B. (2024). *Facilitating Reinforcement Learning
> for Process Control Using Transfer Learning: Overview and Perspectives*. arXiv:2404.00247.

- **Proximidad: 3** — argumenta por qué el RL puro es inviable en la industria de procesos y
  cómo la transferencia (incluida sim-to-real) lo hace tratable.
- **Nivel de lectura: [SERP]** — sede de conferencia (ASCC 2024) mencionada en resultados de
  búsqueda, **no verificada**. Citar la versión arXiv hasta confirmar.

---

## 3. Mismo método, distinta planta: RL que aprende *sobre* un controlador clásico

Este bloque alimenta principalmente el **eje (a) — RL residual** y el **eje (b) — sintonía**.

### 3.1 Lawrence et al. (2022) — el PID como política entrenable, sobre hardware

> Lawrence, N. P., Forbes, M. G., Loewen, P. D., McClement, D. G., Backström, J. U., y
> Gopaluni, R. B. (2022). *Deep reinforcement learning with shallow controllers: An experimental
> application to PID tuning*. **Control Engineering Practice**, 121, 105046.
> DOI: 10.1016/j.conengprac.2021.105046

- **Proximidad: 2** — misma pregunta estructural que el eje (b) del estudiante, pero con PID en
  lugar de LQR y con un sistema de tanques en lugar del TCLab. **Es el modelo metodológico más
  claro para toda la tesis:** aborda exactamente las preocupaciones del jurado (interacción
  software/hardware, diseño experimental, eficiencia muestral, entrenamiento con restricciones de
  entrada, interpretabilidad).
- **Proximidad por eje: (a)=3 · (b)=2 · (c)=4 · (d)=3**
- **Método:** el controlador PID *es* la política de RL (red neuronal poco profunda), embebida en
  un marco actor-crítico.
- **Planta/banco:** **hardware** — sistema de dos tanques no interactuantes (según síntesis de
  búsqueda; entrenamiento realizado directamente sobre el sistema físico, sin preentrenamiento).
- **Validación / resultado:** no leídos.
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref; resumen leído en la página de
  arXiv de la versión preprint 2111.07171).

### 3.2 McClement et al. (2022) — meta-RL offline para sintonía de PI

> McClement, D. G., Lawrence, N. P., Backström, J. U., Loewen, P. D., Forbes, M. G., y
> Gopaluni, R. B. (2022). *Meta-reinforcement learning for the tuning of PI controllers: An
> offline approach*. **Journal of Process Control**, 118, 139–152.
> DOI: 10.1016/j.jprocont.2022.08.002

- **Proximidad: 3** — sintonía automática por RL entrenado *offline* y transferido. El patrón
  "entrenar fuera de línea, desplegar sin reentrenar" es aplicable al problema de entrenamiento
  inviable sobre la placa física.
- **Nivel de lectura: [META]** (Crossref). *(Ronda 1: se retira la afirmación sobre la planta usada,
  que en la ronda 0 se daba desde nivel `[META]` sin fuente abierta.)*

### 3.3 Lawrence et al. (2020) — PID y antiwindup como problema de RL

> Lawrence, N. P., Stewart, G. E., Loewen, P. D., Forbes, M. G., Backström, J. U., y
> Gopaluni, R. B. (2020). *Optimal PID and Antiwindup Control Design as a Reinforcement Learning
> Problem*. **IFAC-PapersOnLine**. arXiv:2005.04539.

- **Proximidad: 3** — trata explícitamente la **saturación del actuador** dentro del marco de RL.
  El TCLab satura en $[0,100]\%$; el perfil de dominio exige declarar cómo se maneja.
- **Nivel de lectura: [SERP]** — volumen 53 e intervalo de páginas 236–241 aparecieron en la
  síntesis de búsqueda pero **no los verifiqué contra Crossref**.

### 3.4 Bloor et al. (2025) — CIRL: estructura de control dentro de la política

> Bloor, M., Ahmed, A., Kotecha, N., Mercangöz, M., Tsay, C., y del Río-Chanona, E. A. (2025).
> *Control-Informed Reinforcement Learning for Chemical Processes*. **Industrial & Engineering
> Chemistry Research**, 64(9), 4966–4978. DOI: 10.1021/acs.iecr.4c03233

- **Proximidad: 2** — inyecta componentes de control PID *dentro de la arquitectura* de la
  política profunda. Es una tercera vía entre "residual" y "sintonía": la estructura del
  controlador clásico se convierte en sesgo inductivo de la red.
- **Proximidad por eje: (a)=2 · (b)=3 · (c)=4 · (d)=3**
- **Planta/banco:** procesos químicos; **verificar si hay hardware** (probablemente simulación).
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref).

### 3.5 Gros y Zanon (2020) — RL que sintoniza el controlador basado en modelo

> Gros, S., y Zanon, M. (2020). *Data-Driven Economic NMPC Using Reinforcement Learning*.
> **IEEE Transactions on Automatic Control**, 65(2), 636–648. DOI: 10.1109/TAC.2019.2913768

- **Proximidad: 3** — el resultado teórico central ("el esquema puede sintonizarse para entregar
  la política óptima del sistema real **incluso con un modelo equivocado**") es el argumento
  formal que justifica el eje (b).
- **Planta/banco:** simulación (ejemplo MPC lineal clásico + ejemplo no lineal estándar de ENMPC).
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref; resumen vía síntesis).

---

## 4. Eje (a): RL residual y corrección aprendida sobre una política base

### 4.1 Silver, Allen, Tenenbaum y Kaelbling (2018) — Residual Policy Learning

> Silver, T., Allen, K. R., Tenenbaum, J., y Kaelbling, L. P. (2018). *Residual Policy Learning*.
> arXiv:1812.06298.

- **Proximidad: 3** — fundamento conceptual del eje (a): $a = \mu(s) + \pi_\theta(s)$, donde
  $\mu$ es un controlador base bueno pero imperfecto.
- **Planta/banco:** tareas de manipulación robótica **simuladas**.
- **Nivel de lectura: [SERP]** — confirmé que **no encontré versión publicada revisada por pares**.
  Marca `% PUBLICACION_NO_COMPROBADA` en `references.bib`: **es citable como preprint.**
- **Ronda 1:** semilla del encadenamiento de citas. **52 obras citantes en OpenAlex, todas
  revisadas, ninguna en control de procesos ni en plantas térmicas.**

### 4.2 Johannink et al. (2019) — RL residual para control de robots

> Johannink, T., Bahl, S., Nair, A., Luo, J., Kumar, A., Loskyll, M., Ojea, J. A., Solowjow, E.,
> y Levine, S. (2019). *Residual Reinforcement Learning for Robot Control*. En **2019
> International Conference on Robotics and Automation (ICRA)**, pp. 6023–6029.
> DOI: 10.1109/ICRA.2019.8794127

- **Proximidad: 3** — la referencia canónica de RL residual con validación en hardware.
- **Nivel de lectura: [META]** (Crossref confirmó los 9 autores y las páginas). *(Ronda 1: se
  retira la afirmación de la ronda 0 sobre "simulación y hardware", que no estaba respaldada por el
  nivel declarado.)*
- **Ronda 1:** **45 obras citantes en OpenAlex, todas revisadas, ninguna en control de procesos ni
  en plantas térmicas.**

### 4.3 Ishihara et al. (2023) — residual sobre PID en cascada

> Ishihara, Y., Hazama, Y., Suzuki, K., Yokono, J. J., Sabe, K., y Kawamoto, K. (2023).
> *Improving Wind Resistance Performance of Cascaded PID Controlled Quadcopters using Residual
> Reinforcement Learning*. arXiv:2308.01648.

- **Proximidad: 3** — el ejemplo más limpio de "residual sobre un controlador clásico ya
  desplegado, para rechazar una perturbación que el controlador base no maneja bien". Traducido
  al TCLab: residual sobre LQR para rechazar corrientes de aire o deriva de temperatura ambiente.
- **Nivel de lectura: [SERP]** — la sede IROS 2023 apareció en la síntesis de búsqueda pero
  **no la verifiqué en Crossref**. Citar la versión arXiv.

### 4.4 Furieri, Galimberti y Ferrari-Trecate (2024) — mejorar desempeño *con* garantía

> Furieri, L., Galimberti, C. L., y Ferrari-Trecate, G. (2024). *Learning to Boost the
> Performance of Stable Nonlinear Systems*. **IEEE Open Journal of Control Systems**, 3, 342–357.
> DOI: 10.1109/OJCSYS.2024.3441768
> (Fe de erratas: **IEEE OJ-CSYS**, 4, 53, 2025. DOI: 10.1109/OJCSYS.2025.3529361.)

- **Proximidad: 3** — responde a la preocupación del jurado "¿qué garantiza que la corrección
  aprendida no desestabilice el lazo?".
- **Nivel de lectura: [ABS]** *(elevado desde `[META]` en la ronda 1: leí el resumen en
  arXiv:2405.00871, porque la afirmación era load-bearing en tres documentos).*
- **Resultado principal, ahora citable con precisión.** El resumen dice literalmente: *"we
  guarantee $L_p$ closed-loop stability even if optimization is halted prematurely, and even when
  the ground-truth dynamics are unknown, with vanishing conservatism in the class of stabilizing
  policies as the model uncertainty is reduced to zero."* El mecanismo es una sinergia entre el
  principio de **Internal Model Control (IMC)** para sistemas no lineales y métodos de optimización
  sin restricciones para aprender dinámicas estables.
- **Planta/banco:** el resumen dice *"several numerical experiments"* y **no nombra ninguna planta**.
  Es simulación; no hay hardware declarado. *(La ronda 0 decía "presumiblemente simulación"; ahora
  está confirmado que el resumen no declara hardware, que es distinto de confirmar que no lo hay.)*
- **Advertencia de calibración:** es un artículo teóricamente pesado para un trabajo de pregrado.
  Sirve como *cita de encuadre y de alcance*, no como resultado a replicar.

### 4.5 Holt y Armellin (2025) — RL que "mejora" un LQR, con función de Lyapunov de control

> Holt, H., y Armellin, R. (2025). *Reinforcement Learning Enhanced LQR and Control Lyapunov
> Functions for Spacecraft Proximity Operations*. **IEEE Transactions on Robotics**, 41,
> 5117–5129. DOI: 10.1109/TRO.2025.3600160

- **Proximidad: 2** — el título describe casi literalmente el eje (a) combinado con el eje (c).
  **Es la evidencia más fuerte de que la combinación LQR+RL es una línea viva y publicable en 2025.**
- **Proximidad por eje: (a)=1 · (b)=3 · (c)=1 · (d)=4**
- **Planta/banco:** dinámica de naves espaciales. **No verificado si hay hardware.**
- **Nivel de lectura: [META]** (Crossref). Lo anterior se deriva del título; no leí el resumen.

### 4.6 Alqithami (2026) — residual + escudo de seguridad en control de procesos

*(Entrada nueva de la ronda 1. Corrige el vacío que la ronda 0 declaraba en este eje.)*

> Alqithami, S. (2026). *AgentTwin: A multi-agent digital-twin testbed for supervisory
> operating-mode scheduling and residual regulatory control on the Tennessee Eastman Process with
> a solver-backed safety shield*. **Journal of Process Control**.
> DOI: 10.1016/j.jprocont.2026.103735

- **Proximidad: 2** — es **la única obra de RL residual situada en control de procesos químicos**
  que encontré en un corpus de 187 registros. Combina residuo sobre control regulatorio con un
  escudo de seguridad resuelto por solver: ejes (a) y (c) a la vez.
- **Proximidad por eje: (a)=1 · (b)=4 · (c)=2 · (d)=4**
- **Planta/banco:** Tennessee Eastman Process, gemelo digital. Es un benchmark **simulado** de la
  industria química, no hardware; y es de escala muy superior al TCLab.
- **Validación / resultado:** no leídos.
- **Nivel de lectura: [META]** (Crossref confirmó autor, revista, año, DOI; volumen y número de
  artículo aún no expuestos). Lo anterior se deriva del título, que es inusualmente descriptivo.
- **Consecuencia para la tesis:** **estrecha el vacío del eje (a).** Ya no se puede decir "no hay
  RL residual en control de procesos". Sí se puede decir "no hay RL residual en procesos térmicos
  de laboratorio ni sobre TCLab, y en control de procesos hay una sola obra, sobre un benchmark
  simulado de escala industrial". **Lectura prioritaria.**

### Vacío detectado en este eje

**No encontré ningún trabajo de RL residual sobre un proceso térmico de laboratorio, ni sobre el
TCLab.** En la ronda 1 el vacío se sometió a tres pruebas independientes —citas hacia adelante de
Silver (52 obras), de Johannink (45 obras) y barrido del corpus completo de OpenAlex (187 registros,
100 revisados)— y **sobrevive**, aunque más estrecho que en la ronda 0. Ver `frontier_map.md` §5.

---

## 5. Eje (b): el aprendizaje sintoniza las matrices de costo $Q$ y $R$

### 5.1 Marco, Hennig, Bohg, Schaal y Trimpe (2016) — sintonía automática del LQR con BO

> Marco, A., Hennig, P., Bohg, J., Schaal, S., y Trimpe, S. (2016). *Automatic LQR tuning based
> on Gaussian process global optimization*. En **2016 IEEE International Conference on Robotics
> and Automation (ICRA)**, pp. 270–277. DOI: 10.1109/ICRA.2016.7487144

- **Proximidad: 2** — misma pregunta que el eje (b) —ajustar automáticamente los pesos del costo
  cuadrático— pero con **optimización bayesiana (Entropy Search)** en lugar de RL, y sobre un
  brazo robótico de 7 grados de libertad equilibrando un péndulo invertido.
- **Proximidad por eje: (a)=4 · (b)=2 · (c)=5 · (d)=4**
- **Planta/banco:** **hardware** (brazo robótico de 7 GDL). Problemas de sintonía de 2 y 4
  dimensiones.
- **Consecuencia para la tesis:** si el estudiante elige el eje (b), **este artículo es la línea
  base contra la que debe justificarse**: "¿por qué RL y no optimización bayesiana, que es más
  eficiente en muestras y por tanto más apta para una planta lenta como el TCLab?".
- **Nivel de lectura: [META]** (Crossref).

### 5.2 Zhang, Yan, Yang y Zhou (2026) — RL jerárquico que optimiza $Q$ y $R$

> Zhang, Y., Yan, X., Yang, W., y Zhou, Y. (2026). *Hierarchical Reinforcement Learning–Based
> Optimal Control for Model-Free Linear Systems*. **Mathematics**, 14(5), 895.
> DOI: 10.3390/math14050895

- **Proximidad: 2** — es la formalización más reciente y más directa del eje (b): arquitectura de
  dos niveles donde un **meta-agente de alto nivel optimiza adaptativamente $Q$ y $R$** mediante
  evaluación de trayectorias basada en entropía, mientras un agente base ejecuta iteración de
  políticas libre de modelo para actualizar la ley de realimentación de estados.
- **Proximidad por eje: (a)=3 · (b)=1 · (c)=5 · (d)=4**
- **Planta/banco:** **presumiblemente solo sistemas lineales en simulación — no verificado.**
  El resumen no menciona hardware, pero no leí el cuerpo del artículo. Esta afirmación es
  load-bearing: sobre ella descansa el vacío del eje (b). Si Zhang et al. incluyen validación en
  planta, ese vacío se cae. **Verificar antes de apoyar nada en él.**
- **Validación / magnitud:** no leídas. El resumen habla cualitativamente de "desempeño efectivo,
  convergencia fiable y adaptabilidad mejorada".
- **Consecuencia para la tesis:** si se confirma que no hay hardware, el hueco que deja es
  explícito, y una tesis que ejecute la idea sobre el TCLab físico aporta lo que le falta.
- **Nivel de lectura: [ABS]** (metadatos verificados en Crossref).

### 5.3 Yildiran (2023) — LQR adaptativo basado en RL sobre péndulo invertido

> Yildiran, U. (2023). *Adaptive Control of an Inverted Pendulum by a Reinforcement
> Learning-based LQR Method*. arXiv:2310.04436.

- **Proximidad: 3** — combina LQR y RL para control adaptativo sin modelo matemático explícito.
- **Planta/banco:** péndulo invertido; **no pude determinar si hay hardware o solo simulación**.
- **Resultado principal:** solo cualitativo en el resumen ("estabiliza muy rápido", "se adapta a
  cambios paramétricos en línea"). **Sin métricas.**
- **Nivel de lectura: [ABS]**. Marca `% PUBLICACION_NO_COMPROBADA`: **citable como preprint.**

### 5.4 Priess, Conway, Choi, Popovich y Radcliffe (2015) — el LQR inverso

*(Entrada nueva de la ronda 1. Resuelve parte de H-9d.)*

> Priess, M. C., Conway, R., Choi, J., Popovich, J. M., y Radcliffe, C. (2015). *Solutions to the
> Inverse LQR Problem With Application to Biological Systems Analysis*. **IEEE Transactions on
> Control Systems Technology**, 23(2), 770–777. DOI: 10.1109/TCST.2014.2343935

- **Proximidad: 3** — **LQR inverso**: dado un comportamiento observado, recuperar las matrices
  $Q$ y $R$ que lo hacen óptimo. Es el planteamiento clásico del eje (b), anterior al RL, y por
  tanto la referencia contra la que el eje (b) tiene que diferenciarse explícitamente.
- **Nivel de lectura: [META]** (Crossref). La descripción del problema inverso se deriva del título.

### 5.5 Control óptimo diferenciable: la tercera vía

*(Entradas nuevas de la ronda 1. Resuelven el resto de H-9d.)*

> Amos, B., Jimenez, I., Sacks, J., Boots, B., y Kolter, J. Z. (2018). *Differentiable MPC for
> End-to-end Planning and Control*. En **Advances in Neural Information Processing Systems 31
> (NeurIPS)**.

- **Proximidad: 3** — deriva a través de las condiciones KKT de la aproximación convexa para
  **aprender el costo y la dinámica** del controlador de extremo a extremo. Es la vía
  "diferenciable" de sintonizar el costo, alternativa al RL.
- **Nivel de lectura: [SERP]**. `% UNVERIFIED`: la forma exacta del nombre del segundo autor no
  está confirmada (algunos registros lo dan como "Ivan Dario Jimenez Rodriguez").

> *Infinite-Horizon Differentiable Model Predictive Control*. En **8th International Conference on
> Learning Representations (ICLR)**, 2020.

- **Proximidad: 3** — MPC lineal-cuadrático de horizonte infinito derivable, con **solución en
  forma cerrada de la derivada de la DARE asociada al LQR**. Es la conexión más directa entre el
  eje (b) y el LQR: permite derivar la ganancia $K$ respecto de $Q$ y $R$ sin agente de RL.
- **Nivel de lectura: [SERP]**. **`% UNVERIFIED` grave: no pude confirmar la lista de autores.**
  OpenReview devolvió una página de verificación de navegador y Crossref no indexa ICLR. En
  `references.bib` la entrada aparece **sin campo `author`, a propósito**: el apellido que circula
  en el encargo no proviene de una fuente que yo consultara y no lo escribo como dato.
  **No citar hasta completar el campo.**

### 5.6 Kiumarsi, Vamvoudakis, Modares y Lewis (2018) — la revisión desde el lado del control

*(Entrada nueva de la ronda 1.)*

> Kiumarsi, B., Vamvoudakis, K. G., Modares, H., y Lewis, F. L. (2018). *Optimal and Autonomous
> Control Using Reinforcement Learning: A Survey*. **IEEE Transactions on Neural Networks and
> Learning Systems**, 29(6), 2042–2062. DOI: 10.1109/TNNLS.2017.2773458

- **Proximidad: 4** — revisión del puente LQR–RL escrita **desde la comunidad de control**, no
  desde la de aprendizaje automático. Complementa a Recht (2019), que mira el mismo puente desde
  el otro lado. Ante un jurado de ingeniería de control, esta cita pesa más.
- **Nivel de lectura: [META]** (Crossref).

### Situación del eje (b)

La idea está **publicada y activa**, pero casi toda la evidencia es en simulación o en plantas
mecánicas rápidas. El análogo maduro es la sintonía de PID/MPC por RL (§3.1–§3.5), que sí tiene
hardware. **No encontré sintonía de $Q$/$R$ por RL sobre ningún proceso térmico ni sobre el TCLab.**

**Advertencia de la ronda 1:** este vacío **no** fue sometido a encadenamiento de citas. Descansa
todavía sobre búsqueda por palabras clave, igual que en la ronda 0. La vía natural para ponerlo a
prueba sería el encadenamiento hacia adelante desde Marco et al. (2016).

---

## 6. Eje (c): control clásico o barrera como filtro de seguridad sobre la acción del RL

### 6.0 Perkins y Barto (2002) — el precedente directo, y el más proporcionado al nivel

*(Entrada nueva de la ronda 1. Resuelve parte de H-9c.)*

> Perkins, T. J., y Barto, A. G. (2002). *Lyapunov Design for Safe Reinforcement Learning*.
> **Journal of Machine Learning Research**, 3, 803–832.

- **Proximidad: 3** — **es el precedente directo del eje (c)**, y con veinte años de anticipación
  sobre el resto de la literatura de esta sección. El agente aprende a controlar conmutando entre
  **controladores base diseñados con conocimiento de Lyapunov**, de modo que *cualquier* política de
  conmutación resulta segura y goza de garantías básicas de desempeño.
- **Por qué importa para una tesis de pregrado:** es la forma más antigua y más simple de "el
  controlador clásico como respaldo seguro del RL", y **no exige sintetizar una función barrera**.
  Es la ruta de menor carga teórica dentro de este eje.
- **Nivel de lectura: [SERP]**. `% UNVERIFIED`: el rango de páginas proviene de síntesis de
  búsqueda; no abrí `jmlr.org/papers/v3/perkins02a.html`, que sí apareció en los resultados.

### 6.1 Alshiekh et al. (2018) — shielding

> Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S., y Topcu, U. (2018). *Safe
> Reinforcement Learning via Shielding*. **Proceedings of the AAAI Conference on Artificial
> Intelligence**, 32(1), 2669–2678. DOI: 10.1609/aaai.v32i1.11797

- **Proximidad: 3** — origen del concepto de "escudo": un sistema reactivo sintetizado a partir
  de una especificación en lógica temporal que corrige la acción del agente cuando la viola.
- **Planta/banco:** dominios discretos; **no directamente transferible** a una planta continua
  con saturación como el TCLab.
- **Nivel de lectura: [META]** (AAAI OJS abierta; DOI y volumen confirmados). El rango de páginas
  lleva `% UNVERIFIED` en `references.bib`.

### 6.2 Ames, Xu, Grizzle y Tabuada (2017) — el CBF como programa cuadrático

*(Entrada nueva de la ronda 1. Resuelve parte de H-9c.)*

> Ames, A. D., Xu, X., Grizzle, J. W., y Tabuada, P. (2017). *Control Barrier Function Based
> Quadratic Programs for Safety Critical Systems*. **IEEE Transactions on Automatic Control**,
> 62(8), 3861–3876. DOI: 10.1109/TAC.2016.2638961

- **Proximidad: 4** — la referencia canónica del CBF formulado como programa cuadrático. Es la base
  sobre la que se apoya Cheng et al. (2019). Citarla es obligatorio si el eje (c) usa CBF.
- **Nivel de lectura: [META]** (Crossref).

### 6.3 Cheng, Orosz, Murray y Burdick (2019) — CBF como filtro y como guía de exploración

> Cheng, R., Orosz, G., Murray, R. M., y Burdick, J. W. (2019). *End-to-End Safe Reinforcement
> Learning through Barrier Functions for Safety-Critical Continuous Control Tasks*. **Proceedings
> of the AAAI Conference on Artificial Intelligence**, 33(1), 3387–3395.
> DOI: 10.1609/aaai.v33i01.33013387

- **Proximidad: 2** — arquitectura que combina un controlador RL libre de modelo con controladores
  basados en modelo que usan CBF, más aprendizaje en línea de la dinámica desconocida. Los CBF
  **no solo garantizan seguridad: acotan el conjunto de políticas explorables**, lo que acelera el
  aprendizaje. Ese doble papel es el argumento central del eje (c).
- **Proximidad por eje: (a)=4 · (b)=5 · (c)=2 · (d)=4**
- **Nivel de lectura: [ABS]** (AAAI OJS + resumen).

### 6.4 Wabersich y Zeilinger (2021) — filtro de seguridad predictivo

> Wabersich, K. P., y Zeilinger, M. N. (2021). *A predictive safety filter for learning-based
> control of constrained nonlinear dynamical systems*. **Automatica**, 129, 109597.
> DOI: 10.1016/j.automatica.2021.109597

- **Proximidad: 2** — la formulación más limpia del eje (c) para sistemas con restricciones: el
  filtro **convierte un sistema restringido en un sistema seguro no restringido**, al que se le
  puede aplicar cualquier algoritmo de RL "tal cual". Directamente aplicable a $u\in[0,100]\%$ y al
  límite térmico del TCLab.
- **Proximidad por eje: (a)=4 · (b)=5 · (c)=2 · (d)=4**
- **Costo:** esfuerzo computacional en línea. Con $T_s$ del orden de segundos en el TCLab,
  **no es un obstáculo**.
- **Nivel de lectura: [ABS]** (Crossref + resumen vía síntesis).

### 6.5 Zanon y Gros (2021) — RL seguro con MPC robusto

> Zanon, M., y Gros, S. (2021). *Safe Reinforcement Learning Using Robust MPC*. **IEEE
> Transactions on Automatic Control**, 66(8), 3638–3652. DOI: 10.1109/TAC.2020.3024161

- **Proximidad: 3** — garantías de estabilidad y seguridad cuando el RL ajusta un MPC robusto.
- **Nivel de lectura: [META]** (Crossref).

### 6.6 Berkenkamp, Turchetta, Schoellig y Krause (2017)

> Berkenkamp, F., Turchetta, M., Schoellig, A. P., y Krause, A. (2017). *Safe Model-based
> Reinforcement Learning with Stability Guarantees*. En **Advances in Neural Information
> Processing Systems 30 (NeurIPS)**.

- **Proximidad: 3** — ancla ya identificada en el perfil de dominio.
- **Nivel de lectura: [META]** — página de NeurIPS Proceedings confirmada; el rango de páginas
  lleva `% UNVERIFIED`. *(Ronda 1: se retira la descripción del método, que excedía el nivel.)*

### 6.7 Fernandez, Togashi, Hong y Yang (2020) — regiones LQR como certificado

> Fernandez, G. I., Togashi, C., Hong, D. W., y Yang, L. F. (2020). *Deep Reinforcement Learning
> with Linear Quadratic Regulator Regions*. arXiv:2002.09820.

- **Proximidad: 2** — cruza los ejes (a), (c) y el problema sim-to-real: redes neuronales con
  "desplazamiento de sesgo" que **conservan propiedades lineales en regiones concretas del espacio
  de estados**, de modo que el controlador aprendido pueda sintonizarse para parecerse a un LQR
  que se sabe estable para el sistema real. Resultado: **región de atracción estable garantizada
  para una política entrenada en simulación**.
- **Proximidad por eje: (a)=2 · (b)=4 · (c)=1 · (d)=4**
- **Planta/banco:** péndulo invertido con *swing-up*, con **transferencia de simulación a hardware
  real**.
- **Nivel de lectura: [ABS]** (página de arXiv abierta). Marca `% PUBLICACION_NO_COMPROBADA`:
  **citable como preprint.**

### 6.8 Revisiones de RL seguro

> García, J., y Fernández, F. (2015). *A comprehensive survey on safe reinforcement learning*.
> **Journal of Machine Learning Research**, 16(1), 1437–1480.

- **Proximidad: 3** — *(entrada nueva de la ronda 1)*. El survey canónico del campo; es la cita
  que ordena todo el eje (c) y la que un jurado espera ver.
- **Nivel de lectura: [SERP]**. `% UNVERIFIED`: páginas y número (JMLR no está en Crossref).

> Brunke, L., Greeff, M., Hall, A. W., Yuan, Z., Zhou, S., Panerati, J., y Schoellig, A. P.
> (2022). *Safe Learning in Robotics: From Learning-Based Control to Safe Reinforcement
> Learning*. **Annual Review of Control, Robotics, and Autonomous Systems**, 5(1), 411–444.
> DOI: 10.1146/annurev-control-042920-020211

- **Proximidad: 3** — revisión de referencia moderna del eje (c). **Nivel: [META]** (Crossref).

> Hewing, L., Wabersich, K. P., Menner, M., y Zeilinger, M. N. (2020). *Learning-Based Model
> Predictive Control: Toward Safe Learning in Control*. **Annual Review of Control, Robotics, and
> Autonomous Systems**, 3(1), 269–296. DOI: 10.1146/annurev-control-090419-075625

- **Proximidad: 4** — fondo. **Nivel: [META]** (Crossref).

### Situación del eje (c)

La literatura es **grande y madura**, pero está concentrada en robótica, conducción autónoma y
simulación. En procesos térmicos hay poco; **sobre TCLab: nada**. El riesgo de este eje no es el
solapamiento sino la **carga teórica** — con la salvedad, hallada en la ronda 1, de que Perkins y
Barto (2002) ofrece una ruta que no exige sintetizar un CBF.

**Advertencia:** este vacío **no** fue sometido a encadenamiento de citas. La vía natural sería el
encadenamiento hacia adelante desde Wabersich y Zeilinger (2021).

---

## 7. Eje (d): comparativo LQR vs RL

### 7.1 Estado general

Este eje es el **más poblado y el de menor novedad marginal**.

> Agyei, K., Sarhadi, P., y Polani, D. (2025). *Deep Reinforcement Learning in Applied Control:
> Challenges, Analysis, and Insights*. arXiv:2507.08196.

- **Proximidad: 3** — evalúa DDPG, TD3, PPO y TD-MPC2 frente a un controlador LQR/LQI en varios
  problemas de referencia, con análisis de márgenes de robustez.
- **Nivel de lectura: [ABS]** para el resumen. **No conseguí extraer el cuerpo del PDF**, de modo
  que las afirmaciones cuantitativas que la ronda 0 atribuía a este trabajo se retiraron.
  Marca `% PUBLICACION_NO_COMPROBADA`: **citable como preprint.**

> Dulac-Arnold, G., Levine, N., Mankowitz, D. J., Li, J., Paduraru, C., Gowal, S., y Hester, T.
> (2021). *Challenges of real-world reinforcement learning: definitions, benchmarks and
> analysis*. **Machine Learning**, 110(9), 2419–2468. DOI: 10.1007/s10994-021-05961-4

- **Proximidad: 3** — formaliza los desafíos que impiden desplegar RL en sistemas reales. Es la
  referencia para justificar por qué el entrenamiento sobre la placa es inviable y por qué la
  brecha sim-to-real debe medirse.
- **Nivel de lectura: [META]** (Crossref).

### 7.2 Comparativas en procesos térmicos (magnitudes: retiradas)

**Las cifras concretas que esta sección contenía fueron eliminadas en la ronda 1 de corrección
(hallazgo H-5).** Provenían de síntesis de resultados de búsqueda y se atribuían a "un controlador
PPO sobre intercambiador termoeléctrico" y a "un PID adaptativo con TD3", sin autor, año, título ni
DOI. Un número que el lector no puede rastrear hasta su fuente no tiene lugar en un entregable de
literatura, ni siquiera con advertencia: la advertencia se pierde al copiar la cifra, el número no.

Lo que sí se conserva, porque es la observación cualitativa que importa:

**Esta literatura reporta mejoras del orden de decenas de puntos porcentuales del RL frente a PID
en procesos térmicos, y esas magnitudes deben leerse con escepticismo.** La pregunta que el jurado
hará —y que la tesis debe anticipar— es si el PID o el LQR de referencia estaba bien sintonizado.
El perfil de dominio ya lo advierte ("comparación sesgada"); el informe del crítico lo señala como
la falla más frecuente y más invalidante en trabajos de este tipo.

Si la tesis necesita anclar expectativas numéricas, hay que localizar los artículos originales y
verificarlos. **Pendiente. El encadenamiento de citas de la ronda 1 se dirigió a los ejes (a) y a
la plataforma, no a estas comparativas; localizar sus fuentes sigue sin hacerse.**

### 7.3 Comparativas nombradas y verificadas

*(Sección nueva de la ronda 1. Resuelve H-10: la ronda 0 calificaba el eje de "saturado" nombrando
un solo estudio.)*

> Machacuay, J., e Ipanaqué, W. (2025). *DDPG and PNMPC controller design comparison for a
> Quadruple-tank process control benchmark*. **Optimization and Engineering**.
> DOI: 10.1007/s11081-025-09990-z

- **Proximidad: 3** — comparación de diseño entre DDPG y PNMPC sobre el benchmark de cuatro
  tanques. Universidad de Piura (Perú): cuenta también como literatura latinoamericana.
- **Nivel de lectura: [META]** (Crossref; volumen y páginas aún no expuestos).

> Machacuay, J., e Ipanaqué, W. (2024). *Zero-Shot DDPG Controller Design for Liquid Level Control
> of a Benchmark Quadruple-Tank Process*. En **2024 10th International Conference on Control,
> Decision and Information Technologies (CoDIT)**, pp. 1–6. DOI: 10.1109/CODIT62066.2024.10708234

- **Proximidad: 3** — *"zero-shot"* = entrenar en simulación y desplegar sin reentrenar. Es
  comparativa **y** sim-to-real a la vez, en una planta de procesos y por un grupo latinoamericano.
- **Nivel de lectura: [META]** (Crossref).

A estas se suman, ya listadas en §1.4, **Páez Ardila et al. (2022)** e **Insuasti et al. (2022)**,
ambas comparativas de controladores sobre el kit de laboratorio, y **Bloor et al. (2026, PC-Gym)**
en §2.3, que establece el protocolo de comparación justa RL vs oráculo NMPC.

### Situación del eje (d)

**Muy poblado en general, y sobre TCLab el nicho está ocupado por varios lados.** *(La ronda 0 decía
"saturado"; la calificación se ajusta a lo que la evidencia nombrada sostiene.)* No encontré ninguna
publicación que compare LQR contra RL sobre TCLab, pero sí NMPC vs DRL (§1.3), RL con PID implícito
(§1.2) y dos comparativas de controladores clásicos sobre el mismo kit (§1.4). El vacío es
estrecho: una comparación LQR vs DRL en esta planta corre el riesgo de leerse como el mismo trabajo
con otro par de controladores.

---

## 8. Puente teórico LQR ↔ RL (fondo obligatorio)

Estas entradas no compiten con la tesis; le dan sustento formal a la afirmación de que LQR y RL
son dos caras del mismo problema. Todas son **proximidad 4**.

> Bradtke, S. J., Ydstie, B. E., y Barto, A. G. (1994). *Adaptive linear quadratic control using
> policy iteration*. En **Proceedings of the 1994 American Control Conference**, vol. 3,
> pp. 3475–3479. DOI: 10.1109/ACC.1994.735224

- El origen histórico de la conexión entre iteración de políticas y control LQ adaptativo. Nota:
  Ydstie es ingeniero de procesos químicos — cita útil para conectar los dos mundos.
  **[META]** (Crossref).

> Fazel, M., Ge, R., Kakade, S. M., y Mesbahi, M. (2018). *Global Convergence of Policy Gradient
> Methods for the Linear Quadratic Regulator*. **ICML**, PMLR 80, pp. 1467–1476.

- Convergencia global del gradiente de políticas al óptimo del LQR pese a la no convexidad en $K$.
  Es la garantía que legitima usar RL sobre una estructura LQR. **[SERP]**, `% UNVERIFIED`.

> Tu, S., y Recht, B. (2018). *Least-Squares Temporal Difference Learning for the Linear Quadratic
> Regulator*. **ICML**, PMLR 80, pp. 5005–5014.

- Análisis en tiempo finito de cuántas muestras hacen falta para estimar la función de valor de
  una política estática. **Argumento para la inviabilidad del entrenamiento sobre hardware lento.**
  **[SERP]**, `% UNVERIFIED`.

> Dean, S., Mania, H., Matni, N., Recht, B., y Tu, S. (2020). *On the Sample Complexity of the
> Linear Quadratic Regulator*. **Foundations of Computational Mathematics**, 20(4), 633–679.
> DOI: 10.1007/s10208-019-09426-y

- Coarse-ID control: estimar modelo, estimar su error, diseñar el controlador con ambos. **Es el
  flujo que la tesis va a seguir** (identificación → LQR), con incertidumbre explícita.
  **[META]** (Crossref).

> Recht, B. (2019). *A Tour of Reinforcement Learning: The View from Continuous Control*. **Annual
> Review of Control, Robotics, and Autonomous Systems**, 2(1), 253–279.
> DOI: 10.1146/annurev-control-053018-023825

- Panorama del RL desde el control continuo, con el LQR como caso central. Lectura introductoria
  más apropiada para el marco teórico. **[META]** (Crossref).

> Mania, H., Guy, A., y Recht, B. (2018). *Simple random search of static linear policies is
> competitive for reinforcement learning*. En **NeurIPS 31**.

- Búsqueda aleatoria sobre políticas lineales estáticas iguala el estado del arte en benchmarks de
  locomoción. **Contraargumento incómodo y necesario**: si una política lineal basta, ¿para qué la
  red profunda? **[SERP]**, `% UNVERIFIED`.

> Lewis, F. L., y Vrabie, D. (2009). *Reinforcement learning and adaptive dynamic programming for
> feedback control*. **IEEE Circuits and Systems Magazine**, 9(3), 32–50.
> DOI: 10.1109/MCAS.2009.933854

- Puente clásico desde la comunidad de control. **[META]** (Crossref).

> Annaswamy, A. M. (2023). *Adaptive Control and Intersections with Reinforcement Learning*.
> **Annual Review of Control, Robotics, and Autonomous Systems**, 6(1), 65–93.
> DOI: 10.1146/annurev-control-062922-090153

- Sitúa el RL respecto al control adaptativo. Cita defensiva ante "¿esto no es control adaptativo
  con otro nombre?". **[META]** (Crossref).

---

## 9. Literaturas de método añadidas en la ronda 1

Estas tres subsecciones sostienen partes del argumento que el propio entregable construye y que en
la ronda 0 estaban sin respaldo bibliográfico.

### 9.1 Metodología de evaluación en RL profundo (resuelve H-9a)

`positioning.md` §4 hace del rigor experimental *el* margen de contribución del eje (d), y el perfil
de dominio exige N semillas con dispersión reportada. Sin estas dos citas, esa exigencia parece una
manía interna del proyecto en lugar del estándar del campo. Con ellas, es el estándar del campo.

> Henderson, P., Islam, R., Bachman, P., Pineau, J., Precup, D., y Meger, D. (2018). *Deep
> Reinforcement Learning That Matters*. **Proceedings of the AAAI Conference on Artificial
> Intelligence**, 32(1). DOI: 10.1609/aaai.v32i1.11694

- **Proximidad: 4** — el trabajo que documentó que los resultados de RL profundo varían de forma
  sustancial entre semillas y que las comparaciones basadas en pocas corridas no son fiables.
- **Nivel de lectura: [META]** (Crossref). `% UNVERIFIED`: rango de páginas.

> Agarwal, R., Schwarzer, M., Castro, P. S., Courville, A. C., y Bellemare, M. G. (2021). *Deep
> Reinforcement Learning at the Edge of the Statistical Precipice*. En **NeurIPS 34**,
> pp. 29304–29320.

- **Proximidad: 4** — propone reportar **estimaciones por intervalo** del desempeño agregado,
  perfiles de desempeño y métricas robustas como la media intercuartílica, en lugar de estimaciones
  puntuales, precisamente en el régimen de pocas corridas en que va a estar esta tesis.
- **Nivel de lectura: [SERP]**. `% UNVERIFIED`: páginas y forma exacta de la lista de autores.

### 9.2 LQG, observador y acción integral (resuelve H-9e)

Requisito estructural, no adorno. El TCLab mide dos temperaturas de una planta 2×2 cuya dinámica
real es de orden superior: si el vector de estado elegido no se mide por completo, **el LQR por
realimentación de estados exige un observador**. Y el LQR es un **regulador**, mientras que todo el
proyecto habla de seguimiento de setpoint: hace falta la formulación servo o con acción integral.

> Kalman, R. E. (1960). *A New Approach to Linear Filtering and Prediction Problems*. **Journal of
> Basic Engineering**, 82(1), 35–45. DOI: 10.1115/1.3662552

- **Proximidad: 4** — el filtro de Kalman. **Obra distinta del artículo del LQR del mismo año y
  autor**; en `references.bib` van con claves separadas y hay un aviso para no fusionarlas.
- **Nivel de lectura: [META]** (Crossref).

> Luenberger, D. G. (1971). *An introduction to observers*. **IEEE Transactions on Automatic
> Control**, 16(6), 596–602. DOI: 10.1109/TAC.1971.1099826

- **Proximidad: 4** — el observador determinista, alternativa más simple al filtro de Kalman si el
  ruido de sensor no se modela estocásticamente. **Nivel: [META]** (Crossref).

> Tan, W., Han, W., y Xu, J. (2022). *State-Space PID*. **IEEE Access**, 10, 116540–116553.
> (Ya listada en §1.4.)

- Relevante aquí porque conecta la línea base clásica con la formulación en espacio de estados.

> Manurung, A., Kristiana, L., y Aryanta, D. (2021). *An Energy Balance Model Parameter Estimation
> with an Extended Kalman Filter*. **IFAC-PapersOnLine**, 54(20), 735–740.
> DOI: 10.1016/j.ifacol.2021.11.259

- **Proximidad: 3** — *(hallazgo de la ronda 1, vía encadenamiento de citas desde Park 2020)*.
  Es lo más cercano a un **observador aplicado a esta plataforma** que encontré.
- **Nivel de lectura: [META]** (Crossref). **Advertencia:** que el banco sea el TCLab lo *infiero*
  de que cita a Park (2020) y del título; **no leí el resumen y no está confirmado.** Verificar
  antes de apoyarse en ello.

**Laguna reconocida:** no añadí un texto de referencia sobre LQG/LQI (Anderson y Moore ya está en
la semilla, sin verificar; Åström y Wittenmark o Franklin, Powell y Emami-Naeini serían candidatos).
No los verifiqué en esta ronda y por tanto no los incluyo.

### 9.3 Sim-to-real: anclas metodológicas (resuelve H-9b)

La ronda 0 justificó la omisión de esta literatura diciendo que "está concentrada en robótica". Eso
es un enunciado sobre el dominio de aplicación, no una razón para omitir el método que el proyecto
propone usar.

> Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., y Abbeel, P. (2017). *Domain
> randomization for transferring deep neural networks from simulation to the real world*. En
> **IROS 2017**, pp. 23–30. DOI: 10.1109/IROS.2017.8202133

- **Proximidad: 4** — origen del término *domain randomization*. Su versión original es **visual**
  (texturas, iluminación), no dinámica. **Nivel: [META]** (Crossref).

> Peng, X. B., Andrychowicz, M., Zaremba, W., y Abbeel, P. (2018). *Sim-to-Real Transfer of
> Robotic Control with Dynamics Randomization*. En **ICRA 2018**, pp. 3803–3810.
> DOI: 10.1109/ICRA.2018.8460528

- **Proximidad: 3** — **es la variante pertinente para el TCLab**: aleatorizar los parámetros
  **dinámicos** (capacidad térmica, coeficiente de convección, retardo), no la apariencia.
  Si la tesis entrena en simulador y despliega en la placa, esta es la cita del método.
- **Nivel: [META]** (Crossref).

> Zhao, W., Peña Queralta, J., y Westerlund, T. (2020). *Sim-to-Real Transfer in Deep
> Reinforcement Learning for Robotics: a Survey*. En **IEEE SSCI 2020**, pp. 737–744.
> DOI: 10.1109/SSCI47803.2020.9308468

- **Proximidad: 4** — survey de encuadre. **Nivel: [META]** (Crossref).

---

## 10. Literatura iberoamericana (resuelve H-9f)

La ronda 0 declaró este eje vacío **sin nombrar dónde había buscado**, que es exactamente lo que un
vacío no puede permitirse. El detalle completo de dónde se buscó está en `frontier_map.md` §6.
Resumen de lo hallado:

| Trabajo | Sede | Verificación |
|---------|------|-------------|
| Rico-Azagra, Gil-Martínez y Nájera-Canal (2024) | *Jornadas de Automática* 45 (CEA, España) | Crossref, con DOI |
| Rico-Azagra y Gil-Martínez (2021) | XLII Jornadas de Automática, pp. 275–281 | Crossref, con DOI |
| Insuasti, Paredes y Camacho (2022) | IEEE ETCM (Ecuador) | Crossref |
| Páez Ardila et al. (2022) | IEEE LA-CCI | Crossref |
| Machacuay e Ipanaqué (2024, 2025) | CoDIT; *Optimization and Engineering* (U. de Piura, Perú) | Crossref |

Todas con **nivel de lectura [META]**.

**Lo que NO se encontró, y dónde no se buscó bien.** No localicé ningún trabajo **colombiano** sobre
TCLab, ni ningún trabajo iberoamericano que aplique **LQR** a esta plataforma. Pero **no consulté
los buscadores propios de RIAI ni las actas del CLCA**, que están mal indexadas en Crossref y
OpenAlex. Ese resultado **no debe leerse como ausencia**: es una laguna de esta búsqueda.

---

## 11. Tabla consolidada de proximidad condicionada al eje

*(Resuelve H-12. Solo entradas de proximidad general 1 o 2. El escalar general es el mínimo del
vector.)*

| Obra | General | (a) Residual | (b) Sintonía $Q,R$ | (c) Filtro | (d) Comparativo |
|------|---------|--------------|--------------------|------------|-----------------|
| Patel (2023 / 2022) | **1** | 2 | 3 | 2 | **1** |
| Soza Mamani y Prado Romo (2025) | **1** | 3 | **1** | 2 | **1** |
| Park et al. (2020) | 2 | 3 | 3 | 3 | **2** |
| Holt y Armellin (2025) | 2 | **1** | 3 | **1** | 4 |
| Alqithami (2026) | 2 | **1** | 4 | 2 | 4 |
| Zhang et al. (2026) | 2 | 3 | **1** | 5 | 4 |
| Fernandez et al. (2020) | 2 | 2 | 4 | **1** | 4 |
| Marco et al. (2016) | 2 | 4 | **2** | 5 | 4 |
| Cheng et al. (2019) | 2 | 4 | 5 | **2** | 4 |
| Wabersich y Zeilinger (2021) | 2 | 4 | 5 | **2** | 4 |
| Lawrence et al. (2022) | 2 | 3 | **2** | 4 | 3 |
| Bloor et al. (2025, CIRL) | 2 | **2** | 3 | 4 | 3 |
| APMonitor RLTCLab (no publicado) | 2 | 3 | 3 | 3 | **2** |

**Cómo leerla.** Bajo el eje (a) hay **tres competidores de proximidad 1** (Holt y Armellin,
Alqithami, y Fernandez muy cerca en 2); bajo el (b), **dos** (Soza Mamani, Zhang); bajo el (c),
**dos** (Holt y Armellin, Fernandez); bajo el (d), **dos** (Patel, Soza Mamani). Ningún eje está
libre de competencia directa; lo que varía es dónde está y sobre qué planta.

---

## 12. Ejes de búsqueda que quedaron vacíos o casi vacíos

| Eje solicitado | Estado tras la ronda 1 | Método de la evidencia |
|----------------|------------------------|------------------------|
| **LQR sobre TCLab (publicado)** | **VACÍO** | **Encadenamiento de citas**: 84 obras citantes de Park et al. (2020), cero coincidencias |
| **RL residual sobre proceso térmico** | **VACÍO** | **Encadenamiento**: 97 obras citantes + 100 registros del corpus, cero coincidencias |
| **RL residual en control de procesos** | **NO VACÍO** *(corregido)* | Alqithami (2026) |
| **Sintonía de $Q$/$R$ por RL sobre hardware térmico** | **VACÍO** | Solo palabras clave — **no sometido a encadenamiento** |
| **CBF / filtro de seguridad sobre TCLab** | **VACÍO** | Solo palabras clave — **no sometido a encadenamiento** |
| **Sim-to-real específico de TCLab** | **VACÍO** | Solo palabras clave — **no sometido a encadenamiento** |
| **Literatura iberoamericana** | **NO VACÍO** *(corregido)* | 5 trabajos verificados; RIAI y CLCA sin consultar |
| **RL sobre TCLab (general)** | **POBLADO PERO ESCASO** | Cuatro trabajos (era dos en la ronda 0) |
| **Comparativo RL vs control clásico** | **MUY POBLADO** | Seis comparativas nombradas (era una) |

**Advertencia sobre la interpretación de los vacíos.** Un eje vacío puede ser una oportunidad o
puede ser señal de que la comunidad no considera la pregunta interesante. Para el TCLab, la
explicación más probable es que es una plataforma **docente** y que los grupos que publican control
avanzado usan bancos con más grados de libertad. Eso no invalida la tesis —el nivel es de pregrado
y la reproducibilidad de una plataforma de 3000 unidades es un activo— pero sí significa que **la
contribución no puede sostenerse solo en la novedad de la plataforma**.

**Advertencia añadida en la ronda 1.** De los cinco vacíos de la ronda 0, **dos cambiaron** al
someterlos a encadenamiento de citas. Tres no fueron sometidos a esa prueba. Es razonable esperar
que también se estrechen si se hace.

---

## 13. Advertencias de calibración para el uso de esta bibliografía

1. **Es un trabajo de pregrado.** Furieri et al. (§4.4), Fazel et al. (§8) y Wabersich y Zeilinger
   (§6.4) se citan para *encuadrar y acotar el alcance*, no para replicarse. Decir "no ofrecemos
   garantía formal de estabilidad para la componente aprendida; véase Furieri et al. (2024) para el
   estado del arte en esa dirección" es una posición honesta y defendible.
2. **La medición de la brecha sim-to-real en el TCLab parece no estar publicada**, y ahora tiene
   anclas metodológicas (§9.3). Es una contribución empírica limpia y proporcionada al nivel,
   *independientemente de qué variante se elija*.
3. **Nada sustituye leer los textos completos de §1.2, §1.3, §4.6 y §5.2.** Son los cuatro
   artículos que determinan el margen real de contribución.

---

## 14. Cambios de la ronda 1

Ronda 1 de 3. Puntaje de entrada: **72/100**. Umbral: 80.
**Quién hizo qué:** el coordinador resolvió H-7, H-6, H-3, H-4, H-5 y H-2 antes de devolverme el
trabajo; yo hice el resto. Se marca en cada línea.

| # | Hallazgo | Quién | Qué se hizo |
|---|----------|-------|-------------|
| **H-1** | Entradas `[META]` que exceden su nivel | **librarian** | Se leyeron los resúmenes de **Reiter et al.** y **Furieri et al.** y se elevó su nivel a `[ABS]`. Se abrió la página de **APMonitor** y se creó el nivel `[WEB]`. Se **recortaron** las afirmaciones excesivas en Johannink (§4.2), McClement (§3.2) y Berkenkamp (§6.6). Se añadió a §0 la regla explícita de qué puede afirmar una entrada `[META]`. |
| **H-2** | "Zhang: solo simulación" sin hedge | coordinador | Hedge aplicado en los tres documentos, con nota de que la afirmación es load-bearing. Conservado. |
| **H-3** | Cinco entradas `VERIFICADO` con evidencia SERP | coordinador | Degradadas a `% UNVERIFIED`; criterio de grado de evidencia añadido a la convención. **El librarian añadió una sexta**: `Haarnoja2018_sac` llevaba sello VERIFICADO con el mismo grado de evidencia que Fazel y Tu-Recht; se degradó por coherencia. |
| **H-4** | Uso laxo de `% UNVERIFIED` | coordinador | Estado `% PUBLICACION_NO_COMPROBADA` creado; los cuatro preprints quedaron citables. Conservado. |
| **H-5** | Magnitudes sin fuente | coordinador | Cifras eliminadas de §7.2 y de `frontier_map.md` §4; advertencia cualitativa conservada. El librarian añadió en §7.2 la nota de que localizar esas fuentes **sigue pendiente**. |
| **H-6** | Colisiones de clave BibTeX | coordinador | Sección de reconciliación añadida. **El librarian añadió el apartado D-bis**: las dos obras de Kalman de 1960 son distintas y no deben fusionarse. Se verificó que ninguna de las 20 claves nuevas colisiona. |
| **H-7** | Tokens de herramienta | coordinador | Eliminados de los cinco archivos. No reintroducidos. |
| **H-8** | Sin encadenamiento de citas | **librarian** | Tres búsquedas de citas hacia adelante vía **OpenAlex**, con procedimiento documentado en `frontier_map.md` §5: Silver (52 citantes), Johannink (45), Park et al. (84), más un barrido del corpus completo de RL residual (187 registros). **Dos vacíos sostenidos, dos corregidos, uno ampliado.** Hallazgos nuevos: Patel (2022), Alqithami (2026), Manurung et al. (2021), Tan et al. (2022), Páez Ardila et al. (2022), Rico-Azagra (2021, 2024). Se declara la limitación de cobertura de OpenAlex frente a Google Scholar. |
| **H-9a** | Evaluación en RL profundo ausente | **librarian** | Henderson et al. (2018) y Agarwal et al. (2021) añadidos (§9.1) y conectados con el protocolo de semillas en `positioning.md` §0 y `frontier_map.md` §4. |
| **H-9b** | Sim-to-real sin ancla | **librarian** | Tobin (2017), Peng (2018) y Zhao et al. (2020) añadidos (§9.3), señalando que la variante pertinente es la aleatorización de **dinámica**, no la visual. |
| **H-9c** | Eje (c) sin anclas seminales | **librarian** | Ames et al. (2017), García y Fernández (2015) y **Perkins y Barto (2002)** añadidos. Este último se destaca como la ruta de menor carga teórica del eje (c). **Discrepancia parcial: no añadí Achiam et al. (CPO) ni la rama CMDP/Lagrangianos** — ver nota abajo. |
| **H-9d** | Eje (b) mal documentado | **librarian** | Priess et al. (2015, LQR inverso), Amos et al. (2018), el trabajo de ICLR 2020 sobre MPC diferenciable de horizonte infinito, y Kiumarsi et al. (2018) añadidos (§5.4–§5.6). |
| **H-9e** | Cero cobertura de LQG/observador/LQI | **librarian** | §9.2 nueva: Kalman (1960, filtro), Luenberger (1971), Tan et al. (2022), Manurung et al. (2021). Añadido como **requisito estructural** en `positioning.md` §0, puntos 3 y 4. Laguna reconocida: falta un texto de referencia verificado de LQG/LQI. |
| **H-9f** | Iberoamericana sin decir dónde se buscó | **librarian** | §10 nueva y `frontier_map.md` §6, con **tabla de dónde se buscó**, incluidos los sitios donde no se buscó bien (RIAI, CLCA). Cinco trabajos verificados. El vacío era de la búsqueda, no del campo. |
| **H-10** | Eje (d) "saturado" con un solo estudio | **librarian** | Calificación cambiada de "saturado" a **"muy poblado"**, con seis comparativas nombradas y verificadas (§7.3 y `frontier_map.md` §4). |
| **H-11** | Elaboración asimétrica hacia el eje (a) | **librarian** | `positioning.md` reescrito: superlativos evaluativos sustituidos por descriptores; **los cuatro ejes reciben ahora contrafáctico operativo, "riesgo específico" y "pregunta del jurado más difícil"**; tabla §5 ampliada con filas comparables para los cuatro. |
| **H-12** | Proximidad escalar única | **librarian** | Vector de cuatro proximidades para las 13 entradas de proximidad 1 y 2, con tabla consolidada en §11. |

### Discrepancias con el informe del crítico

**Una sola, y es parcial: H-9c.** El crítico pide también la rama CMDP/Lagrangianos (Achiam et al.,
CPO 2017). **No la añadí, y la razón no es olvido.** El eje (c) tal como el estudiante lo formuló es
*"el LQR o una barrera actúa como filtro de seguridad sobre la acción del RL"* — un mecanismo
**externo** que corrige o veta la acción. La rama CMDP resuelve un problema distinto: incorpora la
restricción **dentro del objetivo de optimización** mediante multiplicadores de Lagrange, sin filtro
externo y sin garantía por episodio. Es una alternativa al eje (c), no un componente suyo. Añadirla
como si fuera parte del eje habría inflado el conteo de referencias sin ayudar a la decisión del
estudiante, que es el propósito de este entregable. **Si el orquestador considera que el mapa debe
cubrir también las alternativas al eje (c) y no solo sus componentes, la añado en la ronda 2** —
pero entonces correspondería listarla en `positioning.md` §6, junto a CIRL y a la optimización
bayesiana, que es donde viven las opciones que el estudiante no listó.

En todo lo demás el informe me parece correcto, y dos hallazgos me parecen especialmente bien
vistos: **H-8**, porque el encadenamiento efectivamente cambió dos de los cinco vacíos y uno de
ellos era el que yo había llamado "el más limpio de los cuatro"; y **H-11**, porque la asimetría
existía y yo no la veía.

### Lo que sigue sin hacerse

1. Encadenamiento de citas para los ejes **(b)** y **(c)** y para la brecha sim-to-real. Vías
   naturales: Marco et al. (2016) y Wabersich y Zeilinger (2021).
2. Localizar las fuentes de las magnitudes retiradas en §7.2.
3. Completar el campo `author` de la entrada de ICLR 2020 sobre MPC diferenciable, o eliminarla.
4. Un texto de referencia verificado sobre LQG/LQI.
5. Consultar RIAI y las actas del CLCA en sus propios buscadores.
6. Leer los textos completos de Patel (2023), Soza Mamani y Prado Romo (2025), Alqithami (2026) y
   Zhang et al. (2026).
