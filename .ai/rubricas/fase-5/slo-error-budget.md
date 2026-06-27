---
ejercicio_id: fase-5/slo-error-budget
fase: fase-5
sub_unidad: "5.10"
version: 1
---

# Rúbrica — SLO, error budget y la decisión de desplegar

> Rúbrica **analítica** atada a los `objetivos` del contrato. Es un ejercicio de razonamiento sin tests: la parte aritmética (budget) tiene respuesta correcta; las partes de juicio (decisión, qué alertar) se evalúan por la **lógica**, no por una única respuesta. Contrasta contra `.ai/soluciones/fase-5/slo-error-budget.md`.

## Objetivos evaluados

- O1: Distinguir SLI / SLO / error budget y calcular el budget (peticiones y tiempo).
- O2: Decidir el despliegue justificándolo con el budget restante.
- O3: Distinguir RED de USE y elegir qué alertar (síntoma, no causa).

## Criterios y niveles

### C1 — Conceptos y aritmética del budget · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Confunde SLI/SLO/budget (o los llama "SLA"); el cálculo del budget está mal (no es 0.1% × 2M = 2.000) o no lo intenta. |
| **en-progreso** | Distingue los términos pero el número falla (calcula 0.01%, o no convierte a minutos), o define el SLO sin condición de latencia. |
| **competente** | SLI/SLO/budget bien distinguidos; budget = 2.000 peticiones y ~43 min, con la aritmética a la vista. |
| **excelente** | Además define el SLI con precisión (request-based, condición 2xx **y** menor que 300 ms) y justifica p99 vs promedio con un ejemplo numérico propio. |

### C2 — Decisión basada en el budget · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Decide por intuición ("mejor no", "dale") sin mencionar el budget restante. |
| **en-progreso** | Calcula 500 / 25% restante pero la decisión no se conecta con ese número, o ignora que la feature "suele causar incidentes". |
| **competente** | Justifica con el budget restante (25%) y el riesgo de la feature; decisión coherente con el número. |
| **excelente** | Propone mitigación concreta (canary / feature flag / rollback, vigilar burn-rate) en vez de un sí/no binario; razona en términos de "cuenta corriente". |

### C3 — RED vs USE y qué alertar · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue RED de USE; elige alertar una causa sin impacto (CPU 75%) "porque suena peligroso". |
| **en-progreso** | Distingue RED/USE pero el ejemplo de relación es flojo, o duda en la alerta correcta. |
| **competente** | RED = síntoma del usuario (latencia/errores), USE = causa en el recurso (saturación del pool/CPU); alerta sobre (b) el budget quemándose. |
| **excelente** | Articula la regla "alerta síntomas, no causas" y descarta (a)(c)(d) una por una; menciona fatiga de alertas o burn-rate alerts. |

## Errores típicos a marcar

- Usar **SLA** como sinónimo de SLO (el SLA es el contrato con consecuencias; el SLO es la meta interna).
- Calcular el budget como 0.01% en vez de 0.1%, o no convertirlo a minutos.
- Definir el SLO solo como "disponibilidad" y olvidar la condición de **latencia** del enunciado.
- Decidir el despliegue sin aterrizar el budget restante (intuición disfrazada).
- Alertar sobre **causas sin impacto** (CPU al 75%) en vez del síntoma/budget → fatiga de alertas.
- Definir el umbral de latencia sobre el **promedio** (lo correcto es p95/p99).

## Señales de dependencia-IA

- Usa jerga avanzada (burn-rate multiwindow, multi-SLO) pero no hace la aritmética básica del budget.
- Da "~43 minutos" exacto sin mostrar la conversión (30 días → 43.200 min → 0.1%).
- Respuestas pulidas en las partes de juicio que no calzan con un error en la parte numérica (señal de copiar-pegar sin entender).

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Antes de decidir nada, pon el budget en números: ¿cuántas peticiones es el 0.1% de 2.000.000, y cuántas te quedan tras los 1.500 fallos?"
- **Pregunta socrática (nivel 2):** "Si el error budget es una cuenta corriente y te queda el 25%, ¿gastarías ese saldo en algo que 'suele causar incidentes'? / La CPU está al 75% pero ningún usuario se queja: ¿eso es un problema o una observación?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Budget = 0.1% × 2M = 2.000 peticiones (~43 min/mes); restante = 500 (25%). Se alerta el **síntoma que rompe la promesa** (budget quemándose), no la causa interna sin impacto (CPU). RED es la mirada del usuario, USE la de la máquina. Revisa la sección 4.6–4.7 de la lección."

## Conexión con el proyecto / capstone

- El SLO + error budget que defines aquí es el marco con el que operarás el servicio con usuarios reales del Capstone F5, y la semilla de la "historia de falla en producción" del track de empleabilidad: sin un SLO, no hay forma honesta de decir si un incidente fue grave.
