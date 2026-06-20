# TASKS

## En progreso

- [ ] **[DATA-1]** Verificar variable de ingreso en ENAHO 2019 (`lookfor ingreso` en módulo 500)
- [ ] **[DATA-2]** Descargar ENAHO Módulo 500: años 2005–2018, 2020–2024 (19 archivos desde INEI Microdatos)

## Pendiente — Datos

- [ ] **[DATA-3]** Construir panel ENAHO 2004–2024 (`scripts/stata/01_build_panel.do`)
- [ ] **[DATA-4]** Verificar consistencia de p506 en todos los años del panel
- [ ] **[DATA-5]** Deflactar ingreso laboral con IPC (base 2019)
- [ ] **[DATA-6]** Estadísticas descriptivas pre/post por grupo (`scripts/stata/02_descriptives.do`)

## Pendiente — Análisis

- [ ] **[EST-1]** DiD principal: `reghdfe log_ingreso did, absorb(anio conglome) vce(cluster conglome)`
- [ ] **[EST-2]** Event study: `reghdfe log_ingreso ib2020.anio#i.tratado ...`
- [ ] **[EST-3]** Gráfico event study con coefplot (`paper/figures/event_study/`)
- [ ] **[EST-4]** Heterogeneidad: por género, región, tamaño de establecimiento
- [ ] **[EST-5]** Margen extensivo: efecto sobre probabilidad de empleo agrícola
- [ ] **[EST-6]** Robustez: placebo temporal (año base = 2015), grupos control alternativos

## Pendiente — Paper

- [ ] **[PAPER-1]** Redactar Capítulo 2: Marco legal e institucional
- [ ] **[PAPER-2]** Redactar Capítulo 4: Datos y estadísticas descriptivas
- [ ] **[PAPER-3]** Redactar Capítulo 5: Estrategia empírica
- [ ] **[PAPER-4]** Redactar Capítulo 6: Resultados principales
- [ ] **[PAPER-5]** Redactar Capítulo 7: Robustez y heterogeneidad
- [ ] **[PAPER-6]** Redactar Capítulo 8: Conclusiones

## Completado

- [x] **[DESIGN-1]** Definir pregunta de investigación
- [x] **[DESIGN-2]** Identificar grupo tratado y control con CIIU Rev.3
- [x] **[DESIGN-3]** Verificar consistencia de p506 en 2004 y 2019
- [x] **[DESIGN-4]** Verificar tamaño de muestra: 284 conglomerados control, 1782 tratado (2004)
- [x] **[DESIGN-5]** Leer Ley 27360, Ley 31110, Ley 32434 y mapear cambios
- [x] **[DESIGN-6]** Confirmar DiD estándar (no staggered) para ingresos laborales
