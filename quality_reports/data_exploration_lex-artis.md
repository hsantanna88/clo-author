# Data Exploration — Corpus Jurisprudencial
## Lex artis, consentimiento informado y daño médico: criterios jurisprudenciales de responsabilidad civil en el Perú

**Fecha:** 2026-05-21  
**Agentes:** Explorer → Explorer-critic  
**Score del crítico:** 35/100 — FAIL (umbral: 75)  
**Diagnóstico:** Las fuentes identificadas son correctas; el documento de evaluación carece de la arquitectura metodológica para construir un corpus defendible.

---

## RESUMEN EJECUTIVO

El Explorer identificó 12 fuentes relevantes y recomendó una estrategia de tres fuentes gratuitas (JNS + El Peruano + LP Pasión). Las fuentes son las adecuadas para este tipo de investigación en Perú. El problema no es cuáles son las fuentes — el problema es que la evaluación no documenta el protocolo de búsqueda, el procedimiento de verificación de cobertura, ni la arquitectura metodológica para ensamblar un corpus sistemático defendible ante árbitros de revista. El Explorer-critic identificó 6 condiciones que deben satisfacerse antes de iniciar la construcción del corpus.

---

## FUENTES EVALUADAS — RANKING FINAL

| Rank | Fuente | Grado | Acceso | Notas |
|------|--------|-------|--------|-------|
| 1 | Jurisprudencia Nacional Sistematizada (JNS) — Poder Judicial | A | Gratuito | Mayor repositorio; búsqueda por palabras clave; cobertura 2010–2024 incompleta en primeros años |
| 2 | El Peruano — Sentencias en Casación | A | Gratuito | Oficial; texto nativo; solo casaciones publicadas (~20-30% del total) |
| 3 | LP Pasión por el Derecho | A* | Gratuito | Curado; buena cobertura de hitos; no sistemático. *Grado revisado por el critic: B para corpus sistemático |
| 4 | DOXS.AI | B | Gratuito con email UCV | IA con cobertura no verificada; solo búsqueda exploratoria complementaria |
| 5 | SPIJ — colecciones temáticas | B | Gratuito (PDF); búsqueda requiere suscripción | Verificar acceso institucional UCV |
| 6 | vLex Perú | B | Suscripción | Mejor interfaz de búsqueda; verificar acceso UCV |
| 7 | Diálogos con la Jurisprudencia | B/C | Suscripción | Alta calidad doctrinal; selectivo; verificar acceso UCV/Gaceta |
| 8 | Gaceta Civil & Procesal Civil | B/C | Suscripción | Enfoque procesal; valor incremental bajo si ya se tiene Diálogos |
| 9 | Google Scholar / Academia.edu | B | Gratuito | Solo fuente secundaria; útil para identificar casos vía cadena de citas |
| 10 | CEJ / SIGE (expedientes) | C | Gratuito | Solo recuperación de casos individuales por número; no sirve para descubrimiento |
| 11 | juriscivil.com | C | Suscripción | Acceso no confirmado; prioridad baja |
| 12 | CEDIE (cedie.gg) | D | Desconocido | Sin presencia verificable; no usar |

---

## ESTRATEGIA DE TRES FUENTES (Explorer)

### Fase 1 — Descubrimiento primario (JNS)
Búsquedas en `jurisprudencia.pj.gob.pe` con todos los términos relevantes:
- "responsabilidad civil médica"
- "responsabilidad médica"  
- "lex artis" / "lex artis ad hoc"
- "consentimiento informado"
- "mala praxis" / "negligencia médica"
- "daño médico"

Filtros: Sala Civil Permanente y Sala Civil Transitoria, Corte Suprema, 2010–2024.  
Meta: 40–80 decisiones candidatas.

### Fase 2 — Verificación de publicación oficial (El Peruano)
Contrastar todas las decisiones identificadas en JNS con `busquedas.elperuano.pe`. Las decisiones publicadas en El Peruano reciben cita oficial: "CAS. XXXX-YYYY-ZZZ (Sala Civil Permanente), El Peruano, [fecha]".

### Fase 3 — Control de completitud (LP + DOXS.AI)
LP Pasión: identificar decisiones hito no capturadas por búsqueda de palabras clave.  
DOXS.AI (con email UCV): solo como barrido exploratorio suplementario — no como fuente de verificación.

### Fase 4 — Sistematización del corpus
Registrar cada decisión en `data/raw/corpus_index.csv`.

---

## EVALUACIÓN DEL CRITIC (5 PUNTOS)

### JNS — Jurisprudencia Nacional Sistematizada

| Dimensión | Hallazgo | Severidad |
|-----------|----------|-----------|
| Validez de medición | PDFs escaneados vs. texto nativo no discutidos; cobertura 2010-2014 heterogénea en calidad de texto | Mayor |
| Selección de muestra | Sin procedimiento de verificación de cobertura; solo casaciones llegadas a Corte Suprema | Mayor |
| Validez externa | El corpus de casaciones es un corpus de "casos difíciles" (solved cases bias) — los casos resueltos en primera/segunda instancia o que se transaron no aparecen | Mayor |
| Compatibilidad | Casaciones declaradas inadmisibles contienen razonamiento mínimo; proporción de decisiones de fondo desconocida | Moderada |
| Problemas conocidos | Interfaz inestable; sin operadores booleanos; sin metadatos estructurados por resultado | Moderada |

### El Peruano

| Dimensión | Hallazgo | Severidad |
|-----------|----------|-----------|
| Validez de medición | Texto nativo, alta calidad; sesgo de publicación (solo decisiones "de interés general") | Moderada |
| Selección de muestra | Solo 20-30% de total de casaciones publicadas aquí | Mayor |
| Validez externa | Sobrerepresenta decisiones doctrinalmente significativas | Moderada |
| Compatibilidad | Excelente para doctrinal coding — texto legible y estructurado | Nula (no hay problema) |
| Problemas conocidos | Archivo digital pre-2015 incompleto; puede requerir consulta física para 2010-2014 | Moderada |

### LP Pasión por el Derecho

| Dimensión | Hallazgo | Severidad |
|-----------|----------|-----------|
| Validez de medición | Capa editorial (sumillas) entre el investigador y el texto — no usar sumillas para codificación | Moderada |
| Selección de muestra | Cobertura temática no verificada para "responsabilidad civil médica" específicamente; mejor cobertura en años recientes que en 2010-2015 | Mayor |
| Validez externa | Sesgo editorial hacia decisiones "interesantes"; no representativo de aplicaciones rutinarias de doctrina | Mayor |
| Compatibilidad | Útil para identificación de casos hito; no suficiente para corpus sistemático | Moderada |
| Problemas conocidos | Límite entre contenido gratuito y suscripción no documentado | Menor |

---

## 6 CONDICIONES DE CREDIBILIDAD DEL CORPUS (Explorer-critic)

Estas condiciones deben satisfacerse antes de iniciar la construcción del corpus. Son requisitos, no sugerencias, para que el artículo supere la revisión por árbitros.

### Condición 1 — Protocolo de búsqueda documentado *(BLOQUEANTE)*
Antes de la construcción del corpus, documentar y pre-registrar (como mínimo en la sección de metodología del artículo):
- Los términos de búsqueda exactos aplicados a cada fuente
- Los filtros usados (materia, sala, rango de fechas)
- Los criterios de inclusión/exclusión para las decisiones recuperadas
- El protocolo debe ser suficiente para que otro investigador replique la búsqueda y obtenga un corpus sustancialmente similar.

### Condición 2 — Verificación de cobertura *(BLOQUEANTE)*
Contravalidar la cobertura de JNS para al menos un año calendario del período 2010-2015 respecto de las separatas de El Peruano de ese año. Si la cobertura de JNS de casaciones Sala Civil es inferior al 80% de lo publicado en El Peruano para ese año de verificación, cuantificar y divulgar la brecha.

### Condición 3 — Tasa de decisiones de fondo
Reportar qué porcentaje de las casaciones recuperadas son decisiones de fondo (fundado, infundado) versus rechazos de umbral (inadmisible, improcedente). Si más del 40% son rechazos de umbral, reportar el tamaño efectivo del corpus analítico por separado del tamaño bruto.

### Condición 4 — Clasificación de calidad de texto
Clasificar las decisiones recuperadas por tipo de texto (PDF nativo vs. PDF escaneado). Reportar la proporción de cada tipo. Las decisiones codificadas desde PDFs escaneados deben pasar verificación secundaria antes de su inclusión.

### Condición 5 — Búsqueda en repositorios de tesis peruanas
Buscar en ALICIA (alicia.concytec.gob.pe), el Repositorio PUCP, y el Repositorio UNMSM si existe alguna tesis que haya construido un corpus similar de casaciones sobre responsabilidad civil médica. Si existe, posicionar el artículo relativamente a esa tesis, no afirmar ser el primer censo.

### Condición 6 — Declaración del nivel jurisdiccional del corpus
Declarar explícitamente en la metodología si el corpus se limita a casaciones de la Corte Suprema o incluye decisiones de Cortes Superiores. Si se limita a la Corte Suprema, todas las afirmaciones sobre "criterios jurisprudenciales" deben acotarse a la doctrina casatoria. Si se incluyen Cortes Superiores, documentar qué distritos judiciales están cubiertos y reconocer que esa cobertura es incompleta.

---

## NOTA SOBRE EL HALLAZGO "SIN CENSO PREVIO"

El Explorer afirma que no existe un estudio previo con un censo sistemático de casaciones peruanas sobre responsabilidad civil médica. Esta afirmación es **plausible pero no verificada** — el Explorer no buscó en ALICIA (CONCYTEC), Repositorio PUCP, ni Repositorio UNMSM, donde es común encontrar tesis de grado o maestría con corpora de 15–30 casaciones como base empírica.

**Antes de afirmar en el artículo que se trata del primer análisis sistemático**, ejecutar la búsqueda en:
- ALICIA: `alicia.concytec.gob.pe` → "responsabilidad civil médica" + "jurisprudencia" + "casaciones"
- PUCP: `repositorio.pucp.edu.pe`
- UNMSM: `cybertesis.unmsm.edu.pe`
- UCV: `repositorio.ucv.edu.pe`

Si existe trabajo previo, reposicionar la contribución como: análisis más refinado, período actualizado, marco analítico diferente — no como primer censo.

---

## SCORE FINAL

| Categoría | Deducción |
|-----------|-----------|
| Validez de medición — calidad de texto no discutida | -10 |
| Selección de muestra — sin protocolo de verificación de cobertura | -20 |
| Validez externa — filtro de casación no discutido | -5 |
| Fuentes alternativas — ALICIA/repositorios no explorados | -15 |
| Factibilidad práctica — sin protocolo, sin deduplicación | -10 |
| Compatibilidad de identificación — proporción inadmisibles no abordada | -5 |
| **Total deducciones** | **-65** |
| **Score final** | **35/100** |
| **Veredicto** | **FAIL (umbral: 75)** |

---

## PRÓXIMOS PASOS RECOMENDADOS

El Explorer-critic es explícito: **no hay problemas de fuentes — hay un problema de documentación metodológica**. Los pasos para resolver el FAIL no requieren buscar nuevas fuentes, sino diseñar el protocolo antes de ejecutar la búsqueda.

1. **Inmediato:** Diseñar y documentar el Protocolo de Búsqueda del Corpus (Condición 1) como parte de la sección de metodología de la sección 02 del artículo. Guardar como `data/raw/search_protocol.md`.
2. **Al iniciar construcción del corpus:** Ejecutar verificación de cobertura JNS vs. El Peruano para un año de verificación (Condición 2).
3. **Antes de redactar la introducción:** Verificar en ALICIA y repositorios PUCP/UNMSM la existencia de censos previos (Condición 5).
4. **Al completar el corpus:** Reportar tasa de decisiones de fondo y calidad de texto (Condiciones 3 y 4).
5. **En la metodología del artículo:** Declarar explícitamente que el corpus se limita a casaciones de la Corte Suprema (Condición 6).

---

*Agente Explorer: primera evaluación completada*  
*Agente Explorer-critic: revisión y score: 35/100 — FAIL*  
*Fecha: 2026-05-21*
