# Revisión de literatura — librarian-critic

**Fecha:** 2026-09-07
**Artefacto:** `quality_reports/literature/tclab-lqr-rl/`
**Severidad aplicada:** BAJA-MEDIA (fase de Descubrimiento). Excepción sin escalado: verificación de fabricación (INV-28).
**Puntaje: 72/100** — por debajo del umbral de 80. Requiere una ronda de corrección.

> Informe producido por el agente librarian-critic (solo lectura, sin capacidad de escritura por
> separación de poderes) y persistido por el orquestador. Los hallazgos mecánicos H-6 y H-7 fueron
> verificados de forma independiente por el orquestador antes de aceptar el informe: 5/5 archivos
> contaminados y exactamente 6 colisiones de clave, ambos confirmados.

---

## Veredicto en una línea

Trabajo honesto y bien calibrado al nivel de pregrado, sin una sola cita fabricada, con una disciplina de procedencia poco común; pero el propio estándar de honestidad que el librarian se impuso se incumple de forma sistemática en las entradas `[META]`, cinco entradas llevan sello `VERIFICADO` sobre evidencia de grado SERP, hay seis colisiones de clave BibTeX con la semilla, y falta la literatura de métodos que sostiene la contribución que el propio documento propone.

---

## Verificaciones obligatorias — resultado

| # | Verificación | Resultado |
|---|--------------|-----------|
| 0 | **Fabricación de citas (INV-28)** | **PASA.** Contrastadas ~40 entradas contra lo que el informe declara haber consultado. Ninguna entrada inventada. Anclas verificables correctas: Park 2020 `106736`; Johannink ICRA 6023–6029; Dean FoCM 20(4):633–679; Recht ARCRAS 2:253–279; Bradtke ACC vol. 3, 3475–3479; Fazel PMLR 80:1467–1476; Tu y Recht PMLR 80:5005–5014; Haarnoja PMLR 80:1861–1870; Wabersich Automatica 129:109597; Cheng AAAI 33(1):3387–3395; Kalman *Bol. Soc. Mat. Mexicana* 5:102–119. Ningún hallazgo crítico. |
| 1 | **Escala de proximidad** | **PASA.** §0 declara 1 = compite directamente … 5 = tangencial y la aplica en ese sentido. Ver H-12 por una debilidad estructural distinta. |
| 2 | **Honestidad del nivel de lectura** | **FALLA PARCIAL.** Ver H-1, H-2. |
| 3 | **Marcas `% UNVERIFIED`** | **FALLA PARCIAL.** Son 11, no 12 (la 12.ª ocurrencia es la leyenda, línea 13). Ver H-3, H-4. |
| 4 | **Cobertura de los cuatro ejes** | **DESIGUAL.** (c) bien cubierto, (a) suficiente, (b) delgado, (d) asertado sin documentar. Ver H-9d, H-10. |
| 5 | **Ausencias** | Seis literaturas concretas faltantes. Ver H-9. |
| 6 | **Neutralidad del posicionamiento** | **PASA CON RESERVA.** Sin recomendación explícita, pero elaboración asimétrica. Ver H-11. |
| 7 | **Calibración al nivel** | **PASA.** ~40 obras, dimensión correcta para pregrado. Marca explícitamente lo demasiado pesado (Furieri) como cita de encuadre. Acierto, no defecto. |

---

## Hallazgos

### H-1 — Las entradas `[META]` hacen afirmaciones de contenido que su nivel declarado no sostiene
**Severidad: MODERADA · −5**

§0 define `[META]` como *"metadatos bibliográficos verificados… No leí el contenido más allá del título."* Al menos nueve entradas se exceden:

- **§2.4 Reiter et al. `[META]`** — *"la clasificación (RL sobre el controlador, RL que parametriza el controlador, controlador como filtro) mapea casi uno a uno sobre las cuatro variantes"*. Afirmación sobre el contenido de una taxonomía, imposible de derivar del título. Es de las más cargadas del entregable: legitima el marco de los cuatro ejes apelando a una taxonomía publicada que no se leyó.
- **§4.4 Furieri et al. `[META]`** — *"garantizando estabilidad $\mathcal{L}_p$ en lazo cerrado incluso si la optimización se detiene antes de converger"*. Detalle técnico de resultado, no de título. Se repite en `frontier_map.md` §1 y `positioning.md` §1.
- **§8 Tu y Recht `[META]`**, **§8 Dean et al. `[META]`**, **§8 Mania et al. `[META]`**, **§3.2 McClement et al. `[META]`**, **§6.1 Alshiekh et al. `[META]`**, **§6.5 Berkenkamp et al. `[META]`**, **§8 Bradtke et al. `[META]`** — descripciones de método más allá del título.
- **§1.5 APMonitor `[SERP]`** — declara *"no la abrí"* y acto seguido afirma tres hechos técnicos: DDPG, en PyTorch, con entorno Gymnasium. Esa entrada asciende después a la tabla de riesgo de scooping.

**Atenuante:** la prueba concreta que exigía el encargo —afirmaciones sobre número de semillas o magnitud de resultados— se supera casi en todas partes. Los campos *Validación* y *Resultado principal* están sistemáticamente vacíos o marcados "no leído". El incumplimiento es en descripciones de método, no en cifras. De ahí −5 y no más.

### H-2 — Afirmación sin cobertura que sostiene el vacío del eje (b)
**Severidad: MENOR-MODERADA · −2**

`references.bib` (Zhang2026, L356) y §5.2 afirman sin matiz *"Solo simulación"* / *"Sin hardware"*, desde nivel `[ABS]`. Sobre eso descansan: `frontier_map.md` §2 (el vacío del eje b) y `positioning.md` §2 (*"deja el hueco explícito"*). Si Zhang et al. incluyen aunque sea un experimento de validación en planta, el vacío del eje (b) se desploma. Contrasta con el buen manejo de Furieri (*"presumiblemente simulación"*) y Holt y Armellin (*"presumiblemente solo simulación — no verificado"*). Zhang es el único caso load-bearing sin hedge.

### H-3 — Cinco entradas rotuladas `VERIFICADO` sobre evidencia de grado SERP, sin `% UNVERIFIED`
**Severidad: MODERADA · −3**

| Entrada | Nota | Problema |
|---|---|---|
| `Fazel2018_policy_gradient_lqr` (L539) | *"pagina oficial PMLR … presente en los resultados"* | Aparecer en resultados ≠ consultar la página |
| `TuRecht2018_lstd_lqr` (L554) | *"pagina oficial PMLR"* | Sin declarar si se abrió |
| `Mania2018_random_search` (L592) | *"consultada en resultados"* | Hash truncado; evidencia SERP |
| `Alshiekh2018_shielding` (L385) | *"El rango 2669-2678 proviene de la sintesis de resultados"* | Campo `pages` es SERP bajo cabecera VERIFICADO |
| `Lillicrap2016_ddpg` (L651) | *"confirmados en la busqueda"* | Fuente no nombrada |

Incoherente que `Berkenkamp2017` reciba `% UNVERIFIED` por páginas de origen SERP y `Alshiekh2018` no, siendo el mismo tipo de evidencia.

### H-4 — Uso semánticamente laxo de `% UNVERIFIED` en cuatro entradas
**Severidad: MENOR · −1**

`Silver2018` (L270), `Yildiran2023` (L365), `Fernandez2020` (L446) y `Agyei2025` (L489) llevan la marca por *"no comprobé si existe versión publicada"*. Eso no es un campo sin confirmar: autor, título, año e identificador arXiv sí están verificados. Bajo la regla del propio archivo —*"No citar hasta confirmarlo"*— esto bloquearía innecesariamente cuatro preprints citables, incluido Silver et al. (2018), fundamento del eje (a). Hace falta un estado "estado de publicación no comprobado" separado de "campo sin confirmar".

### H-5 — Magnitudes numéricas sin fuente localizable
**Severidad: MENOR-MODERADA · −2**

§7.2 reporta −78,6 % de sobreimpulso, +51,1 % en tiempo de establecimiento, ISE 47,6 %, IAE 26,5 %, sobreimpulso 100 %, atribuidas a *"un controlador PPO sobre intercambiador termoeléctrico"* y *"un PID adaptativo con TD3"*: sin autor, año, título ni DOI. El lector no puede localizarlas nunca. Están marcadas como no citables y fuera de `references.bib` —lo que las salva de ser hallazgo crítico bajo INV-28— pero reaparecen en `frontier_map.md` §4 con un hedge más débil (*"las magnitudes que circulan"*). O se localiza el artículo, o se elimina el número y se conserva la advertencia cualitativa. Además, *"sobreimpulso 100 %"* es ininteligible: ¿reducción del 100 %, o sobreimpulso del 100 %?

### H-6 — Seis colisiones exactas de clave BibTeX con `Bibliography_base.bib`
**Severidad: MODERADA · −2**

El encabezado declara ser *"un ANEXO, no un reemplazo"*, pero al incluir versiones corregidas reutiliza la clave idéntica sin indicar que haya que borrar la semilla. Si ambos archivos se pasan a biber:

**Colisiones exactas (6):** `Kalman1960_contributions`, `Haarnoja2018_sac`, `Lillicrap2016_ddpg`, `Dean2020_sample_complexity_lqr`, `Recht2019_tour_rl`, `Fazel2018_policy_gradient_lqr`.

**Casi-duplicados (misma obra, clave distinta):** `Park2020_tclab`/`Park2020_tclab_benchmark`; `Silver2018_residual_policy`/`Silver2018_residual_policy_learning`; `Johannink2019_residual_rl`/`Johannink2019_residual_rl_robot`; `Berkenkamp2017_safe_rl`/`Berkenkamp2017_safe_mbrl_stability`; `Bradtke1994_adaptive_lq`/`Bradtke1994_adaptive_lq_policy_iteration`; `Bertsekas_dynamic_programming`/`Bertsekas2017_dynamic_programming_vol1`; `Ogata_control_moderna`/`Ogata2010_control_moderna`.

`verificacion_bib_semilla.md` §2.8 detecta el caso Park pero no generaliza. Falta una sección de reconciliación de los dos archivos.

### H-7 — Contaminación de los cinco archivos con tokens de herramienta
**Severidad: MENOR · −1**

Los cinco entregables terminan con `</content>` y `</invoke>` literales. En los `.md` se renderiza como texto suelto; en `references.bib` es basura al final de un archivo que biber va a parsear. Es 5/5: defecto de proceso, no accidente.

### H-8 — No hay evidencia de encadenamiento de citas, pese a ser instrucción explícita
**Severidad: MODERADA · −3**

Los tres documentos describen la búsqueda solo en términos de formulaciones de palabras clave. En ningún punto se reporta búsqueda de citas hacia adelante ni hacia atrás. No es formalismo: **el hallazgo central —los cinco vacíos— descansa entero sobre búsqueda por palabras clave.** Las dos pruebas decisivas no se hicieron:

- *Citas hacia adelante de Silver (2018) y Johannink (2019)*, filtradas por control de procesos: vía natural para hallar RL residual en plantas térmicas, exactamente el vacío declarado *"el más limpio de los cuatro"*.
- *Citas hacia adelante de Park et al. (2020)*: quién cita el artículo de referencia del TCLab y hace diseño de control sobre él. Prueba definitiva del vacío "LQR sobre TCLab".

El vacío puede ser real, pero la evidencia no lo establece con la fuerza que el documento le atribuye.

### H-9 — Vacíos de literatura de métodos
**Severidad: MODERADA · −6 (itemizado)**

**H-9a (−2) · Metodología de evaluación en RL profundo — ausente por completo.** `positioning.md` §4 hace del rigor experimental *el* margen de contribución. La literatura que estableció ese estándar no está citada: Henderson et al. (2018), *Deep Reinforcement Learning that Matters*, AAAI 32; Agarwal et al. (2021), *Deep RL at the Edge of the Statistical Precipice*, NeurIPS 34. Sin ellas, INV-14 y el protocolo de semillas quedan como exigencia interna del proyecto en vez de estándar del campo. Es la ausencia más grave.

**H-9b (−1) · Sim-to-real sin ancla metodológica.** Faltan Tobin et al. (2017) *Domain Randomization*; Peng et al. (2018), *Sim-to-Real Transfer with Dynamics Randomization*, ICRA; Zhao, Queralta y Westerlund (2020), survey de sim-to-real en DRL. La justificación dada (*"está concentrada en robótica"*) es un enunciado sobre la aplicación, no una razón para omitir el método que se propone usar.

**H-9c (−1) · Eje (c) sin sus anclas seminales.** Falta Ames, Xu, Grizzle y Tabuada (2017), IEEE TAC 62(8):3861–3876; el survey canónico García y Fernández (2015), JMLR 16:1437–1480; y el precedente directo de "controlador clásico como respaldo seguro del RL": Perkins y Barto (2002), JMLR 3:803–832. Ausente la rama CMDP/Lagrangianos (Achiam et al., CPO 2017).

**H-9d (−1) · Eje (b) es el peor documentado.** Solo tres entradas propias. Faltan dos familias: *LQR/MPC diferenciable* (Amos et al. 2018, NeurIPS; East et al. 2020, ICLR) y *control óptimo adaptativo desde la comunidad de control* (Kiumarsi, Vamvoudakis, Modares y Lewis 2018, IEEE TNNLS 29(6):2042–2062; y el LQR inverso: Priess et al. 2015, IEEE TCST 23(2):770–777).

**H-9e (−1) · Cero cobertura de LQG/observador y de acción integral (LQI).** El TCLab mide dos temperaturas de una planta 2×2 con dinámica de orden superior: el LQR por realimentación de estados casi con seguridad exigirá observador. No hay una sola referencia de LQG, Luenberger o filtro de Kalman aplicado a control. Y todo el entregable habla de seguimiento de setpoint cuando el LQR es un regulador: la formulación servo/LQI es requisito de método.

**H-9f (−1) · Literatura iberoamericana declarada vacía sin nombrar dónde se buscó.** Para un trabajo de la Universidad Distrital ante un jurado colombiano, y en una plataforma de uso extendido en la docencia de control latinoamericana, no se declara haber buscado en RIAI (*Revista Iberoamericana de Automática e Informática Industrial*), en actas del CLCA, ni en repositorios institucionales de trabajos de grado. Un vacío solo se puede reportar si se nombra dónde se buscó.

### H-10 — El eje (d) se declara "saturado" con una sola comparativa nombrada
**Severidad: MENOR · −1**

Se afirma *"decenas de comparativas"*, *"demasiado"*, *"abundante"*. De todo eso se nombra exactamente un estudio comparativo: Agyei et al. (2025), preprint sin sede verificada, cifras de nivel `[SERP]`. Un eje descartado por saturación debería documentarla con tres o cuatro representantes; si no, "saturado" es una impresión, y esa impresión está cerrando una de las cuatro opciones del estudiante.

### H-11 — Neutralidad declarada, elaboración asimétrica hacia el eje (a)
**Severidad: MENOR-MODERADA · −2**

Cumple la letra (nunca dice "elige X") pero la presentación converge:

- Superlativos evaluativos reservados al eje (a): *"el más limpio de los cuatro"*, *"el eje más despejado"*.
- El eje (a) recibe un diseño experimental completo y accionable; ningún otro recibe un contrafáctico operativo de esa especificidad.
- En el cuadro §5, (a) es la única celda de riesgo con **Bajo** sin matiz; las demás columnas llevan negativos en negrita.
- Subsecciones adversas exclusivas de los otros ejes (*"La pregunta incómoda…"*, *"El riesgo específico…"*, *"El problema específico…"*). El eje (a) no tiene equivalente.

Contraargumento reconocido: si la evidencia realmente favorece a (a), la asimetría es reporte honesto. De ahí la deducción pequeña. La crítica precisa no es "recomienda (a)", sino que **el desnivel de elaboración y el vocabulario evaluativo hacen el trabajo de una recomendación sin asumir su responsabilidad.**

Punto a favor: §6 introduce CIRL y optimización bayesiana como opciones no listadas por el estudiante, prefaciadas con *"No son recomendaciones"*. Eso amplía el espacio de decisión y es lo que un mapa neutral debe hacer.

### H-12 — La proximidad es un escalar único aunque la pregunta de investigación está indefinida
**Severidad: MENOR · −1**

Con cuatro ejes vivos, la proximidad depende del eje. Se intuye una vez (§1.5) pero no se sistematiza, y el escalar único subestima a los competidores más directos: Zhang et al. (2026) = 2, cuando bajo el eje (b) es un 1 por la escala declarada; Holt y Armellin (2025) = 2, cuando bajo (a)×(c) es un 1. La sustancia se rescata en la tabla de scooping, así que es defecto de instrumento, no de juicio. Lo correcto sería un vector de cuatro proximidades por entrada.

---

## Lo que está bien hecho

1. **Cero fabricación.** Criterio más pesado de la rúbrica, superado limpiamente.
2. **La auditoría de la semilla es exacta y verificable.** 19 entradas, 8 comentarios `% VERIFICAR`, 13 campos individuales: la aritmética cuadra. La resolución de `Park2020_tclab` contra Crossref es exactamente el trabajo que INV-28 exige.
3. **El hallazgo de Bertsekas Vol. I vs Vol. II excede lo pedido** y es genuinamente valioso.
4. **Iniciativa auditora más allá del encargo:** revisa entradas no marcadas y declara *"no las verifiqué; el hecho de no estar marcadas no significa que estén verificadas"*.
5. **Corrección de atribución errónea detectada y documentada** (Soza Mamani/Prado Romo vs. la atribución falsa que devolvió una síntesis de búsqueda).
6. **Recencia excelente:** ocho obras de 2025–2026.
7. **Mezcla de sedes correcta:** solo ~15 % preprint-only, muy por debajo del umbral de alarma y sano para RL-para-control. Ausencia menor no deducida: L4DC, sede natural de esta intersección.
8. **Reporte de vacíos en vez de relleno**, con la advertencia de que *"la contribución no puede sostenerse solo en la novedad de la plataforma"*.
9. **Calibración al nivel, explícita y correcta.**

---

## Desglose del puntaje

| | Concepto | Descuento |
|---|---|---|
| | **Inicial** | **100** |
| H-1 | Nivel `[META]`/`[SERP]` excedido en ≥9 entradas | −5 |
| H-2 | "Zhang (2026) solo simulación" sin hedge; sostiene el vacío del eje (b) | −2 |
| H-3 | Cinco entradas `VERIFICADO` sobre evidencia SERP, sin `% UNVERIFIED` | −3 |
| H-4 | Uso semánticamente laxo de `% UNVERIFIED` en cuatro entradas | −1 |
| H-5 | Magnitudes numéricas sin fuente localizable | −2 |
| H-6 | Seis colisiones exactas de clave BibTeX + casi-duplicados | −2 |
| H-7 | Tokens de herramienta en los cinco archivos | −1 |
| H-8 | Sin evidencia de encadenamiento de citas | −3 |
| H-9a | Metodología de evaluación en RL profundo ausente | −2 |
| H-9b | Sim-to-real sin ancla metodológica | −1 |
| H-9c | Eje (c) sin Ames (2017), García y Fernández (2015), Perkins y Barto (2002) | −1 |
| H-9d | Eje (b) sin LQR/MPC diferenciable ni control óptimo adaptativo ni LQR inverso | −1 |
| H-9e | Cero cobertura de LQG/observador y de LQI/acción integral | −1 |
| H-9f | Literatura iberoamericana declarada vacía sin nombrar fuentes | −1 |
| H-10 | Eje (d) declarado saturado con una sola comparativa nombrada | −1 |
| H-11 | Elaboración asimétrica que inclina hacia el eje (a) | −2 |
| H-12 | Proximidad escalar única con RQ indefinida | −1 |
| | **Final** | **72/100** |

**Umbral de fase:** 80. **No aprueba.** Corresponde una ronda de corrección con el librarian.

---

## Prioridades para la ronda de corrección

1. **H-7, H-6** (mecánico, minutos): limpiar los cinco archivos; añadir sección de reconciliación que diga qué claves de la semilla deben borrarse.
2. **H-3, H-4** (media hora): degradar a `% UNVERIFIED` las cinco entradas con evidencia SERP; separar "estado de publicación no comprobado" de "campo sin confirmar" para no bloquear cuatro preprints citables.
3. **H-1, H-2** (revisión de texto): subir el nivel declarado leyendo el resumen —que es barato— o recortar las afirmaciones a lo que el título sostiene. Reiter et al. y Furieri et al. son prioritarios porque su contenido es load-bearing. Poner hedge a "Zhang (2026) solo simulación".
4. **H-8** (búsqueda nueva, alto valor): citas hacia adelante de Silver (2018), Johannink (2019) y Park et al. (2020). Es lo que convierte los vacíos declarados de impresión en hallazgo.
5. **H-9a, H-9b** (seis citas): sin la literatura de evaluación en RL y de sim-to-real, la contribución propuesta queda sin respaldo bibliográfico.
6. **H-9e** (dos o tres citas): LQG/observador y LQI. Requisito estructural del proyecto, no adorno.
7. **H-11, H-10** (reequilibrio): dar a (b), (c) y (d) un contrafáctico operativo del mismo grano que el de (a); sustituir superlativos por descriptores; documentar la saturación de (d) o retirar la calificación.

---

## Ruta de escalamiento

Desacuerdo resoluble por el trabajador, **no** materia de escalamiento. Ningún hallazgo es una disputa de alcance amplitud-vs-profundidad. Si tras tres rondas persistiera, el objetivo declarado en `permissions.md` para este par es el **Usuario**.
