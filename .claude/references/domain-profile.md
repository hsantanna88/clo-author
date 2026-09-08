# Perfil de dominio

<!--
Todos los agentes leen este archivo para calibrar su comportamiento según el campo.
Este perfil reemplaza al de economía empírica que traía la plantilla clo-author.
-->

## Campo

**Principal:** Control automático — control óptimo y aprendizaje por refuerzo aplicados a procesos térmicos
**Subcampos adyacentes:** Identificación de sistemas, control de procesos, control adaptativo, RL seguro
**Nivel del trabajo:** Trabajo de grado de pregrado (Ingeniería de Sistemas, Universidad Distrital Francisco José de Caldas)

**Advertencia de calibración:** este es un trabajo de pregrado, no un artículo para *Automatica*.
Los críticos exigen rigor experimental y honestidad en las afirmaciones, no contribución teórica
novedosa. Un LQR bien identificado, bien sintonizado y honestamente comparado es un resultado
válido; un teorema nuevo no es el estándar.

---

## Planta de estudio: TCLab

| Aspecto | Descripción |
|---------|-------------|
| Qué es | Temperature Control Lab: shield sobre Arduino con dos calentadores (transistores) y dos sensores de temperatura (TMP36) |
| Estructura | MIMO 2x2 con acoplamiento térmico cruzado entre calentadores |
| Entradas | $Q_1, Q_2 \in [0, 100]\%$ (PWM sobre los calentadores) |
| Salidas | $T_1, T_2$ en °C |
| Dinámica | No lineal (radiación $\propto T^4$ y convección), con retardo de transporte, constantes de tiempo del orden de minutos |
| Perturbaciones | Temperatura ambiente, corrientes de aire, deriva térmica acumulada entre corridas |
| Restricciones | Saturación del actuador; límite térmico de seguridad; el disipador retiene calor entre experimentos |

**Consecuencias prácticas que los agentes deben respetar:**

- Los experimentos ocurren en **tiempo real** y son lentos. Una corrida de identificación o una
  evaluación de política toman minutos u horas. No se pueden acelerar sobre el hardware.
- Entre corridas hay que **esperar el enfriamiento** hasta la temperatura ambiente, o la condición
  inicial contamina la comparación.
- El entrenamiento de RL sobre la placa física es inviable por el número de episodios requerido.
  De ahí la necesidad del simulador y del análisis sim-to-real.

---

## Protocolos de excitación y adquisición

<!-- Reemplaza a "fuentes de datos" del perfil de economía. Los datos aquí se generan, no se buscan. -->

| Protocolo | Uso | Notas |
|-----------|-----|-------|
| Escalón (step test) | Identificación FOPDT inicial | Simple e interpretable; sensible al punto de operación |
| Escalones múltiples | Verificar no linealidad | Ganancia y constante de tiempo varían con la temperatura |
| PRBS | Identificación paramétrica (ARX/ARMAX/subespacios) | Excita un rango amplio de frecuencias; requiere elegir bien el periodo de reloj |
| Multi-seno | Identificación en frecuencia | Control fino del contenido espectral |
| Doblete / pulso | Validación cruzada del modelo | Nunca identificar y validar con la misma corrida |

**Regla:** los datos de identificación y los de validación provienen de corridas distintas.

---

## Enfoques de modelado

| Enfoque | Aplicación típica | Supuesto clave a defender |
|---------|------------------|--------------------------|
| Balance de energía (primeros principios) | Modelo físico con capacidad térmica, convección y radiación | Los parámetros físicos son identificables a partir de los datos disponibles |
| FOPDT | Punto de partida y sintonía clásica | El sistema opera cerca de un punto de equilibrio; el retardo es aproximadamente constante |
| Espacio de estados lineal $(A,B,C,D)$ | Requisito del LQR | Linealización válida en el rango de operación considerado |
| ARX / ARMAX | Identificación paramétrica discreta | Estructura de ruido correctamente especificada |
| Subespacios (N4SID) | Identificación MIMO sin fijar estructura | Orden del sistema bien seleccionado (valores singulares) |

Para el LQR el modelo debe ser **lineal y en espacio de estados**, y debe verificarse
**controlabilidad y observabilidad** antes de diseñar. Si el estado no se mide por completo, hace
falta un observador (Luenberger o filtro de Kalman) y hay que decirlo explícitamente.

---

## Convenciones del campo

- **Declarar siempre el tiempo de muestreo** $T_s$ y justificarlo frente a la dinámica de la planta.
- **El LQR se diseña en discreto** (`dlqr` / `c2d`) cuando el controlador corre en un bucle
  muestreado, que es el caso aquí. Diseñar en continuo y discretizar después exige justificarlo.
- **Saturación del actuador explícita**: $Q_1, Q_2 \in [0,100]\%$. Un LQR sin manejo de saturación
  produce señales irrealizables; declarar cómo se trata (recorte, anti-windup, o su ausencia).
- **Reportar el esfuerzo de control**, no solo el error de seguimiento. Un controlador rápido que
  satura permanentemente no es mejor.
- **Repeticiones**: toda métrica sobre hardware se reporta como media ± desviación estándar sobre
  N corridas, con N declarado. Una sola corrida no es evidencia.
- **Semillas en RL**: mínimo N semillas independientes, con la varianza entre ellas reportada.
  Curvas de aprendizaje de una sola semilla no son resultado.
- **Condiciones ambientales**: registrar temperatura ambiente inicial en cada corrida.
- **Comparación justa**: el LQR base y la política de RL se evalúan con los mismos setpoints, el
  mismo $T_s$, la misma condición inicial y el mismo perfil de perturbación.

---

## Convenciones de notación

| Símbolo | Significado | Antipatrón |
|---------|-------------|-----------|
| $x_k \in \mathbb{R}^n$ | Vector de estado en el instante $k$ | No usar $x$ para el estado y también para una posición genérica |
| $u_k \in \mathbb{R}^m$ | Entrada de control (potencia de calentadores, %) | No mezclar $u$ con $Q$ sin definir la relación |
| $y_k \in \mathbb{R}^p$ | Salida medida (temperaturas, °C) | — |
| $(A, B, C, D)$ | Matrices del sistema en espacio de estados | Mantener discreto y continuo tipográficamente distintos: $(A_d, B_d)$ |
| $Q \succeq 0$, $R \succ 0$ | Matrices de peso del costo LQR | **No confundir con $Q_1, Q_2$, las potencias de los calentadores.** Si ambos aparecen, renombrar las potencias como $u_1, u_2$ |
| $K$ | Ganancia de realimentación, $u = -Kx$ | — |
| $P$ | Solución de la ecuación de Riccati | — |
| $J$ | Funcional de costo | — |
| $T_s$ | Tiempo de muestreo | Declarar unidades siempre |
| $r_k$ | Recompensa instantánea (RL) | No usar $r$ también para la referencia; la referencia es $y^{\mathrm{ref}}$ o $\mathrm{SP}$ |
| $\pi_\theta$ | Política parametrizada | — |
| $\gamma$ | Factor de descuento | — |

**Colisión crítica de notación:** $Q$ es a la vez la matriz de peso del LQR y la potencia de los
calentadores en la nomenclatura estándar del TCLab. Fijar una convención en el capítulo de
preliminares y sostenerla en toda la tesis (INV-7).

---

## Referencias fundamentales

<!-- El librarian asegura que se citen cuando corresponda. Verificar cada entrada antes de citar. -->

| Tema | Anclas |
|------|--------|
| LQR / control óptimo | Kalman (1960); Anderson & Moore, *Optimal Control: Linear Quadratic Methods*; Bertsekas, *Dynamic Programming and Optimal Control* |
| Fundamentos de control | Åström & Murray, *Feedback Systems*; Ogata, *Ingeniería de Control Moderna* |
| Identificación de sistemas | Ljung, *System Identification: Theory for the User* |
| RL general | Sutton & Barto, *Reinforcement Learning: An Introduction* (2.ª ed., 2018) |
| RL y LQR (puente teórico) | Bradtke et al. (control LQ adaptativo por iteración de políticas); Fazel et al. (2018, convergencia global de gradiente de políticas para LQR); Dean et al. (complejidad muestral del LQR); Recht (2019, panorama de RL desde el control continuo) |
| Algoritmos de RL continuo | Lillicrap et al. (DDPG); Schulman et al. (PPO); Haarnoja et al. (SAC) |
| RL residual | Johannink et al. (RL residual para control de robots); Silver et al. (residual policy learning) |
| RL con garantías de seguridad | Berkenkamp et al. (RL basado en modelo con garantías de estabilidad) |
| Plataforma TCLab | Literatura de Hedengren y colaboradores sobre el laboratorio de control de temperatura |

**Regla de honestidad bibliográfica:** ninguna cita se inventa. Las entradas cuyos datos exactos
(volumen, páginas, año) no estén verificados llevan la marca `% VERIFICAR` en
`Bibliography_base.bib` y se confirman con `/tools validate-bib` antes de aparecer en la tesis.

---

## Preocupaciones típicas del jurado

<!-- El domain-referee y el methods-referee vigilan estas. -->

- **"¿Por qué RL si el LQR ya resuelve el problema lineal?"** — La justificación debe ser concreta:
  no linealidad, incertidumbre del modelo, restricciones, o desempeño fuera del punto de diseño.
  "Porque es novedoso" no es una respuesta.
- **Brecha sim-to-real** — ¿Cuánto se degrada la política al pasar del simulador a la placa? Si no
  se midió, la contribución experimental está incompleta.
- **Sobreajuste al simulador** — Una política que solo funciona con el modelo con el que se entrenó
  no es un resultado de control.
- **Estabilidad del componente aprendido** — ¿Qué garantiza que la corrección aprendida no
  desestabilice el lazo? Si no hay garantía formal, decirlo abiertamente y acotar el alcance.
- **Comparación sesgada** — ¿Se sintonizó el LQR con el mismo esfuerzo que el agente de RL? Un
  baseline mal sintonizado invalida la comparación.
- **Diseño de la recompensa** — ¿La recompensa premia lo que dice premiar? Buscar *reward hacking*:
  políticas que optimizan la métrica sin controlar bien.
- **Repeticiones y semillas** — ¿Cuántas corridas? ¿Cuántas semillas? ¿Se reporta la dispersión?
- **Reproducibilidad** — ¿Puede otro estudiante repetir el experimento con lo que hay en el repo?
- **Validez del modelo** — ¿Se validó contra datos distintos de los de identificación?
- **Controlabilidad y observabilidad** — ¿Se verificaron antes de diseñar el LQR?

---

## Métricas de desempeño y tolerancias

| Métrica | Definición | Unidad |
|---------|-----------|--------|
| IAE | $\int \lvert e(t) \rvert \, dt$ | °C·s |
| ISE | $\int e^2(t) \, dt$ | °C²·s |
| ITAE | $\int t \lvert e(t) \rvert \, dt$ | °C·s² |
| Sobreimpulso | Exceso máximo sobre el setpoint | % |
| Tiempo de establecimiento | Entrada permanente a la banda del ±2 % | s |
| Error en estado estacionario | Error promedio tras el establecimiento | °C |
| Esfuerzo de control | $\int u^2(t)\,dt$ o variación total de $u$ | %²·s |
| Consumo energético | Integral de la potencia aplicada | J (o %·s) |

| Cantidad | Tolerancia | Justificación |
|----------|-----------|---------------|
| Reproducción de resultados numéricos en simulación | 1e-6 | Determinismo con semilla fija |
| Métricas sobre hardware entre corridas | Reportar dispersión; no exigir igualdad | Ruido del sensor, ambiente y deriva térmica |
| Ajuste del modelo identificado | Declarar el criterio y su valor (p. ej. FIT o $R^2$) | La calidad del modelo condiciona todo el LQR |
| Resolución del sensor TMP36 | Documentar la cuantización observada | Fija el piso del error alcanzable |

**Regla:** ninguna diferencia de desempeño se declara relevante si es menor que la dispersión
entre corridas de la misma configuración.
