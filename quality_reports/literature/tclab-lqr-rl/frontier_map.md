# Mapa de la frontera — LQR + aprendizaje por refuerzo sobre TCLab

**Proyecto:** tclab-lqr-rl · **Fecha:** 2026-09-07 · **Revisado:** 2026-09-08 (ronda 1)
**Agente:** librarian

Este documento responde a una sola pregunta: **para cada una de las cuatro formas de combinar LQR
y RL que el estudiante está considerando, ¿qué está hecho, qué está saturado y qué está vacío?**

No recomienda ninguna. La decisión es del estudiante en la entrevista de descubrimiento.

> **Cambio de la ronda 1.** La versión anterior sostenía los cinco vacíos declarados únicamente
> sobre búsqueda por palabras clave. Esta versión añade la **§5, Evidencia del encadenamiento de
> citas**, con tres búsquedas de citas hacia adelante y su procedimiento. Dos vacíos sobreviven
> reforzados, uno se estrecha y uno se corrige. Los cambios están marcados en su sitio.

---

## 0. Resumen en una tabla

| Eje | Qué es | Densidad de la literatura general | Densidad **sobre TCLab** | Vacío más claro |
|-----|--------|-----------------------------------|--------------------------|-----------------|
| **(a)** RL residual sobre política base LQR | $u = -Kx + \pi_\theta(x)$ | **Alta** en robótica; **una sola obra** en control de procesos (Alqithami 2026) | **VACÍA** | RL residual sobre un proceso térmico de laboratorio |
| **(b)** RL sintoniza $Q$ y $R$ | El agente elige los pesos del costo | **Media**, casi toda en simulación o plantas mecánicas rápidas | **VACÍA** | Sintonía de $Q$/$R$ validada en hardware térmico lento |
| **(c)** LQR o barrera como filtro de seguridad | El controlador clásico corrige o veta la acción del RL | **Alta** en robótica y control con restricciones | **VACÍA** | Filtro de seguridad sobre planta térmica de laboratorio con saturación |
| **(d)** Comparativo LQR vs RL | Estudio de desempeño lado a lado | **Muy poblada** (ver §4 para la documentación) | **Ocupada por trabajo adyacente** (NMPC vs DRL, 2025; PID/DMC/Fuzzy, 2022) | Ninguno limpio |

---

## 1. Eje (a) — RL residual sobre una política base LQR

### Qué está hecho

**El método está establecido y tiene nombre propio.** Dos artículos fundacionales lo definen:
Silver et al. (2018) lo formaliza como $a = \mu(s) + \pi_\theta(s)$ y sostiene que aprender el
residuo requiere mucha menos exploración que aprender desde cero; Johannink et al. (2019) lo
valida en manipulación robótica. Ishihara et al. (2023) lo aplica sobre un PID en cascada de un
quadcopter para rechazar viento — que es, estructuralmente, la misma historia que "residual sobre
LQR para rechazar corrientes de aire y deriva térmica en el TCLab".

**El campo es grande y crece rápido.** La consulta a OpenAlex por `"residual reinforcement
learning"` en título o resumen devuelve **187 registros** (§5.3). Los cien más recientes son de
2025–2026. Esto matiza la impresión de la ronda 0: no es un método de nicho, es una técnica de uso
corriente.

**La versión con garantías también existe, y ahora está leída.** Furieri et al. (2024) parametriza
controladores de refuerzo de desempeño sobre un sistema ya estable. El resumen, **leído
directamente en arXiv en esta ronda**, dice literalmente: *"we guarantee $L_p$ closed-loop
stability even if optimization is halted prematurely, and even when the ground-truth dynamics are
unknown"*. El mecanismo es una sinergia entre el principio de *Internal Model Control* no lineal y
métodos de optimización sin restricciones para aprender dinámicas estables. El resumen habla de
*"several numerical experiments"* y **no nombra ninguna planta**: es simulación, sin hardware
declarado. Holt y Armellin (2025) publican en *IEEE T-RO* algo cuyo título es casi el enunciado del
eje: RL que mejora un LQR, con funciones de Lyapunov de control como certificado.

**En control de procesos ahora sí hay algo, y es de 2026.** *(Corrección de la ronda 1.)*
Alqithami (2026), en *Journal of Process Control*, presenta **AgentTwin**: un banco de gemelo
digital multiagente con **control regulatorio residual** sobre el Tennessee Eastman Process y un
**escudo de seguridad resuelto por solver**. Es la única obra del corpus de 187 registros situada en
control de procesos químicos, y combina los ejes (a) y (c). La versión anterior de este documento
afirmaba que en procesos no había nada residual; **eso era incorrecto** y se corrige aquí.

Distinto de lo anterior, Bloor et al. (2025, CIRL) inyectan estructura PID *dentro* de la
arquitectura de la política profunda. No suma un residuo a la acción del controlador: usa el
controlador como sesgo inductivo de la red. Distinguirlo con precisión importa para no reclamar
novedad que no corresponde.

**Tendencia de 2026 que la ronda 0 no vio.** Entre los cien registros más recientes del corpus
residual aparecen, por título, al menos cuatro trabajos que combinan residuo con seguridad:
*Provably Safe Residual Reinforcement Learning Using Tube MPC*; *Safety-Filtered Residual
Reinforcement Learning over Model Predictive Control*; *MPC-Informed Residual Reinforcement
Learning for Hybrid Control*; *Conflict-driven Adaptive Scaling for Safe Residual Reinforcement
Learning*. **El campo se está moviendo hacia (a)×(c).** No verifiqué ninguno de estos cuatro más
allá del título que devuelve OpenAlex; no tienen entrada en `references.bib`.

### Qué está saturado

La aplicación de RL residual a **manipulación robótica**. Está agotada como contribución. A la vista
del corpus de 2026, también empiezan a estarlo la navegación de drones y el control de vehículos.

### Qué está vacío

**No encontré ningún trabajo de RL residual sobre un proceso térmico de laboratorio, ni sobre el
TCLab.** El vacío sobrevive al encadenamiento de citas (§5.1) y a la revisión del corpus completo
(§5.3), pero es **más estrecho** de lo que decía la ronda 0: ya no es "nada en control de procesos",
sino "nada en procesos térmicos de laboratorio, y una sola obra en control de procesos químicos".

**Vacío secundario, quizá más interesante:** no encontré ningún trabajo que use un LQR como
política base residual *y* mida la brecha sim-to-real de la corrección aprendida. Fernandez et al.
(2020) está cerca — usa regiones LQR como certificado para transferir de simulación a hardware —
pero la planta es un péndulo y el LQR no es la política base, es el certificado.

### Qué NO se puede reclamar

- "Nadie ha hecho RL residual." Falso: es una línea establecida desde 2018 y muy activa en 2026.
- "Nadie ha combinado RL con LQR." Falso: Holt y Armellin (2025), Fernandez et al. (2020),
  Yildiran (2023).
- "No hay RL residual en control de procesos." Falso desde 2026: Alqithami.
- Lo único defendible es la **combinación planta + método**: residual sobre LQR, en TCLab, con
  medición honesta de la degradación sim-to-real.

### El contrafáctico operativo de este eje

*(Los cuatro ejes llevan uno, del mismo grano — véase la nota de equilibrio en `positioning.md`.)*

El LQR se diseña sobre un modelo *lineal*; el TCLab es no lineal (radiación $\propto T^4$). Si el
residuo hace lo que se dice que hace, **su aportación debe crecer con la distancia al punto de
linealización**. Diseño: evaluar en setpoints cercanos y lejanos al punto de diseño y comprobar si
la mejora crece. Si no crece, el residuo está compensando una mala sintonía del LQR, no la no
linealidad, y el resultado no sostiene la afirmación.

---

## 2. Eje (b) — El RL sintoniza las matrices de costo $Q$ y $R$

### Qué está hecho

**La pregunta está formalizada y publicada.** Zhang et al. (2026, *Mathematics*) propone
exactamente esta arquitectura: un meta-agente de alto nivel optimiza adaptativamente $Q$ y $R$
mediante evaluación de trayectorias basada en entropía, mientras un agente de bajo nivel ejecuta
iteración de políticas libre de modelo. Es la referencia más directa del eje y es de este año.

**Existe una alternativa competidora, más eficiente y con hardware.** Marco et al. (2016, ICRA)
resuelve el mismo problema con **optimización bayesiana** (Entropy Search) sobre un brazo robótico
de 7 GDL. Es más eficiente en muestras que el RL, que es precisamente la restricción dominante en
una planta cuyas constantes de tiempo son de minutos.

**Y existe el planteamiento clásico, anterior al RL.** *(Añadido en la ronda 1.)* Priess et al.
(2015, *IEEE TCST*) resuelve el **problema LQR inverso**: dado un comportamiento observado,
recuperar las matrices $Q$ y $R$ que lo hacen óptimo. Es la formulación que el eje (b) reinventa en
lenguaje de aprendizaje, y por tanto la referencia contra la que tiene que diferenciarse
explícitamente.

**La vía diferenciable es una tercera opción.** *(Añadida en la ronda 1.)* Amos et al. (2018,
NeurIPS) deriva a través de las condiciones KKT para aprender el costo del controlador de extremo a
extremo; el trabajo de ICLR 2020 sobre MPC diferenciable de horizonte infinito da una **solución en
forma cerrada de la derivada de la DARE asociada al LQR**, que permite derivar la ganancia $K$
respecto de $Q$ y $R$ sin RL. *(De esa entrada no pude confirmar la lista de autores; véase la nota
en `references.bib`.)*

**El análogo con PID/MPC es maduro y con hardware.** Lawrence et al. (2022, *CEP*) convierte el
PID en la política entrenable y lo valida sobre un sistema de tanques físico. McClement et al.
(2022, *JPC*) entrena meta-RL offline y transfiere. Gros y Zanon (2020, *IEEE TAC*) demuestra
formalmente que un esquema basado en modelo puede sintonizarse para entregar la política óptima
del sistema real **incluso con un modelo equivocado** — el argumento teórico más fuerte a favor de
este eje cuando el modelo lineal identificado del TCLab es imperfecto.

**La revisión desde la comunidad de control existe.** *(Añadida en la ronda 1.)* Kiumarsi et al.
(2018, *IEEE TNNLS*) revisa control óptimo y autónomo mediante RL desde el lado del control, no del
aprendizaje automático. Ante un jurado de ingeniería, esta cita pesa más que Recht (2019).

### Qué está saturado

La sintonía de **PID** por RL. Hay decenas de artículos, muchos con líneas base dudosas.

### Qué está vacío

**Sintonía de $Q$ y $R$ por RL validada sobre hardware térmico.** Nadie lo ha hecho sobre TCLab.

Sobre Zhang et al. (2026): su resumen habla de pruebas en sistemas lineales y **no menciona
hardware**, pero no leí el artículo y la ausencia de mención en el resumen no prueba la ausencia de
experimento. **Esta afirmación es load-bearing** — sobre ella descansa el vacío de este eje — y
debe confirmarse leyendo el artículo, que es de acceso abierto en MDPI.

**Vacío conceptual adicional:** no encontré ningún trabajo que compare, sobre la misma planta,
*sintonía de $Q$/$R$ por RL* contra *sintonía de $Q$/$R$ por optimización bayesiana* o contra *LQR
inverso*. Ese es exactamente el contrafáctico que un jurado exigiría, y no está resuelto.

### El contrafáctico operativo de este eje

Si el objetivo es elegir dos o cuatro números ($Q$ y $R$ diagonales para un sistema 2×2), y cada
evaluación cuesta una corrida de minutos con enfriamiento posterior, la pregunta es **por qué RL y
no una búsqueda en malla, un algoritmo genético, optimización bayesiana o LQR inverso**. Diseño que
la responde: ejecutar **dos brazos sobre la misma planta y el mismo presupuesto de corridas** — RL
frente a optimización bayesiana — y reportar desempeño alcanzado *en función del número de
evaluaciones consumidas*. Si el RL no gana a igualdad de presupuesto, ese es el resultado, y es
publicable. Marco et al. (2016) y Priess et al. (2015) existen precisamente porque esta pregunta
tiene respuestas clásicas.

---

## 3. Eje (c) — LQR o barrera como filtro de seguridad sobre la acción del RL

### Qué está hecho

**Es el eje con la literatura más grande y mejor consolidada de los cuatro.** Cuatro familias:

1. **El precedente histórico, y el más proporcionado a un pregrado.** *(Añadido en la ronda 1.)*
   Perkins y Barto (2002, *JMLR*) construyen agentes que **conmutan entre controladores base
   diseñados con conocimiento de Lyapunov**, de modo que *cualquier* política de conmutación resulta
   segura y goza de garantías básicas de desempeño. Es la forma más antigua y más simple de "el
   controlador clásico como respaldo seguro del RL" y **no exige sintetizar un CBF**.
2. **Escudos lógicos** — Alshiekh et al. (2018, AAAI): sintetizar un sistema reactivo a partir de
   una especificación en lógica temporal que corrige la acción cuando viola la especificación.
   Concebido para dominios discretos; su transferencia a una planta continua con saturación no es
   inmediata.
3. **Funciones barrera de control (CBF)** — Ames et al. (2017, *IEEE TAC*) es la referencia
   canónica del CBF como programa cuadrático *(añadida en la ronda 1)*; Cheng et al. (2019, AAAI)
   la lleva al RL y muestra que los CBF no solo garantizan seguridad, **acotan el conjunto de
   políticas explorables y con ello aceleran el aprendizaje**. Ese doble papel es el argumento
   central que el eje (c) puede reclamar más allá de la seguridad.
4. **Filtros predictivos** — Wabersich y Zeilinger (2021, *Automatica*): el filtro convierte un
   sistema restringido en uno no restringido al que se aplica cualquier RL "tal cual". Resuelve
   una optimización en cada paso; en el TCLab, con $T_s$ del orden de segundos, el costo
   computacional **no es un obstáculo**.

**La variante que usa el LQR mismo como certificado existe.** Fernandez et al. (2020) construye
redes con desplazamiento de sesgo que conservan propiedades lineales en regiones concretas del
espacio de estados, de modo que el controlador aprendido se sintoniza para parecerse a un LQR
conocido y estable. Resultado: **región de atracción garantizada para una política entrenada en
simulación**, con transferencia a hardware. Es lo más cercano a "el LQR actúa como filtro".

**Las revisiones están hechas:** García y Fernández (2015, *JMLR*) es el survey canónico del campo
*(añadido en la ronda 1)*; Brunke et al. (2022, *ARCRAS*) para RL seguro en robótica; Hewing et al.
(2020, *ARCRAS*) para MPC basado en aprendizaje.

### Qué está saturado

La aplicación de CBF a robótica, conducción autónoma y benchmarks de simulación. Proponer un CBF
nuevo no es viable en un trabajo de pregrado y tampoco es necesario.

### Qué está vacío

**Filtros de seguridad sobre plantas térmicas de laboratorio.** Encontré aplicaciones a
refrigeración distrital y a control de edificios, ambas a escala de sistema, no de banco de
pruebas. **Sobre TCLab: nada.**

### El riesgo real de este eje no es el solapamiento, es la carga técnica

La propia literatura reconoce que **sintetizar un CBF no es directo y exige conocimiento de
dominio considerable**. Para el TCLab, la restricción de seguridad es doble: saturación del
actuador ($u \in [0,100]\%$, trivial de imponer por recorte) y límite térmico (requiere un modelo
predictivo de la evolución de $T$, que ya es un filtro predictivo tipo Wabersich–Zeilinger). Un
recorte de saturación **no es un filtro de seguridad** y no debe presentarse como tal.

### El contrafáctico operativo de este eje

Un filtro que nunca interviene no es evidencia de nada. Diseño que lo pone a prueba: **entrenar y
evaluar la misma política con filtro y sin filtro**, sobre el mismo perfil de setpoints y de
perturbaciones, y reportar (i) número de intervenciones del filtro por corrida, (ii) número de
violaciones del límite térmico en cada condición, y (iii) curvas de aprendizaje de ambas, para
contrastar la afirmación de Cheng et al. (2019) de que el filtro *acelera* el aprendizaje. Si el
filtro no interviene nunca, hay que forzar la condición — agente deliberadamente agresivo o
perturbación adversa — y decirlo.

---

## 4. Eje (d) — Estudio comparativo LQR vs RL

### Qué está hecho — con los trabajos nombrados

*(La ronda 0 calificaba este eje de "saturado" nombrando un solo estudio. El crítico objetó, con
razón, que una impresión no documentada estaba cerrando una de las cuatro opciones del estudiante.
Aquí van los trabajos concretos; la calificación se ajusta de "saturado" a **"muy poblado"**, que
es lo que la evidencia sostiene.)*

Comparativas de control clásico frente a RL, o entre controladores, con datos verificados:

- **Agyei et al. (2025, arXiv:2507.08196)** — evalúa DDPG, TD3, PPO y TD-MPC2 frente a un
  controlador **LQR/LQI**, incluyendo márgenes de ganancia y de retardo, no solo IAE. Es la
  comparativa más directamente pertinente al eje. *No leí el PDF*: no pude extraer su cuerpo.
- **Machacuay e Ipanaqué (2025, *Optimization and Engineering*)** — comparación de diseño entre
  **DDPG y PNMPC** sobre el benchmark de cuatro tanques. Grupo de la Universidad de Piura (Perú).
- **Machacuay e Ipanaqué (2024, CoDIT)** — DDPG *zero-shot* (entrenar en simulación, desplegar sin
  reentrenar) sobre el mismo benchmark. Es comparativa **y** sim-to-real a la vez.
- **Páez Ardila et al. (2022, IEEE LA-CCI)** — comparativa de **PID, DMC y Fuzzy PD+I** sobre un kit
  de laboratorio de control. Hallado por encadenamiento de citas desde Park et al. (2020).
- **Insuasti et al. (2022, IEEE ETCM)** — controladores y compensadores clásicos comparados
  **sobre TCLab**.
- **Bloor et al. (2026, PC-Gym)** — establece el protocolo de comparación justa RL vs oráculo NMPC
  y reporta que existen brechas de desempeño a favor del NMPC.

Y la referencia que explica por qué estas comparaciones son difíciles de hacer bien:
**Dulac-Arnold et al. (2021, *Machine Learning*)**, que formaliza los nueve desafíos del RL en
sistemas reales.

### El problema específico de este eje

**Sobre el TCLab, el nicho comparativo ya está ocupado por trabajo adyacente**, y por más de un
lado. Soza Mamani y Prado Romo (2025, *Processes*) publicaron NMPC vs DDPG vs TD3 **sobre TCLab
físico**; Insuasti et al. (2022) y Páez Ardila et al. (2022) publicaron comparativas de
controladores clásicos sobre el mismo kit. Una tesis que compare LQR vs DDPG sobre TCLab corre el
riesgo de leerse como el mismo trabajo con otro par de controladores. La diferencia tendría que
argumentarse con algo distinto de *qué* se compara.

### Dónde queda margen

El margen no está en *qué se compara* sino en **cómo se compara** — y ahora ese "cómo" tiene
respaldo bibliográfico propio, que la ronda 0 no aportaba. **Henderson et al. (2018, AAAI)**
documentó que los resultados de RL profundo varían de forma sustancial entre semillas y que las
comparaciones basadas en pocas corridas son poco fiables; **Agarwal et al. (2021, NeurIPS)**
propone reportar **estimaciones por intervalo** del desempeño agregado, perfiles de desempeño y
métricas robustas como la media intercuartílica, en lugar de estimaciones puntuales. Con esas dos
citas, el protocolo que el perfil de dominio exige deja de ser una manía interna del proyecto y
pasa a ser el estándar del campo:

- media ± desviación estándar sobre N corridas declaradas,
- N semillas independientes en RL con dispersión reportada,
- temperatura ambiente inicial registrada por corrida,
- esfuerzo de control reportado, no solo error de seguimiento,
- LQR base sintonizado con el mismo esfuerzo que el agente,
- ninguna diferencia declarada relevante si es menor que la dispersión entre corridas.

Las mejoras que reporta esta literatura frente a PID son de decenas de puntos porcentuales, y
resultan sospechosas precisamente porque esos protocolos no se aplicaron. (Las cifras concretas que
esta sección citaba se retiraron en la ronda 1: no tenían fuente rastreable — ver §7.2 de la
bibliografía anotada.) **Una comparación metodológicamente rigurosa que concluya "no hay diferencia
significativa" sería un resultado legítimo a nivel de trabajo de grado**, pero el estudiante debe
entrar sabiendo que ese puede ser el resultado.

### El contrafáctico operativo de este eje

La comparación solo es informativa si el LQR puede perder por una razón identificable. Diseño:
evaluar ambos controladores **dentro y fuera del rango de linealización**, y con el modelo
deliberadamente desajustado (por ejemplo, identificado a una temperatura ambiente distinta de la de
evaluación). Si el RL solo gana fuera del punto de diseño, eso *explica* la diferencia; si gana
igual en todas partes, lo más probable es que el LQR esté mal sintonizado y la comparación no valga.

---

## 5. Evidencia del encadenamiento de citas

*(Sección nueva de la ronda 1. Resuelve H-8. La ronda 0 sostenía los vacíos solo con búsqueda por
palabras clave; el crítico señaló que las dos pruebas decisivas no se habían hecho.)*

### Herramienta y procedimiento

Usé la **API de OpenAlex** (`api.openalex.org`), no Google Scholar. Procedimiento, idéntico en los
tres casos:

1. Resolver el DOI de la obra semilla a un identificador OpenAlex:
   `api.openalex.org/works/doi:<DOI>?select=id,title,cited_by_count`
2. Listar **todas** las obras citantes:
   `api.openalex.org/works?filter=cites:<ID>&per-page=100&select=title,publication_year,type&sort=publication_year:desc`
3. Leer la lista completa de títulos y clasificarlos manualmente por dominio de aplicación.

**Limitación que hay que declarar, y es seria.** Los recuentos de OpenAlex para estas obras son
notablemente más bajos que los de Google Scholar. Johannink et al. (2019) aparece con 45 obras
citantes, cuando en Google Scholar supera con holgura esa cifra. La causa probable es doble:
OpenAlex separa el registro de arXiv del registro de actas IEEE, y su cobertura de las listas de
referencias de actas IEEE es incompleta. **En consecuencia, la evidencia negativa de esta sección
es más débil de lo que sugiere su aparente exhaustividad.** No prueba que no exista el trabajo; sí
prueba que no aparece en el grafo de citas de OpenAlex, que es una fuente sustancialmente más amplia
que la búsqueda por palabras clave que se usó en la ronda 0.

### 5.1 Citas hacia adelante de Silver et al. (2018) — *Residual Policy Learning*

- **ID OpenAlex:** W2905364877 · **Obras citantes: 52** · **Revisadas: 52 (todas)**
- **Filtro aplicado:** lectura de los 52 títulos, buscando control de procesos, plantas térmicas,
  reactores, intercambiadores, columnas o cualquier proceso continuo.
- **Resultado: cero coincidencias.** El conjunto es íntegramente robótica (manipulación, inserción
  industrial, agarre, destreza en mano), navegación, conducción autónoma y tenis de mesa.
- Lo más cercano a teoría de control: *Combining Model-Based and Model-Free Methods for Nonlinear
  Control: A Provably Convergent Policy Gradient Approach* (2020) y *Bayesian controller fusion:
  Leveraging control priors in deep reinforcement learning for robotics* (2023). Ninguno es proceso
  térmico. También aparece *Adaptive Control of a Mechatronic System Using Constrained Residual
  Reinforcement Learning* (2022): mecatrónica, no procesos.

### 5.2 Citas hacia adelante de Johannink et al. (2019) — *Residual RL for Robot Control*

- **ID OpenAlex:** W2904746163 · **Obras citantes: 45** · **Revisadas: 45 (todas)**
- **Filtro aplicado:** el mismo.
- **Resultado: cero coincidencias.** Ensamblaje aeronáutico, manipulación, apertura de puertas,
  semáforos, compensación de movimiento buque-a-buque, óptica adaptativa, planificación en HPC.
- Lo más cercano a un proceso continuo: *Deep reinforcement learning-based jet control for tandem
  cylinders* (2025), que es mecánica de fluidos, no control de procesos.

**Conclusión conjunta de 5.1 y 5.2:** de **97 obras citantes revisadas** de los dos artículos
fundacionales del RL residual, **ninguna aplica el método a un proceso térmico ni a control de
procesos**. El vacío del eje (a) sobre plantas térmicas queda sostenido por algo más que
palabras clave.

### 5.3 Barrido del corpus completo de RL residual

Prueba complementaria, independiente del grafo de citas:
`filter=title_and_abstract.search:"residual reinforcement learning"` → **187 registros**; revisé
por título los ~100 más recientes (2025–2026, orden descendente por año).

- **Una sola obra en control de procesos:** Alqithami (2026), *Journal of Process Control* —
  AgentTwin, control regulatorio residual sobre el Tennessee Eastman Process con escudo de
  seguridad. **Corrige la afirmación de la ronda 0** de que no había residual en control de procesos.
- Adyacentes, sin ser control de procesos: gestión energética de edificios, convertidores DC-DC de
  carga rápida, bombeo hidráulico, regulación de bus DC en sistemas fotovoltaicos.
- Todo lo demás: robótica, humanoides, drones, vehículos, tráfico, ejecución financiera, LLM.
- **Tendencia dominante en 2026: residual + seguridad** (Tube MPC, filtros de seguridad, escalado
  adaptativo). Ver §1.

### 5.4 Citas hacia adelante de Park et al. (2020) — el artículo de referencia del TCLab

- **ID OpenAlex:** W2998862960 · **Obras citantes: 84** · **Revisadas: 84 (todas)**
- **Filtro aplicado:** lectura de los 84 títulos buscando (i) mención de LQR, control óptimo,
  espacio de estados o realimentación de estados; (ii) RL sobre esta plataforma; (iii) literatura
  iberoamericana.

**Resultado (i) — LQR sobre TCLab: cero coincidencias.** Ningún título entre los 84 menciona LQR,
regulador lineal cuadrático ni control óptimo. **El vacío "LQR sobre TCLab" queda sostenido por la
prueba que el crítico pedía.** Lo más cercano son tres trabajos que sí tocan el espacio de estados
y la estimación:

- *State-Space PID: A Missing Link Between Classical and Modern Control* (Tan et al., 2022, *IEEE
  Access*) — puente PID ↔ espacio de estados. **Verificado, en `references.bib`.**
- *An Energy Balance Model Parameter Estimation with an Extended Kalman Filter* (Manurung et al.,
  2021, *IFAC-PapersOnLine*) — lo más parecido a un **observador** sobre esta plataforma.
  **Verificado, en `references.bib`.** Advertencia: que el banco sea el TCLab lo *infiero* de que
  cita a Park (2020) y del título; no leí el resumen.
- *An Energy Balance Model for a Small Educational Thermal Device* (2021) — no verificado.

**Resultado (ii) — RL sobre TCLab: cuatro trabajos, uno de ellos nuevo y relevante.**

- *Safe, Fast and Explainable Online Reinforcement Learning for Continuous Process Control* (Patel,
  2022, IEEE AdCONIP, pp. 54–60) — **versión de congreso precursora del artículo de 2023 de Patel**,
  mismo autor. No había aparecido en ninguna búsqueda por palabras clave. **Verificado.**
- *Integrating Model Predictive Control with Deep Reinforcement Learning…* (Soza Mamani y Prado
  Romo, 2025) — ya identificado en la ronda 0.
- *A practical Reinforcement Learning implementation approach…* (Patel, 2023) — ya identificado.
- *iTCLab PID Control Tuning Using Deep Learning* (2023) y *Deep Transfer Learning for Approximate
  Model Predictive Control* (2023) — no verificados, solo título.

**Resultado (iii) — literatura iberoamericana: existe y es sustancial** (ver §6).

### 5.5 Qué cambió y qué no

| Vacío declarado en la ronda 0 | Estado tras el encadenamiento |
|---|---|
| LQR sobre TCLab | **SOSTENIDO.** Cero coincidencias en las 84 obras citantes de Park et al. (2020). |
| RL residual sobre proceso térmico | **SOSTENIDO.** Cero coincidencias en 97 obras citantes + 100 registros del corpus. |
| "No hay RL residual en control de procesos" | **CORREGIDO.** Alqithami (2026), *J. Process Control*. |
| Literatura iberoamericana "no encontrada" | **CORREGIDO.** Existe; ver §6. El vacío era de la búsqueda, no del campo. |
| RL sobre TCLab: "dos artículos" | **AMPLIADO a cuatro**, uno de ellos precursor de Patel (2023). |

---

## 6. Literatura iberoamericana: dónde busqué y qué encontré

*(Sección nueva de la ronda 1. Resuelve H-9f. La ronda 0 declaró este eje vacío sin nombrar dónde
había buscado, que es exactamente lo que un vacío no puede permitirse.)*

### Dónde busqué

| Fuente | Cómo | Resultado |
|--------|------|-----------|
| Grafo de citas de Park et al. (2020) vía OpenAlex | 84 títulos revisados | **5 trabajos iberoamericanos** |
| Crossref, consulta bibliográfica en español | Títulos completos en español | Confirmó 2 con DOI |
| Búsqueda web: repositorios institucionales de trabajos de grado en Colombia | "TCLab control temperatura trabajo de grado universidad Colombia LQR" | **Nada de una universidad colombiana.** Sí apareció un trabajo español (Universidad de Sevilla) sobre control predictivo del TCLab, y repositorios de código de autores hispanohablantes. |
| RIAI (*Revista Iberoamericana de Automática e Informática Industrial*) | Búsqueda por nombre de revista junto a TCLab | **Sin coincidencias localizadas.** No consulté el buscador propio de la revista: es una laguna de esta búsqueda, no un vacío del campo. |
| Actas del CLCA (Congreso Latinoamericano de Control Automático) | Búsqueda por nombre del congreso | **Sin coincidencias localizadas.** Las actas del CLCA no están bien indexadas en Crossref ni en OpenAlex; **este resultado no debe leerse como ausencia**. |

### Qué encontré

- **Rico-Azagra, Gil-Martínez y Nájera-Canal (2024)**, *Jornadas de Automática* 45 — nueva
  plataforma de control de temperatura de bajo coste para educación en ingeniería de control.
  Verificado en Crossref con DOI. *Jornadas de Automática* es el congreso anual del Comité Español
  de Automática.
- **Rico-Azagra y Gil-Martínez (2021)**, XLII Jornadas de Automática, pp. 275–281 — rediseño de esa
  plataforma. Verificado con DOI.
- **Insuasti, Paredes y Camacho (2022)**, IEEE ETCM (Ecuador) — ya estaba en la ronda 0.
- **Páez Ardila et al. (2022)**, IEEE LA-CCI — comparativa PID/DMC/Fuzzy sobre kit de laboratorio.
- **Machacuay e Ipanaqué (2024, 2025)**, Universidad de Piura (Perú) — DDPG sobre benchmark de
  cuatro tanques, incluyendo variante *zero-shot* sim-to-real.

Además, entre las 84 obras citantes de Park aparecen por título, sin verificar: *Uso del paradigma
Take-Home Labs para la enseñanza del control automático en estudios de ingeniería* (2021),
*Introducing Data Science to Spanish Speaker Students Using the TCLab Arduino Kit* (2024) y *Use of
TCLab kits for control engineering curricula at the University of Almería* (2022).

### Lectura para el jurado colombiano

Hay una comunidad iberoamericana activa alrededor de estas plataformas: España (Rioja, Almería),
Ecuador, Perú, Brasil. **No localicé ningún trabajo colombiano sobre TCLab**, y tampoco ningún
trabajo iberoamericano que aplique LQR a esta plataforma. Con la salvedad de que RIAI y CLCA no
fueron consultados en sus propios buscadores, ese sigue siendo el hueco regional.

---

## 7. Lo que atraviesa los cuatro ejes: la brecha sim-to-real en el TCLab

Este no es uno de los cuatro ejes, pero **aparece como vacío en los cuatro**.

El perfil de dominio establece que entrenar RL sobre la placa es inviable por el número de
episodios, de ahí la necesidad del simulador y del análisis sim-to-real. Ahora bien:

- **Patel (2023)** resuelve el problema **evitando el simulador**: RL online directamente sobre
  el proceso, con reducción de dimensionalidad y exploración modificada. No mide brecha sim-to-real
  porque no hay simulación.
- **Soza Mamani y Prado Romo (2025)** valida experimentalmente sobre TCLab, pero el resumen no
  declara medición de degradación simulador → hardware.
- **Fernandez et al. (2020)** sí mide y garantiza transferencia, pero sobre un péndulo invertido.
- **Machacuay e Ipanaqué (2024)** hace *zero-shot* de simulación a benchmark, pero sobre cuatro
  tanques, no sobre TCLab. *(Añadido en la ronda 1.)*

**No encontré ninguna medición publicada de la brecha sim-to-real sobre el TCLab.** Si eso se
confirma leyendo los textos completos, es una contribución empírica limpia, proporcionada al nivel
de un trabajo de grado, y **compatible con cualquiera de las cuatro variantes**.

**El método ahora tiene anclas.** *(Añadidas en la ronda 1.)* Tobin et al. (2017) es el origen del
término *domain randomization*, aunque su versión original es visual. La variante pertinente aquí es
**Peng et al. (2018, ICRA)**: aleatorizar la **dinámica** (parámetros físicos — capacidad térmica,
coeficiente de convección, retardo), no la textura. Zhao, Peña Queralta y Westerlund (2020) es el
survey. La justificación que daba la ronda 0 para omitir esta literatura ("está concentrada en
robótica") era un enunciado sobre el dominio de aplicación, no una razón para omitir el método.

---

## 8. Riesgo de scooping — trabajos que hay que leer antes de decidir

| Trabajo | Por qué es riesgo | Ejes afectados |
|---------|-------------------|----------------|
| **Soza Mamani y Prado Romo (2025)**, *Processes* 13(6):1627 | TCLab hardware + control óptimo predictivo + DDPG/TD3 + comparación. El trabajo publicado más cercano al conjunto del proyecto. | (b), (c), (d) sobre todo |
| **Patel (2023)**, *Comput. Chem. Eng.* 174:108232, **y su precursor de congreso Patel (2022)**, IEEE AdCONIP, pp. 54–60 | RL sobre TCLab hardware con conocimiento de dominio incorporado. Ocupa el nicho "RL práctico sobre TCLab". *(El precursor se añadió en la ronda 1.)* | (a), (d) |
| **Alqithami (2026)**, *J. Process Control* | Residual + escudo de seguridad sobre Tennessee Eastman. Única obra residual en control de procesos. *(Añadido en la ronda 1.)* | (a), (c) |
| **Zhang et al. (2026)**, *Mathematics* 14(5):895 | Formaliza el eje (b): meta-agente que optimiza $Q$ y $R$. Presumiblemente solo simulación — **no verificado**. | (b) |
| **Holt y Armellin (2025)**, *IEEE T-RO* 41:5117–5129 | "RL Enhanced LQR + CLF": el enunciado del eje (a) cruzado con el (c), en otra planta. | (a), (c) |
| **APMonitor, tutorial RLTCLab** | No es publicación. **Corrección de la ronda 1:** abrí la página. Usa DDPG en PyTorch con entorno Gymnasium, y por defecto corre sobre `tclab.TCLabModel()`, es decir **el simulador**, con el hardware como opción comentada. El solapamiento es con la parte de simulación, no con la experimental. | todos |

**De estos, ninguno fue leído en texto completo.** Los cuatro primeros están tras muro de pago.
Conseguirlos por la biblioteca de la Universidad Distrital es prerrequisito para decidir el eje.

---

## 9. Ejes de búsqueda solicitados que quedaron vacíos

| Búsqueda solicitada | Resultado tras la ronda 1 |
|---------------------|---------------------------|
| LQR sobre TCLab (publicación revisada por pares) | **Nada.** Sostenido por el encadenamiento de citas (§5.4): cero coincidencias en 84 obras citantes. Lo más cercano: Tan et al. (2022) sobre PID en espacio de estados y Manurung et al. (2021) sobre estimación con EKF. |
| RL residual sobre proceso **térmico** | **Nada.** Sostenido por §5.1–§5.3. |
| RL residual en control de **procesos** | **CORREGIDO: existe.** Alqithami (2026). |
| Sintonía de $Q$/$R$ por RL sobre hardware térmico | **Nada.** No sometido a encadenamiento de citas; sigue apoyado solo en palabras clave. |
| Safe RL / CBF sobre TCLab | **Nada.** No sometido a encadenamiento de citas. |
| Medición de brecha sim-to-real en TCLab | **Nada.** No sometido a encadenamiento de citas. |
| Domain randomization en control de procesos térmicos | **Casi nada.** En control de procesos el tema aparece bajo la etiqueta *transfer learning* (Lin et al., 2024) o *zero-shot* (Machacuay e Ipanaqué, 2024), no *domain randomization*. |
| Literatura iberoamericana | **CORREGIDO: existe.** Ver §6. Sin trabajos colombianos localizados; RIAI y CLCA no consultados en sus buscadores propios. |

**Advertencia sobre la interpretación de los vacíos.** Un eje vacío puede ser una oportunidad o
puede ser una señal de que la comunidad no considera la pregunta interesante. Para el TCLab
específicamente, la explicación más probable es que es una plataforma **docente** y que los grupos
que publican control avanzado usan bancos con más grados de libertad. Eso no invalida la tesis
—el nivel es de pregrado y la reproducibilidad de una plataforma de 3000 unidades es un activo—
pero sí significa que **la contribución no puede sostenerse solo en la novedad de la plataforma**.

**Advertencia añadida en la ronda 1.** Tres de los vacíos de la tabla anterior **no** fueron
sometidos a encadenamiento de citas: los ejes (b) y (c) sobre TCLab, y la brecha sim-to-real.
Descansan todavía sobre búsqueda por palabras clave, igual que en la ronda 0. Dado que dos de los
cinco vacíos originales cambiaron al aplicarles el encadenamiento, **es razonable esperar que estos
tres también se estrechen si se someten a la misma prueba**. La vía natural sería el encadenamiento
hacia adelante desde Marco et al. (2016) para el eje (b) y desde Wabersich y Zeilinger (2021) para
el eje (c).
