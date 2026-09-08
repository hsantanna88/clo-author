# Posicionamiento — las cuatro variantes, sin recomendación

**Proyecto:** tclab-lqr-rl · **Fecha:** 2026-09-07 · **Revisado:** 2026-09-08 (ronda 1)
**Agente:** librarian

> **Este documento no recomienda una variante.** Esa decisión es del estudiante en la entrevista
> de descubrimiento. Lo que se entrega aquí es el mapa: para cada variante, cuán poblada está la
> literatura, qué haría distinta a una tesis situada ahí, qué riesgo de solapamiento tiene, qué
> contrafáctico experimental la pondría a prueba, y qué pregunta del jurado sería la más difícil de
> responder.

> **Nota de equilibrio (ronda 1).** El crítico observó que la versión anterior cumplía la letra de
> la neutralidad pero no su espíritu: reservaba superlativos evaluativos al eje (a) ("el más
> limpio", "el más despejado"), le daba un contrafáctico operativo completo que ningún otro eje
> recibía, y colocaba subsecciones adversas solo en (b), (c) y (d). Tenía razón. En esta versión:
> los superlativos evaluativos se sustituyen por descriptores comparables; **los cuatro ejes
> reciben un contrafáctico operativo del mismo grano**; y los cuatro reciben una subsección
> "riesgo específico" y una "pregunta del jurado más difícil". Si la evidencia favorece a alguno,
> debe verse en los hechos de la tabla §5, no en el vocabulario.

---

## 0. Lo que las cuatro variantes comparten

### Obligaciones comunes (no son contribución, son requisito)

1. Identificación de un modelo lineal en espacio de estados del TCLab, con datos de identificación
   y de validación provenientes de **corridas distintas** (Ljung; perfil de dominio).
2. Verificación de controlabilidad y observabilidad antes de diseñar el LQR.
3. **Observador.** El TCLab mide dos temperaturas de una planta 2×2 cuya dinámica real es de orden
   superior. Si el vector de estado elegido no se mide por completo, hace falta un observador
   (Luenberger 1971) o un filtro de Kalman (Kalman 1960b), y hay que decirlo explícitamente. En el
   entorno de esta plataforma existe ya un precedente de estimación: Manurung et al. (2021), con
   EKF sobre un modelo de balance de energía. *(Requisito añadido en la ronda 1.)*
4. **Seguimiento, no regulación.** El LQR es un **regulador**: lleva el estado a cero. Todo el
   proyecto habla de seguir un setpoint. Hace falta la formulación servo — LQR con acción integral
   (LQI), o error aumentado, o prealimentación de referencia — y hay que declarar cuál se usa. Tan
   et al. (2022) conecta explícitamente PID y espacio de estados y es un puente útil desde la línea
   base clásica. *(Requisito añadido en la ronda 1.)*
5. Declaración y justificación de $T_s$; diseño del LQR **en discreto**.
6. Tratamiento explícito de la saturación $u \in [0,100]\%$.
7. LQR base sintonizado con el mismo esfuerzo que el agente de RL.
8. Métricas sobre hardware como media ± desviación estándar sobre N corridas declaradas; N semillas
   en RL con dispersión reportada; temperatura ambiente inicial registrada por corrida. Este
   protocolo **es el estándar del campo, no una manía del proyecto**: Henderson et al. (2018)
   documentó la variabilidad entre semillas en RL profundo, y Agarwal et al. (2021) propone
   reportar estimaciones por intervalo y métricas robustas en lugar de estimaciones puntuales.
   *(Respaldo bibliográfico añadido en la ronda 1.)*
9. Resolución de la colisión de notación $Q$ (peso del LQR) vs $Q_1,Q_2$ (potencias) — INV-7.

### Activo común disponible para las cuatro

**La medición de la brecha sim-to-real sobre el TCLab parece no estar publicada.** Cualquiera de
las cuatro variantes puede incorporarla como resultado propio. Es la contribución empírica más
proporcionada al nivel del trabajo y la más difícil de disputar, porque no depende de que el
método sea novedoso sino de que la medición sea honesta. El método tiene anclas: Peng et al. (2018)
para aleatorización de la **dinámica** —que es la variante pertinente aquí, no la visual de Tobin
et al. (2017)—, y Zhao et al. (2020) como survey.

### Riesgo común

Los artículos que definen el margen real —Patel (2023) y su precursor Patel (2022), Soza Mamani y
Prado Romo (2025), Zhang et al. (2026), Alqithami (2026)— **no fueron leídos en texto completo**.
La mayoría están tras muro de pago. **Cualquier afirmación de novedad hecha antes de leerlos es
especulación.**

---

## 1. Variante (a) — RL residual sobre política base LQR

$$u_k = -K x_k + \pi_\theta(x_k)$$

### Cuán poblada está esta literatura

**Alta en general, vacía en el nicho térmico.**

- El método está establecido desde 2018 (Silver et al.; Johannink et al. 2019) y es de uso
  corriente: el corpus de OpenAlex para `"residual reinforcement learning"` tiene **187 registros**,
  con fuerte concentración en 2025–2026.
- La versión con garantías de estabilidad existe y es técnicamente exigente (Furieri et al. 2024:
  estabilidad $\mathcal{L}_p$ en lazo cerrado incluso con parada prematura de la optimización).
- En control de procesos hay **una** obra residual: Alqithami (2026), sobre Tennessee Eastman, con
  escudo de seguridad. *(Hallazgo de la ronda 1; la ronda 0 afirmaba que no había ninguna.)*
- **En procesos térmicos de laboratorio: nada. En TCLab: nada.** Sostenido por revisión de 97 obras
  citantes y 100 registros del corpus (`frontier_map.md` §5).

### Qué haría distinta a una tesis situada aquí

- **La planta.** Residual sobre LQR en un proceso térmico MIMO 2×2 con acoplamiento cruzado,
  retardo de transporte y no linealidad por radiación. La literatura residual vive en robótica,
  donde la dinámica es rápida y el problema de sensor es otro.
- **El objetivo del residuo es declarable y falsable.** El LQR se diseña sobre un modelo lineal; el
  TCLab no lo es. El residuo tiene una tarea concreta: recuperar el desempeño que el LQR pierde
  fuera del punto de linealización.
- **Permite acotar honestamente la garantía de estabilidad**, remitiendo a Furieri et al. (2024)
  como estado del arte que el trabajo no alcanza.

### Contrafáctico operativo

Evaluar en setpoints cercanos y lejanos al punto de diseño y comprobar si **la mejora del residuo
crece con la distancia**. Si crece, la explicación causal es la no linealidad. Si es plana, lo más
probable es que el residuo esté compensando una sintonía deficiente del LQR, y entonces el
resultado no sostiene la afirmación. Barrido previo de sintonías del LQR para fijar el mejor
baseline alcanzable.

### Riesgo específico de este eje

**El residuo puede convertirse en el controlador.** Si $\pi_\theta$ no está acotado en magnitud,
puede dominar a $-Kx$ y el sistema deja de ser "LQR + corrección" para ser "RL con una condición
inicial afortunada". Hay que fijar y declarar la cota del residuo, y reportar qué fracción de la
acción total aporta cada término. Sin eso, la contribución del LQR es decorativa y el jurado lo verá.

Riesgo secundario: Holt y Armellin (2025) publicaron "RL Enhanced LQR" en *IEEE T-RO* y Alqithami
(2026) publicó residual + escudo en *J. Process Control*. Hay que leerlos y diferenciarse
explícitamente.

### La pregunta del jurado más difícil

> *"Si el residuo mejora el desempeño, ¿cómo sabe que la mejora viene del residuo y no de que su
> LQR estaba mal sintonizado?"*

---

## 2. Variante (b) — El RL sintoniza $Q$ y $R$

### Cuán poblada está esta literatura

**Media, con dos competidores metodológicos no basados en RL.**

- La formalización directa existe y es de este año: Zhang et al. (2026), meta-agente que optimiza
  $Q$ y $R$ sobre un agente base de iteración de políticas.
  **Hedge obligatorio:** su resumen habla de pruebas en sistemas lineales y no menciona hardware,
  pero **no leí el artículo**, y la ausencia de mención en el resumen no prueba ausencia de
  experimento. Esta afirmación es load-bearing para el vacío de este eje. Confirmar (MDPI, acceso
  abierto).
- **Competidor 1:** Marco et al. (2016, ICRA) resuelve el mismo problema con **optimización
  bayesiana** sobre hardware robótico, con mucha mejor eficiencia muestral.
- **Competidor 2:** Priess et al. (2015, *IEEE TCST*) plantea el **LQR inverso**: recuperar $Q$ y
  $R$ a partir del comportamiento observado. Es el planteamiento clásico del problema.
  *(Añadido en la ronda 1.)*
- **Vía diferenciable:** Amos et al. (2018) y el trabajo de ICLR 2020 sobre MPC diferenciable de
  horizonte infinito, que da la derivada en forma cerrada de la DARE. *(Añadida en la ronda 1.)*
- El análogo con PID/MPC es maduro y con hardware: Lawrence et al. (2022), McClement et al. (2022),
  Gros y Zanon (2020). La revisión desde la comunidad de control es Kiumarsi et al. (2018).
- **En hardware térmico: nada. En TCLab: nada.**

### Qué haría distinta a una tesis situada aquí

- **Hardware donde la literatura tiene simulación.** Ejecutar la idea sobre una placa física, con
  corridas de minutos y enfriamiento entre ellas, aporta lo que a Zhang et al. (2026) le falta —
  si se confirma que efectivamente le falta.
- **El contrafáctico que nadie ha hecho.** No hay ningún trabajo que compare, sobre la misma planta,
  sintonía de $Q$/$R$ por RL contra optimización bayesiana o contra LQR inverso.
- **El argumento de Gros y Zanon (2020)** da sustento teórico: con un modelo imperfecto —y lo será—
  los pesos aprendidos pueden recuperar desempeño que el LQR nominal pierde.

### Contrafáctico operativo

Ejecutar **dos o tres brazos sobre la misma planta y el mismo presupuesto de corridas** — RL,
optimización bayesiana y (opcionalmente) búsqueda en malla — y reportar el desempeño alcanzado
**en función del número de evaluaciones consumidas**, no solo el desempeño final. Si el RL no gana
a igualdad de presupuesto, ese es el resultado y es publicable: convierte al competidor incómodo en
el segundo brazo del experimento en lugar de en la objeción del jurado.

### Riesgo específico de este eje

**El costo experimental es el más alto de los cuatro.** Cada evaluación del objetivo es una corrida
completa más el tiempo de enfriamiento; un presupuesto realista puede ser de decenas de
evaluaciones, no de miles. Eso puede bastar para optimización bayesiana y ser insuficiente para RL,
lo que sesga el experimento antes de empezar. Hay que dimensionar el presupuesto de corridas
**antes** de comprometerse con este eje.

Riesgo secundario: si Soza Mamani y Prado Romo (2025) resultan estar adaptando las funciones de
costo del NMPC mediante RL sobre TCLab —que es la lectura que sugiere su resumen—, el solapamiento
sobre esta misma planta es directo. **Es la lectura pendiente más urgente de todas.**

### La pregunta del jurado más difícil

> *"Son dos o cuatro números y cada evaluación cuesta una corrida de minutos. ¿Por qué RL profundo
> y no una malla, un algoritmo genético, optimización bayesiana o LQR inverso?"*

---

## 3. Variante (c) — LQR o barrera como filtro de seguridad sobre la acción del RL

### Cuán poblada está esta literatura

**Alta y bien consolidada**, con cuatro familias distinguibles: conmutación entre controladores base
con conocimiento de Lyapunov (Perkins y Barto 2002); escudos lógicos (Alshiekh et al. 2018);
funciones barrera de control (Ames et al. 2017; Cheng et al. 2019); y filtros predictivos
(Wabersich y Zeilinger 2021). El survey canónico es García y Fernández (2015); las revisiones
recientes, Brunke et al. (2022) y Hewing et al. (2020). La variante que usa el LQR mismo como
certificado existe (Fernandez et al. 2020), con transferencia sim-to-real a hardware.

**En procesos térmicos: muy poco. En TCLab: nada.**

### Qué haría distinta a una tesis situada aquí

- **El TCLab tiene restricciones de seguridad reales y de dos tipos distintos**, lo que da contenido
  genuino al filtro: saturación del actuador (dura, trivial) y límite térmico (predictiva, no
  trivial, requiere anticipación por la inercia térmica). Solo la segunda justifica un filtro.
- **El obstáculo habitual del filtro predictivo aquí desaparece.** Con $T_s$ del orden de segundos,
  resolver una optimización pequeña por paso es holgado. Se puede argumentar que el TCLab es un
  banco especialmente adecuado para estudiar filtros predictivos.
- **Hay un segundo resultado medible además de la seguridad.** Cheng et al. (2019) sostiene que el
  filtro acota el espacio de políticas explorables y acelera el aprendizaje. Eso es contrastable.
- **Existe una versión proporcionada al nivel.** *(Añadido en la ronda 1.)* Perkins y Barto (2002)
  no exige sintetizar un CBF: basta con conmutar entre controladores base seguros. Es la ruta de
  menor carga teórica dentro de este eje.

### Contrafáctico operativo

Entrenar y evaluar **la misma política con filtro y sin filtro**, sobre el mismo perfil de setpoints
y perturbaciones, reportando (i) número de intervenciones del filtro por corrida, (ii) violaciones
del límite térmico en cada condición y (iii) curvas de aprendizaje de ambas, para contrastar la
afirmación de aceleración. Si el filtro no interviene nunca, forzar la condición con un agente
deliberadamente agresivo o una perturbación adversa, y declararlo.

### Riesgo específico de este eje

**La trampa de alcance: un recorte de saturación no es un filtro de seguridad.** Si el "filtro" se
reduce a `clip(u, 0, 100)`, la contribución se evapora. El filtro debe anticipar la violación del
límite térmico, no solo acotar la acción. Y sintetizar un CBF para una planta MIMO no lineal exige
conocimiento de dominio que la propia literatura reconoce como su punto débil.

Riesgo secundario: este eje consume presupuesto de esfuerzo en la parte de *seguridad* y deja menos
para la de *desempeño*. Hay que decidir de antemano cuál es el resultado principal.

### La pregunta del jurado más difícil

> *"¿Su filtro alguna vez se activó? Muéstreme las corridas en que intervino y qué habría pasado
> sin él."*

---

## 4. Variante (d) — Estudio comparativo LQR vs RL

### Cuán poblada está esta literatura

**Muy poblada.** *(La ronda 0 decía "saturada" nombrando un solo estudio; el crítico objetó con
razón. Los trabajos concretos están ahora en `frontier_map.md` §4: Agyei et al. 2025; Machacuay e
Ipanaqué 2024 y 2025; Páez Ardila et al. 2022; Insuasti et al. 2022; Bloor et al. 2026.)*

**Y sobre TCLab el nicho está ocupado por varios lados:** Soza Mamani y Prado Romo (2025) publicaron
NMPC vs DDPG vs TD3 sobre TCLab físico; Insuasti et al. (2022) y Páez Ardila et al. (2022)
publicaron comparativas de controladores clásicos sobre el mismo kit.

### Qué haría distinta a una tesis situada aquí

El margen no está en *qué* se compara sino en **cómo**, y ese "cómo" ahora tiene respaldo
bibliográfico propio:

- **Rigor de evaluación con estándar citable.** Henderson et al. (2018) y Agarwal et al. (2021)
  convierten el protocolo de N semillas y estimaciones por intervalo en el estándar del campo, no
  en una exigencia interna. *(Respaldo añadido en la ronda 1.)*
- **Márgenes de robustez, no solo IAE.** Agyei et al. (2025) muestra que el DDPG puede perder en
  márgenes de ganancia y de retardo aunque gane en velocidad. En el TCLab, cuyo retardo de
  transporte no es despreciable, eso es más informativo que otra tabla de IAE.
- **Evaluación fuera del punto de diseño**, no solo cerca de la linealización, donde el LQR es
  óptimo por construcción.
- **Un resultado negativo bien hecho es un resultado**, y es relativamente raro en esta literatura.

### Contrafáctico operativo

La comparación solo informa si el LQR puede perder por una razón identificable. Evaluar ambos
controladores **dentro y fuera del rango de linealización**, y además con el modelo deliberadamente
desajustado (identificado a una temperatura ambiente distinta de la de evaluación). Si el RL solo
gana fuera del punto de diseño o con el modelo desajustado, la diferencia queda *explicada*; si gana
igual en todas partes, lo más probable es que el LQR esté mal sintonizado y la comparación no valga.

### Riesgo específico de este eje

**Riesgo de lectura, no de método:** la tesis puede leerse como "Soza Mamani y Prado Romo (2025)
pero con un controlador más simple". La diferenciación tiene que venir del protocolo experimental y
del diseño de las condiciones, y eso hay que decidirlo antes de tomar el primer dato, no después.

Riesgo secundario: es el eje con mayor probabilidad de terminar en "no hay diferencia
significativa". Eso es un resultado legítimo, pero el estudiante debe entrar sabiéndolo y con el
director de acuerdo.

### La pregunta del jurado más difícil

> *"¿Qué aprendemos aquí que no supiéramos ya? Que el RL puede igualar a un LQR en una planta
> aproximadamente lineal no es sorprendente."*

---

## 5. Cuadro comparativo de las cuatro

| Criterio | (a) Residual | (b) Sintonía $Q,R$ | (c) Filtro de seguridad | (d) Comparativo |
|----------|--------------|--------------------|-------------------------|-----------------|
| Densidad de literatura general | Alta | Media | Alta | Muy alta |
| Densidad sobre TCLab | Vacía | Vacía | Vacía | Ocupada por trabajo adyacente |
| Vacío sostenido por encadenamiento de citas | **Sí** (97 obras citantes + corpus) | No (solo palabras clave) | No (solo palabras clave) | — |
| Obras que compiten de cerca | Alqithami 2026; Holt y Armellin 2025 | Zhang 2026; Soza Mamani 2025 | Fernandez 2020 | Soza Mamani 2025; Insuasti 2022 |
| Riesgo de solapamiento | Bajo | Medio-alto | Bajo en nicho, alto en método | Alto |
| Carga teórica | Media | Baja-media | Alta | Baja |
| Carga experimental sobre hardware | Alta | Muy alta (cada evaluación es una corrida completa) | Media | Alta |
| Competidor evidente no basado en RL | No | Sí (opt. bayesiana; LQR inverso) | Sí (MPC con restricciones) | — |
| Vía de menor carga dentro del eje | Residuo acotado sin garantía formal | Sintonía de 2 pesos diagonales | Perkins y Barto (2002): conmutación entre controladores base | Protocolo de evaluación reforzado |
| Compatible con medir brecha sim-to-real | Sí | Sí | Sí | Sí |
| Probabilidad de resultado "no hay diferencia" | Media | Media | Baja | Alta |

---

## 6. Combinaciones que la literatura sugiere pero el estudiante no listó

Se registran porque el mapa quedaría incompleto sin ellas. **No son recomendaciones.**

1. **(a) + (c): residual acotado por un filtro.** Es lo que hacen Holt y Armellin (2025), Alqithami
   (2026) y, en otra forma, Fernandez et al. (2020). **Y es hacia donde se mueve el campo en 2026**:
   entre los cien registros residuales más recientes aparecen, solo por título, *Provably Safe
   Residual RL Using Tube MPC*, *Safety-Filtered Residual RL over MPC*, *MPC-Informed Residual RL* y
   *Conflict-driven Adaptive Scaling for Safe Residual RL*. Cuesta más esfuerzo que cualquiera de
   las dos por separado. *(Actualizado en la ronda 1.)*

2. **Estructura de control dentro de la política (CIRL, Bloor et al. 2025).** Ni residual ni
   sintonía: el controlador clásico como sesgo inductivo de la arquitectura de la red. Es una quinta
   variante que existe en control de procesos y que el estudiante podría no conocer.

3. **Sintonía por optimización bayesiana o por LQR inverso, en lugar de RL** (Marco et al. 2016;
   Priess et al. 2015). Si la restricción dominante es el costo por evaluación en una planta lenta,
   la literatura ya tiene respuestas que no son RL.

4. **Sintonía diferenciable del costo** (Amos et al. 2018; MPC diferenciable de horizonte infinito,
   ICLR 2020). Deriva $K$ respecto de $Q$ y $R$ a través de la DARE, sin agente de RL.
   *(Añadida en la ronda 1.)*

---

## 7. Lo que hay que hacer antes de decidir

Ordenado por urgencia. Ninguno de estos textos fue leído en esta búsqueda.

| # | Texto | Qué hay que extraer | Decide qué |
|---|-------|---------------------|-----------|
| 1 | **Soza Mamani y Prado Romo (2025)**, *Processes* 13(6):1627 | ¿Qué hace exactamente el agente: adapta el costo del NMPC, o produce la acción? ¿Cuántas corridas y semillas? ¿Mide brecha sim-to-real? | Si (b) y (d) siguen en pie |
| 2 | **Patel (2023)**, *Comput. Chem. Eng.* 174:108232, y su precursor **Patel (2022)**, AdCONIP | ¿Hay política base o controlador clásico dentro del esquema? ¿Qué métricas reporta sobre TCLab? ¿Cuántas corridas? | Si (a) y (d) siguen en pie |
| 3 | **Alqithami (2026)**, *J. Process Control* | Cómo define el residuo regulatorio y cómo implementa el escudo. Es el precedente más cercano de (a)×(c) en procesos. | Cuánto margen queda en (a) y en (a)+(c) |
| 4 | **Zhang et al. (2026)**, *Mathematics* 14(5):895 | **Si hay o no experimento en hardware**, y qué dejan como trabajo futuro | Cuánto margen queda en (b) |
| 5 | **Lawrence et al. (2022)**, *CEP* 121:105046 | Protocolo experimental: corridas, semillas, saturación, diseño de recompensa | Plantilla metodológica para **cualquier** variante |
| 6 | **Park et al. (2020)**, *Comput. Chem. Eng.* 135:106736 | Modelos del TCLab (físico, ARX, Hammerstein-ANN) y su calidad de ajuste | Punto de partida del simulador, para **cualquier** variante |
| 7 | **Manurung et al. (2021)**, *IFAC-PapersOnLine* 54(20):735–740 | Confirmar si el banco es el TCLab y qué estado estima el EKF | El diseño del observador, para **cualquier** variante |

---

## 8. Declaración de alcance de este documento

- Ningún artículo de esta búsqueda fue leído en texto completo. Los niveles de lectura por entrada
  están declarados en `annotated_bibliography.md`.
- En la ronda 1 se leyeron **tres resúmenes** que antes solo se conocían por título (Reiter et al.,
  Furieri et al.) y **una página web** (el tutorial de APMonitor). Las afirmaciones que dependían de
  ellos se corrigieron o se recortaron.
- Ninguna cifra de desempeño de esta bibliografía debe entrar a la tesis sin localizar y leer el
  artículo original. Las magnitudes sin fuente rastreable que aparecían en la ronda 0 se retiraron.
- Los vacíos de los ejes (b) y (c) y el de la brecha sim-to-real **no** fueron sometidos a
  encadenamiento de citas y descansan todavía sobre búsqueda por palabras clave. Dos de los cinco
  vacíos originales cambiaron al aplicarles esa prueba; es razonable esperar que estos también se
  estrechen.
- Este documento entrega el mapa, no la ruta. **La elección de variante es del estudiante.**
