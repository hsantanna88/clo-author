# Perfiles de evaluación

<!--
Calibran al domain-referee y al methods-referee. Reemplazan a los perfiles de revistas de
economía de la plantilla clo-author (archivados en .template-reference/journal-profiles-economia.md).
Usados por: domain-referee.md, methods-referee.md, editor.md (vía /review --peer [perfil])
-->

## Cómo funciona

1. **El editor hace la revisión de entrada** → decide si el documento está listo para evaluación
2. **El editor selecciona evaluadores** → toma disposiciones del *pool* del perfil
3. **Perfil encontrado** → los evaluadores se calibran con él
4. **Perfil no encontrado** → usan el nombre del venue más `domain-profile.md`
5. **Sin perfil especificado** → se usa **Jurado de tesis (UD)**, el perfil por defecto

Disposiciones disponibles: EXPERIMENTAL, TEORICO, IMPLEMENTACION, APLICACION, REPRODUCIBILIDAD,
ESCEPTICO. Los dos evaluadores siempre reciben disposiciones DISTINTAS.

| Disposición | Qué le importa |
|-------------|----------------|
| EXPERIMENTAL | Protocolo, repeticiones, condiciones controladas, validez de la comparación |
| TEORICO | Formulación, estabilidad, convergencia, corrección de las derivaciones |
| IMPLEMENTACION | Calidad del código, tiempo real, manejo del hardware, ingeniería |
| APLICACION | Utilidad práctica, transferibilidad a plantas reales, justificación del enfoque |
| REPRODUCIBILIDAD | ¿Puede otro repetir esto? Semillas, versiones, datos, documentación |
| ESCEPTICO | Busca la afirmación exagerada, el baseline débil, el resultado que no se sostiene |

### Convención de tablas

Todas las tablas usan `booktabs` sin líneas verticales. Las métricas de desempeño se reportan con
**unidades explícitas** y, cuando provienen de hardware, como **media ± desviación estándar sobre
N corridas** con N declarado (INV-4). No se usan estrellas de significancia: esta no es una
disciplina de contraste de hipótesis sobre muestras observacionales.

---

## Perfil por defecto

### Jurado de tesis — Universidad Distrital Francisco José de Caldas (Ing. de Sistemas, pregrado)

**Foco:** Que el estudiante demuestre dominio del problema, método coherente con los objetivos, y
resultados obtenidos y reportados con honestidad.

**Barra:** Competencia técnica y rigor experimental. **No** se exige contribución original al
estado del arte: se exige que el trabajo esté bien hecho, bien justificado y bien documentado.

**El evaluador de dominio ajusta:** Verifica que los objetivos declarados en el anteproyecto se
cumplan uno a uno. Que el marco teórico sustente las decisiones tomadas, no que sea una enciclopedia.
Que el estudiante sepa explicar *por qué* eligió cada componente. Valora la aplicación correcta de
conocimiento establecido por encima de la novedad.

**El evaluador de métodos ajusta:** Revisa que el modelo esté validado contra datos independientes,
que el LQR se haya diseñado sobre un sistema verificado como controlable, que la comparación entre
controladores sea justa, y que las métricas tengan unidades y dispersión. Penaliza fuerte la
afirmación no respaldada por el experimento; penaliza poco la ausencia de garantías teóricas
avanzadas.

**Preocupaciones típicas:**
- "¿Cumplió los objetivos específicos del anteproyecto?"
- "¿Por qué eligió este método y no otro? Justifíquelo."
- "¿Qué pasa si cambia las condiciones de operación?"
- "¿Este resultado se repite o lo corrió una sola vez?"
- "Explique esta ecuación." (dominio conceptual, no solo implementación)
- "¿Qué limitaciones tiene su trabajo?" — reconocerlas suma, ocultarlas resta

**Pool de evaluadores:** EXPERIMENTAL (alto), APLICACION (alto), REPRODUCIBILIDAD (medio),
IMPLEMENTACION (medio), TEORICO (bajo), ESCEPTICO (bajo)

**Severidad:** Media. Formativa antes que punitiva. Un hallazgo se reporta con la corrección
concreta, no solo con el reproche.

---

## Venues para un artículo derivado

Aplican solo si más adelante se deriva un artículo de la tesis. **No** se usan para evaluar el
documento de grado.

### IEEE Transactions on Control Systems Technology (TCST)
**Foco:** Control aplicado a sistemas reales, con validación experimental.
**Barra:** La aplicación debe resolver un problema de ingeniería real y la validación debe ser sobre hardware, no solo simulación.
**Dominio ajusta:** Exige que el problema tenga relevancia industrial o práctica más allá de lo didáctico. Una planta de laboratorio como el TCLab necesita argumentar por qué sus conclusiones transfieren.
**Métodos ajusta:** Resultados experimentales rigurosos, comparación contra baselines bien sintonizados, análisis de robustez.
**Preocupaciones:** "¿Esto funciona fuera del laboratorio?" "¿El baseline está bien sintonizado?" "¿Qué tan sensible es al modelo?"
**Pool:** EXPERIMENTAL (alto), APLICACION (alto), ESCEPTICO (medio), IMPLEMENTACION (medio), TEORICO (bajo), REPRODUCIBILIDAD (bajo)

### Control Engineering Practice (IFAC)
**Foco:** Práctica de la ingeniería de control; aplicaciones y lecciones de implementación.
**Barra:** Contribución práctica demostrable. Acepta plantas de escala reducida si la lección es transferible.
**Dominio ajusta:** Valora el reporte honesto de dificultades de implementación. La sección de "lecciones aprendidas" cuenta.
**Métodos ajusta:** Menos exigente en formalismo, más en evidencia experimental y en el detalle de la puesta en marcha.
**Preocupaciones:** "¿Qué aprendió alguien que quiera implementar esto?" "¿Reporta los problemas o solo los éxitos?"
**Pool:** APLICACION (alto), IMPLEMENTACION (alto), EXPERIMENTAL (medio), REPRODUCIBILIDAD (medio), ESCEPTICO (bajo), TEORICO (bajo)

### ISA Transactions
**Foco:** Instrumentación, automatización y control de procesos.
**Barra:** Aplicación sólida con validación. Tolerante con plantas de laboratorio.
**Dominio ajusta:** Contexto de control de procesos; espera comparación contra PID bien sintonizado como referencia mínima.
**Métodos ajusta:** Métricas estándar de la industria (IAE, ITAE, esfuerzo de control), análisis de robustez frente a perturbaciones.
**Preocupaciones:** "¿Comparó contra un PID bien sintonizado?" "¿Cómo se comporta ante perturbaciones de carga?"
**Pool:** EXPERIMENTAL (alto), APLICACION (medio), IMPLEMENTACION (medio), ESCEPTICO (medio), TEORICO (bajo), REPRODUCIBILIDAD (bajo)

### Journal of Process Control
**Foco:** Control de procesos, con peso en modelado e identificación.
**Barra:** Rigor en el modelado. La identificación del sistema recibe tanto escrutinio como el controlador.
**Dominio ajusta:** El modelo es el centro. Espera validación cruzada, análisis de incertidumbre y discusión del punto de operación.
**Métodos ajusta:** Escrutinio detallado del procedimiento de identificación, del orden del modelo y de la validez de la linealización.
**Preocupaciones:** "¿Cómo validó el modelo?" "¿Qué pasa fuera del punto de linealización?" "¿Cuantificó la incertidumbre del modelo?"
**Pool:** TEORICO (alto), EXPERIMENTAL (alto), ESCEPTICO (medio), APLICACION (bajo), IMPLEMENTACION (bajo), REPRODUCIBILIDAD (bajo)

### Automatica
**Foco:** Teoría de control y sistemas.
**Barra:** Contribución teórica sustancial. **Fuera de alcance para una tesis de pregrado aplicada.**
**Dominio ajusta:** Exige un resultado formal nuevo. La aplicación por sí sola no basta.
**Métodos ajusta:** Demostraciones completas, condiciones de regularidad explícitas, análisis de estabilidad y convergencia.
**Preocupaciones:** "¿Dónde está el teorema?" "¿Qué garantiza la estabilidad del lazo cerrado?"
**Pool:** TEORICO (alto), ESCEPTICO (alto), EXPERIMENTAL (bajo), APLICACION (bajo), IMPLEMENTACION (bajo), REPRODUCIBILIDAD (bajo)

### IFAC-PapersOnLine (congresos IFAC)
**Foco:** Actas de congresos IFAC. Trabajo en curso y resultados preliminares.
**Barra:** Más accesible. Buen destino para un primer resultado derivado de la tesis.
**Dominio ajusta:** Acepta alcance acotado si la idea es clara y el resultado honesto.
**Métodos ajusta:** Exige corrección, no exhaustividad. Límite estricto de páginas.
**Preocupaciones:** "¿Es claro y correcto?" "¿Cabe en el límite de páginas?"
**Pool:** APLICACION (alto), EXPERIMENTAL (medio), TEORICO (medio), IMPLEMENTACION (medio), ESCEPTICO (bajo), REPRODUCIBILIDAD (bajo)

### IEEE Access
**Foco:** Multidisciplinar, acceso abierto, revisión rápida.
**Barra:** Solidez técnica y novedad razonable. Menos selectivo que TCST.
**Dominio ajusta:** Requiere posicionamiento claro frente a la literatura reciente.
**Métodos ajusta:** Corrección técnica y reproducibilidad; menos exigente en profundidad teórica.
**Preocupaciones:** "¿Está bien posicionado frente a trabajos recientes?" "¿Es reproducible?"
**Pool:** REPRODUCIBILIDAD (alto), EXPERIMENTAL (medio), APLICACION (medio), IMPLEMENTACION (medio), TEORICO (bajo), ESCEPTICO (bajo)

---

## Agregar otro perfil

```markdown
### [Nombre del venue]
**Foco:**
**Barra:**
**Dominio ajusta:**
**Métodos ajusta:**
**Preocupaciones:**
**Pool:** [disposición (alto/medio/bajo) x6]
```
