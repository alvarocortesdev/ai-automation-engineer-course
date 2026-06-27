---
ejercicio_id: fase-5/estimador-de-costos
fase: fase-5
sub_unidad: "5.8"
version: 1
---

# Rúbrica — Estimador de costos cloud

> Rúbrica **analítica** atada a los `objetivos` del contrato. Hay tests automáticos (`test_estimador.py`):
> el verde es condición necesaria, **no suficiente**. El corrector evalúa además la **comprensión**
> (¿entiende por qué el egress lleva `max(0, …)` y por qué el always-on domina?) y la **calidad**
> (caso propio significativo, no decorativo).

## Objetivos evaluados

- O1: Estimar el costo mensual descomponiéndolo en los 4 drivers (compute, storage, egress, requests).
- O2: Tratar el tramo gratis de egress (nunca negativo) y el compute always-on vs. scale-to-zero.
- O3: Devolver un desglose por driver coherente con el total.

## Criterios y niveles

### C1 — Corrección (¿los 4 drivers y el total están bien?) · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo; falta un driver, o el `total` no es la suma del desglose. |
| **en-progreso** | Pasa la mayoría pero falla un caso (típico: egress por debajo del tramo gratis, o compute con un solo recurso "hardcodeado" en vez de sumar la lista). |
| **competente** | Los 10 tests en verde; `total == suma de los 4`; el desglose tiene exactamente las 5 claves del contrato. |
| **excelente** | Además, código limpio (sin redondeos que rompan la tolerancia, sin claves de más), y un **caso propio significativo** (escenario viral donde domina el egress, o sin NAT). |

### C2 — Comprensión del modelo de costo (el corazón del ejercicio) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Cobra todo el egress sin tramo gratis, o el egress puede salir negativo, o no distingue horas encendido. |
| **en-progreso** | Aplica el tramo gratis pero no sabe explicar por qué; o pasa los tests sin entender por qué el NAT pesa 32.85 de 35.48. |
| **competente** | Usa `max(0, egress_gb - gratis)` con intención; explica que el compute cobra por horas encendido (always-on vs. scale-to-zero). |
| **excelente** | Explica el trade-off VM 24/7 vs. scale-to-zero por **patrón de tráfico**, y reconoce que el storage casi nunca es el balde a optimizar primero. |

### C3 — Calidad de testing (hilo transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No añadió ningún test propio. |
| **en-progreso** | Añadió un test trivial (repite un caso existente con otros números). |
| **competente** | Añadió un caso borde real (egress dominante, o NAT removido) con una aserción que prueba algo nuevo. |
| **excelente** | El caso propio ilustra una **decisión de costo** (p. ej. demuestra cuánto baja el total al quitar el NAT always-on). |

## Errores típicos a marcar

- Cobrar todo el egress sin descontar el tramo gratis (sobre-estima y asusta sin razón).
- Egress negativo por no usar `max(0, …)`.
- Hardcodear un solo recurso de compute en vez de sumar la lista (rompe con 2+ recursos).
- Redondear dentro de la función y romper la comparación con tolerancia (no hace falta redondear).
- Calcular el `total` por separado en vez de sumar el desglose (puede divergir).
- (transversal) Perseguir que "pasen los tests" sin poder explicar por qué el NAT domina el total.

## Señales de dependencia-IA

- Función impecable y genérica pero el alumno no puede decir por qué el caso de ejemplo da 35.48 ni qué línea pesa más.
- Caso de prueba propio sospechosamente sofisticado (tiers de egress múltiples, descuentos por reserva) impropio del nivel, e indefendible.
- Comentarios que explican *qué* hace cada línea pero no *por qué* el tramo gratis importa.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "¿Qué pasa con tu función de egress cuando sirves 80 GB y el tramo gratis es 100? Corre ese caso a mano antes de mirar el test."
- **Pregunta socrática (nivel 2):** "En el caso de ejemplo, ¿cuál de los dos recursos de compute pesa más en el total, y por qué uno con 730 horas cambia tanto la cifra?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El egress se cobra solo por encima del tramo gratis: `max(0, egress_gb - egress_gratis_gb) * precio`. El `max` evita el negativo. El compute es la suma de `usd_por_hora * horas_encendido` sobre la lista; por eso el NAT con 730 horas (always-on) domina. Revisa la sección 6 de la lección."

## Conexión con el proyecto / capstone

- La cifra que produce este estimador es el **boceto de presupuesto** del [capstone F5](/fase-5-devops/proyecto/) y alimenta el write-up de trade-offs. El mismo patrón (estimar antes, poner tope) es el techo de costo de un agente de IA en F6/F7.
