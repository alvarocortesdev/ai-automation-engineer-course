---
ejercicio_id: fase-7/eval-gate-agente
fase: fase-7
sub_unidad: "7.7"
version: 1
---

# Rúbrica — El eval gate de un agente

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **mixto**:
> tests automáticos (`test_eval_gate.py`) **y** un `write-up.md`. El verde de los
> tests es necesario, no suficiente: el corrector evalúa si el alumno entiende *por
> qué* la métrica de una automatización es la decisión correcta y no la fluidez, y
> *por qué* se necesita un gate de regresión además del umbral.

## Objetivos evaluados

- O1: Calcular accuracy de routing/clasificación y exactitud de extracción sobre un golden set.
- O2: Implementar un gate que bloquee por umbral fijo y por regresión vs baseline.
- O3: Explicar por qué la métrica es la decisión correcta (no la fluidez) y la diferencia eval offline vs monitoreo online.

## Criterios y niveles

### C1 — Corrección del cálculo de métricas · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; la exactitud de campos se calcula como promedio de promedios, o la lista vacía revienta por división por cero. |
| **en-progreso** | accuracy correcta pero exactitud de campos mal (no suma sobre el total global de campos esperados), o no respeta la convención de verdad vacua. |
| **competente** | Los tests de `evaluar` pasan: accuracy = correctas/n, exactitud = campos correctos / total esperado (global), lista vacía → 1.0/1.0/0. |
| **excelente** | Maneja con cuidado claves faltantes en la predicción (no cuenta como acierto), y un caso propio con campos parcialmente correctos. |

### C2 — Corrección del gate (umbral + regresión) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El gate solo mira el umbral, o no distingue umbral de regresión en el motivo. |
| **en-progreso** | Distingue umbral de regresión pero falla la frontera (accuracy igual al umbral debe pasar) o aplica regresión cuando `baseline` es `None`. |
| **competente** | Los tests de `gate` pasan: bloquea bajo umbral y por regresión por separado, frontera incluida, regresión solo con baseline. |
| **excelente** | El motivo es informativo (reporta el valor y el límite), y maneja el caso de fallar por ambos a la vez. |

### C3 — Comprensión: qué medir y por qué · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El write-up justifica el eval por la fluidez/calidad del texto, o cree que el eval offline reemplaza al monitoreo en prod. |
| **en-progreso** | Explica que importa la decisión pero no por qué la regresión necesita su propio gate. |
| **competente** | Explica que la métrica es routing/extracción (no fluidez), da un escenario donde el umbral pasa pero la regresión bloquea, y nombra el origen del golden set (trazas de prod). |
| **excelente** | Articula eval offline (gate en CI, datos fijos) vs monitoreo online (deriva, casos nuevos), y por qué se necesitan ambos. |

## Errores típicos a marcar

- Exactitud de campos como promedio de ratios por ítem en vez de fracción global (numerador/denominador totales) — da números distintos en casos desbalanceados.
- Dividir por cero en la lista vacía (no respetar la convención de verdad vacua).
- Gate que aplica regresión aunque `baseline is None`.
- Frontera mal: tratar `accuracy == umbral` como bloqueo (debe pasar).
- Motivo que no distingue "bajo umbral" de "regresión" → el operador no sabe qué pasó.
- (transversal) Evaluar el agente con métricas de chatbot (fluidez, "suena bien"); creer que un golden set se inventa en vez de salir de trazas reales.

## Señales de dependencia-IA

- Métricas correctas pero el alumno no puede explicar por qué la regresión necesita un gate aparte del umbral.
- Write-up que repite "tool-call accuracy" sin poder dar un escenario concreto de regresión que pase el umbral.
- Sofisticación impropia (menciona F1, LLM-as-judge, ragas) sin poder explicar el caso simple "accuracy = correctas / total".
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué hace el gate con accuracy 0.92, umbral 0.90 y baseline 0.95 (debe decir: bloquea por regresión). Si entendió, responde al toque; si dependió de IA, duda.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Tu agente sube de un baseline de 0.95 a... 0.92, y tu umbral es 0.90. ¿Pasa? ¿Debería? ¿Qué te dice eso sobre tener solo un umbral fijo?"
- **Pregunta socrática (nivel 2):** "Si el texto del agente ahora se lee precioso pero rutea mal 1 de cada 3 tickets, ¿es un mejor agente para una automatización? ¿Qué deberías estar midiendo?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Separa `evaluar` (calcula) de `gate` (decide). En `gate`, dos chequeos con motivos distintos: bajo umbral, y regresión (solo si hay baseline). La regresión bloquea cuando la accuracy es estrictamente menor que la del baseline. El origen del golden set (trazas de prod) está en 4.7 y conecta con la 6.9."

## Conexión con el proyecto / capstone

- Este eval gate es el **punto 5 del Definition of Done** del [capstone F7](/fase-7-automatizacion/proyecto/): eval harness versionado + número + gate de regresión + budget de costo/latencia como entregables de primera clase. Es lo que impide que el capstone degrade en silencio entre commits.
