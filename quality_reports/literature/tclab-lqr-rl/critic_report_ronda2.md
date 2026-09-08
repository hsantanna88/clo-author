# Revisión de literatura — librarian-critic (ronda 2)

**Fecha:** 2026-09-08
**Severidad:** BAJA-MEDIA (Descubrimiento), con excepción no escalable para INV-28
**Puntaje: 73/100 — NO alcanza el umbral de 80**

> Lectura en frío: este crítico no vio el informe de la ronda 1 (`critic_report_ronda1.md`).
> Los hallazgos de aquella ronda se resolvieron; estos son nuevos, salvo C12, que es el residuo
> conocido de las colisiones de clave.

---

## Fabricación de citas (INV-28) — LIMPIO, sin deducción

Contrastadas ~45 de las 70 entradas. **Ninguna cita fabricada.** La consistencia año/volumen —donde
suele delatarse una entrada inventada— es correcta en todos los casos verificables: *Processes* 13 =
2025, *Mathematics* 14 = 2026, *IEEE T-RO* 41 = 2025, *Annual Reviews in Control* 61 = 2026,
PMLR 80 = ICML 2018.

Tres prácticas que sostienen el veredicto:

1. La atribución errónea de una síntesis de búsqueda (Soza Mamani y Prado Romo atribuidos a
   "Onyenanu et al.") está documentada y corregida, no silenciada.
2. `East2020_infinite_horizon_diff_mpc` se entrega **sin campo `author` a propósito**: *"El apellido
   'East' proviene del encargo del coordinador, NO de una fuente que yo consultara, así que NO lo
   escribo como dato."* Es lo contrario de fabricar.
3. `Luenberger1971_observers` marca como no verificada la expansión "David G." porque Crossref
   registra "D. Luenberger". Escrúpulo inusual en un campo de nombre propio.

---

## Escala de proximidad — dirección correcta, agregación contradicha

La escala (1 = compite directamente … 5 = tangencial) se aplica en la dirección correcta en todo el
documento. **Sin uso invertido, sin deducción por esto.**

Pero §0 declara una regla de agregación —*"el escalar general es el mínimo del vector"*— que la
tabla §11 **viola en 4 de 13 filas**, todas en la misma dirección:

| Obra | Escalar declarado | Vector (a)(b)(c)(d) | Mínimo real |
|---|---|---|---|
| Holt y Armellin (2025) | 2 | (1, 3, 1, 4) | **1** |
| Alqithami (2026) | 2 | (1, 4, 2, 4) | **1** |
| Zhang et al. (2026) | 2 | (3, 1, 5, 4) | **1** |
| Fernandez et al. (2020) | 2 | (2, 4, 1, 4) | **1** |

El párrafo posterior agrava la contradicción: dice *"bajo el eje (a) hay tres competidores de
proximidad 1"* mientras la columna "General" sigue diciendo 2.

---

## Hallazgos

### C1 · MODERADO · −3 — Falta la literatura de identificación de sistemas

`positioning.md` §0 abre las obligaciones comunes a las cuatro variantes con la identificación de un
modelo lineal en espacio de estados. Es el paso del que dependen los cuatro ejes —sin modelo no hay
LQR— y todo su respaldo es un paréntesis con un apellido. El perfil de dominio nombra protocolos
(PRBS, multiseno, doblete) y enfoques (ARX/ARMAX, subespacios/N4SID) que **no tienen ninguna entrada
bibliográfica** en el entregable.

Ausencias concretas: **Van Overschee y De Moor (1996), *Subspace Identification for Linear Systems***
(texto canónico de N4SID); y una referencia de **diseño de señales PRBS** (capítulo de Ljung, o
Godfrey, *Perturbation Signals for System Identification*). Un jurado preguntará por el periodo de
reloj del PRBS y por el criterio de selección de orden en subespacios.

**Agravante:** el entregable no declara este vacío. Declara con cuidado los de (b), (c) y sim-to-real,
pero este no aparece ni en la tabla §12 ni en "Lo que sigue sin hacerse".

### C2 · MODERADO · −3 — El eje (b) omite la rama con la que la comunidad de control nombra este problema

Bien servido por el lado del aprendizaje automático (Zhang, Marco, Amos, East) y por el clásico
(Priess, LQR inverso). Falta la rama intermedia, la que un jurado colombiano de control reconocerá:

- **Programación dinámica adaptativa / integral RL para LQR:** Jiang y Jiang (2012), *Automatica*
  48(10); Vrabie y Lewis (2009). Kiumarsi et al. (2018) está presente, pero es el *survey* de esa
  rama y no se extrae de él ninguna obra primaria. Un survey sin sus obras primarias no cubre la rama.
- **RL inverso:** el eje (b) formulado como "recuperar $Q$ y $R$ del comportamiento" **es** RL
  inverso. Falta Ng y Russell (2000), ICML, la cita canónica.
- **Contrafáctico sin respaldo:** el documento plantea como pregunta difícil del jurado *"¿por qué RL
  profundo y no una malla, un algoritmo genético, optimización bayesiana o LQR inverso?"* — y da
  referencia para dos de las cuatro alternativas.

### C3 · MENOR · −1 — Ausencia de CMDP/Lagrangianos en `positioning.md` §6

Ver adjudicación abajo.

### C4 · MODERADO · −4 — La forma del entregable es ancha y delgada; para un pregrado debía ser al revés

70 entradas, **cero textos completos leídos**. El propio entregable lo admite dos veces, y la segunda
es seria: *"Nada sustituye leer los textos completos de §1.2, §1.3, §4.6 y §5.2. Son los cuatro
artículos que determinan el margen real de contribución."*

Leídas juntas, esas frases dicen que **la decisión que el entregable existe para informar todavía no
puede tomarse con lo que el entregable entrega**. Cuatro artículos leídos a fondo habrían informado
la elección de eje mejor que metadatos verificados de setenta. La verificación es impecable; el
problema es que se invirtió en amplitud en lugar de en profundidad. El documento identifica la vía
—biblioteca de la Universidad Distrital— sin haberla recorrido.

### C5 · MENOR · −1 — El aparato metodológico excede lo que la decisión requiere

Vector de cuatro proximidades por entrada, taxonomía de marcas de cinco valores, barridos con
recuentos, ~1.800 líneas. Es infraestructura de revisión sistemática al servicio de una decisión de
cuatro opciones. La tabla §5 de `positioning.md` y la §12 de `frontier_map.md` cargan casi todo el
peso decisorio y podrían haber sido el entregable con un tercio del volumen.

### C6 · MODERADO · −3 — La tabla §11 contradice su propia regla de agregación

Detallado arriba: 4 de 13 filas. Como §11 es el instrumento con el que el estudiante comparará
competencia entre ejes, la inconsistencia **subestima sistemáticamente a los competidores más
directos** de (a), (b) y (c).

### C7 · MODERADO · −2 — La fila de riesgo de solapamiento contradice la §11, a favor del eje (a)

`positioning.md` §5 califica: (a) Bajo · (b) Medio-alto · (c) Bajo en nicho · (d) Alto.

Pero la §11 dice que **(a) tiene tres competidores de proximidad 1**, más que ningún otro eje —(b),
(c) y (d) tienen dos cada uno. Calificar de "Bajo" el eje con más competidores directos mientras (b)
recibe "Medio-alto" es una asimetría que empuja hacia (a) por la vía de la tabla resumen.

El documento neutralizó honestamente el vocabulario —los superlativos desaparecieron y los cuatro
ejes tienen contrafáctico, riesgo específico y pregunta del jurado— pero la neutralidad se le escapó
por las celdas, que es donde más pesa.

Efecto relacionado sin deducción: la fila *"Vacío sostenido por encadenamiento de citas"* da **Sí** a
(a) y **No** a (b) y (c). Es exacto, pero refleja **dónde se gastó el esfuerzo de búsqueda**, no una
propiedad del campo. La salvedad existe en el cuerpo, pero no en la celda — y la tabla se lee suelta.

### C8 · MODERADO · −2 — La regla de disciplina cubre `[META]` pero no `[SERP]`, que es más débil

§0 endurece la disciplina solo para `[META]`. No hay regla equivalente para `[SERP]`. Resultado: dos
afirmaciones de mecanismo load-bearing apoyadas solo en síntesis de resultados:

- **Perkins y Barto (2002)**, `[SERP]`, sostiene una descripción de mecanismo completa que viaja
  después a `positioning.md` §3 y a la celda *"Vía de menor carga dentro del eje"* de la tabla §5,
  **sin hedge de nivel en ninguno de los dos sitios.** Es la recomendación operativa más concreta
  del documento sobre el eje (c).
- **Agarwal et al. (2021)**, `[SERP]`, sostiene contenido metodológico específico que funda el punto
  8 de las obligaciones comunes.

Menores en la misma categoría: Mania et al., Tu y Recht, Amos et al., East 2020.

### C9 · MODERADO · −2 — Dos entradas declaran `[ABS]` sobre resúmenes leídos "vía síntesis"

El propio `references.bib` fija el criterio: *"una página que aparece en los resultados NO cuenta
como consultada. Solo cuenta abrirla."* Aplicado a rajatabla, están infladas:

- §3.5 Gros y Zanon: *"[ABS] (metadatos en Crossref; **resumen vía síntesis**)"*
- §6.4 Wabersich y Zeilinger: *"[ABS] (Crossref + **resumen vía síntesis**)"*

Y la de Gros y Zanon escala otra vez: `frontier_map.md` §2 dice que el trabajo *"**demuestra
formalmente**…"* — afirmación sobre el cuerpo, hecha desde un resumen que no se abrió.

Contraste que muestra que el criterio sí se sabe aplicar: Reiter y Furieri se elevaron a `[ABS]`
abriendo arXiv, y de Furieri se cita el resumen textualmente.

### C10 · MENOR · −1 — Dos entradas `[SERP]` con marca acotada al campo de sede

`Lin2024_transfer_learning_process_rl` e `Ishihara2023_residual_rl_quadcopter` son `[SERP]` pero su
marca solo dice "UNVERIFIED: sede". A nivel `[SERP]` tampoco están confirmados autores ni año.
Compárese con Fernandez, Silver, Yildiran y Agyei, que sí declaran *"página de arXiv consultada
directamente"*. **Mismo grado de evidencia, marca distinta.**

### C11 · MENOR · −1 — El sistema declara tres estados y el archivo usa cinco

La convención declara *(sin marca)*, `% UNVERIFIED`, `% PUBLICACION_NO_COMPROBADA`. El archivo usa
además `VERIFICADO` como marcador positivo (~35 entradas, cuando lo verificado debía ir sin marca),
`PARCIAL` (Alshiekh) y `VERIFICADO parcialmente` (Bertsekas). Además, el campo NIVEL DE LECTURA solo
se registra en las entradas de la ronda 1 (secciones 10–16): quien lea `references.bib` sin la
bibliografía anotada no sabe con qué evidencia cuenta para dos tercios del corpus.

### C12 · MENOR · −2 — Las 6 colisiones de clave siguen vivas

La sección de reconciliación las nombra y da procedimiento, lo que reduce mucho la gravedad. Pero
tal como se entregan, **los dos archivos no pueden pasarse ambos a biber**. Un entregable cuyo
contrato es producir `references.bib` no debería dejarlo en estado no compilable junto a la
bibliografía central, aunque documente cómo arreglarlo.

### C13 · MENOR · −2 — Cribado por título sin declarar como falso negativo; falta el barrido simétrico

La solidez de la evidencia de los vacíos es **la parte más fuerte del entregable**: declara qué se
probó con qué herramienta e IDs, cuáles vacíos NO se probaron, la limitación de OpenAlex sin
suavizarla, la asimetría interpretativa del vacío, dónde no buscó bien, y se autocorrige en dos de
cinco vacíos. Eso está por encima del estándar. La deducción es por dos huecos:

1. **Cribado solo por título.** Las tres búsquedas (84 + 52 + 45) se resolvieron leyendo títulos. El
   documento es transparente en eso, pero **nunca dice que el cribado por título produce falsos
   negativos**. Un artículo que aplique LQR al TCLab puede titularse "Control óptimo de un sistema
   térmico de bajo coste" sin la sigla.
2. **Falta el barrido simétrico** sobre `"TCLab" OR "temperature control lab"` en
   `title_and_abstract.search`. Es más barato que los tres encadenamientos juntos, no depende de que
   la obra cite a Park (2020), y es la prueba natural del vacío central del proyecto.

---

## Adjudicación: CMDP / Lagrangianos (Achiam et al., CPO)

**Concuerdo con el creador en el fondo y discrepo en la conclusión.**

La distinción es correcta: el eje (c) es un mecanismo **externo** que corrige o veta la acción,
mientras que CMDP **interioriza la restricción en el objetivo** vía multiplicadores, sin filtro
externo ni garantía por episodio. **No debe figurar como componente del eje (c).** Sin deducción por
la discrepancia.

**Pero debe figurar en `positioning.md` §6**, donde el propio creador propuso. La razón no es
completitud taxonómica sino una consecuencia de posicionamiento medible: la §6 lista hoy cuatro
alternativas —CIRL para (a); optimización bayesiana, LQR inverso y sintonía diferenciable para (b)—
**es decir, (a) y (b) reciben alternativas y (c) no recibe ninguna.** Y (c) es el único al que la
tabla §5 asigna *"Carga teórica: Alta"*.

El estudiante que lea el mapa para decidir sobre (c) ve dos rutas caras más el paliativo de Perkins
y Barto, que además está apoyado solo en `[SERP]`. Una formulación CMDP con Lagrangiano es la vía
más barata para RL consciente de restricciones sobre esta planta. **Omitirla no es neutral: hace que
(c) parezca más caro de lo que la literatura permite.**

Recomendación: **Achiam, Held, Tamar y Abbeel (2017), "Constrained Policy Optimization", ICML** como
punto 5 de §6, con la distinción que el propio creador formuló. Opcionalmente Ray, Achiam y Amodei
(2019), *Benchmarking Safe Exploration in Deep RL*. Deducción −1, no más, porque el razonamiento del
creador era correcto y solo le faltó ver la asimetría que su propia §6 producía.

---

## Verificación de `Bibliography_base.bib` — cumplida

Auditoría campo a campo (8 comentarios, 13 campos), con escala de cuatro estados y método declarado:
12 confirmados, 1 resuelto por inaplicabilidad, 0 no confirmados. Dos hallazgos valiosos:

1. **El error latente de Bertsekas.** La semilla dice 2017, 4.ª ed., sin declarar volumen. La 4.ª ed.
   del Vol. I es 2017 pero la del Vol. II es 2012, y el contenido relevante para el puente LQR↔RL
   está en el Vol. II. **Si la tesis cita a Bertsekas para lo que va a citarlo, el año es incorrecto.**
2. **La distinción entre las dos obras de Kalman de 1960** (LQR en *Bol. Soc. Mat. Mexicana* y filtro
   en *J. Basic Engineering*), con aviso en tres sitios de no fusionarlas.

Registra además que `AndersonMoore1990` y `AstromHagglund2006` no llevan marca pero tampoco fueron
verificadas: *"no estar marcada NO significa estar verificada"*. Razonamiento correcto sobre INV-28.

---

## Desglose del puntaje

| Categoría | Deducción | Detalle |
|---|---|---|
| **Inicial** | **100** | |
| 1. Vacíos de cobertura | **−7** | C1 identificación de sistemas −3 · C2 ADP/RL inverso −3 · C3 CMDP −1 |
| 2. Calidad de las sedes | **0** | Sedes nucleares de control y de ML presentes; preprints ~14 % |
| 3. Calibración de alcance | **−5** | C4 ancho y delgado −4 · C5 aparato desproporcionado −1 |
| 4. Recencia | **0** | 2024–2026 cubierto; scooping específico; preprint vs publicado distinguidos |
| 5. Calidad de la categorización | **−5** | C6 §11 viola su regla del mínimo −3 · C7 fila de solapamiento −2 |
| 6. BibTeX | **−8** | Fabricación 0 · C8 −2 · C9 −2 · C10 −1 · C11 −1 · C12 −2 |
| Solidez de la evidencia de vacíos | **−2** | C13 −2 |
| **Final** | **73/100** | |

---

## Recomendación

**NO APRUEBA el umbral de 80.** Rechazo estrecho, y conviene ser claro sobre su naturaleza: **no hay
ningún problema de integridad.** Sin citas fabricadas, escala correcta, vacíos con base probatoria y
limitaciones declaradas, auditoría exhaustiva que encontró un error real. La honestidad está por
encima del estándar y **no debe rehacerse**.

Lo que lo deja bajo el umbral son tres cosas de naturaleza distinta:

1. **Una inconsistencia interna que sesga la decisión del estudiante** (C6 + C7). Reparable sin
   buscar nada: recalcular una columna y recalificar una fila.
2. **Un vacío de cobertura no declarado** (C1 + C2): identificación de sistemas y la rama ADP / RL
   inverso del eje (b).
3. **La forma del entregable es la contraria a la que pide un pregrado** (C4).

### Ruta más corta al umbral

1. Recalcular la columna "General" de §11 según la regla del mínimo, o reescribir la regla; y
   recalificar la fila "Riesgo de solapamiento" de forma consistente. *(~5 puntos)*
2. Añadir la regla de disciplina para `[SERP]` en §0 y aplicarla: hedge a Perkins y Barto en §3 y en
   la tabla §5; degradar Gros y Zanon y Wabersich–Zeilinger o abrir sus resúmenes; retirar "demuestra
   formalmente"; ampliar el alcance de `% UNVERIFIED` en Lin2024 e Ishihara2023. *(~5 puntos)*
3. Añadir identificación de sistemas (2–3 entradas) y la rama ADP/RL inverso (2–3 entradas), y
   declarar el vacío en la tabla §12 si no se cubre. *(~6 puntos)*
4. Añadir Achiam et al. (2017) a §6 como punto 5. *(~1 punto)*
5. Ejecutar el barrido de OpenAlex sobre `"TCLab" OR "temperature control lab"` y nombrar el cribado
   por título como fuente de falsos negativos. *(~2 puntos)*

**La lectura de los cuatro textos completos es lo que más valor aporta a la tesis, y ninguna ronda de
corrección bibliográfica la sustituye.**
