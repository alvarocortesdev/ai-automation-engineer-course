---
ejercicio_id: fase-6/break-even-local-vs-api
fase: fase-6
sub_unidad: "6.10"
version: 1
---

# Rúbrica — Calculadora del punto de equilibrio local vs API

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con
> `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar. El
> objetivo de fondo es que el alumno entienda que **local es costo fijo y la API es costo
> variable**, y que sepa derivar de ahí cuándo conviene cada una.

## Objetivos evaluados

- **O1** — Calcular el costo por request y el costo mensual de una API (pricing por millón).
- **O2** — Calcular el punto de equilibrio en requests donde local iguala a la API.
- **O3** — Explicar por qué a volumen bajo/variable la API casi siempre gana por costo.

## Criterios y niveles

### C1 — Corrección de las funciones · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Los tests no pasan; la fórmula usa `/1000`, un solo precio para ambos lados, o el equilibrio no es la división correcta. |
| **en-progreso** | Pasan algunos tests; falla el manejo del costo-por-request 0, o `punto_equilibrio` reimplementa la fórmula con un bug sutil. |
| **competente** | Los 8 tests pasan; las tres funciones son correctas y `punto_equilibrio_requests` lanza `ValueError` ante costo por request 0. |
| **excelente** | Lo anterior + `punto_equilibrio` **reusa** `costo_api_por_request` (DRY) y el alumno añadió un test propio que captura un caso borde real. |

### C2 — Proceso Primero-Sin-IA (predicción antes de medir) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `prediccion.md`, o aparece con los mismos números que el output de los tests (predijo después de ejecutar). |
| **en-progreso** | Hay predicción pero incompleta (falta el equilibrio o el ganador a 20.000 requests). |
| **competente** | `prediccion.md` con costo por request, costo local, equilibrio y ganador a 20.000 requests, calculados a mano antes de ejecutar. |
| **excelente** | La predicción muestra el razonamiento por paso y, si tenía un error, queda la traza de cómo lo detectó al correr los tests (productive failure). |

### C3 — Comprensión demostrada (la reflexión calza) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `verificacion.md`, o afirma que "local es siempre más barato". |
| **en-progreso** | Dice que la API gana a volumen bajo pero no nombra el concepto de costo fijo vs variable. |
| **competente** | Explica que local es **costo fijo** (la GPU se paga ociosa o llena) y por eso pierde a volumen bajo/variable. |
| **excelente** | Además nombra una razón **no-costo** que justificaría local bajo el equilibrio (privacidad/cumplimiento, latencia sin red, control/disponibilidad). |

## Errores típicos a marcar

- `/1000` en vez de `/1e6` (costo 1000× inflado).
- Promediar `in` y `out` o usar un solo precio para ambos lados.
- Devolver `inf` o dejar reventar `ZeroDivisionError` en vez de `ValueError` con mensaje.
- Reimplementar la fórmula en `punto_equilibrio_requests` (deuda de diseño / no DRY).
- En la reflexión, invertir el sentido del equilibrio ("por encima gana la API").
- (transversal) perseguir que "pasen los tests" sin la predicción a mano ni la reflexión.

## Señales de dependencia-IA

- Funciones correctas y elegantes pero `prediccion.md` ausente o con números idénticos al
  test (señal de que ejecutó/usó IA antes de predecir).
- `verificacion.md` con prosa sofisticada que no se compromete ("depende del caso") sin
  nombrar costo fijo vs variable — explicación que no calza con un código correcto.
- **Verificación sugerida:** pídele que calcule de cabeza el equilibrio si la GPU costara
  el doble (1460 USD/mes). Si entendió la división, responde 1.460.000 al instante; si lo
  copió, titubea.

## Feedback sugerido (graduado)

> Ordenadas de menos a más directas. **Nunca escribir el código por el alumno.**

- **Pista (nivel 1):** "Mira el caso del README: ¿tu costo por request da 0.001? Si da
  1.0, revisa por cuánto divides — el pricing viene por millón."
- **Pregunta socrática (nivel 2):** "Si la API fuera gratis (costo por request 0),
  ¿cuántos requests necesitas para igualar una GPU de 730 USD? ¿Esa pregunta tiene
  respuesta?" (lleva al `ValueError`).
- **Dirección concreta (nivel 3, sólo tras intento real):** "El equilibrio es
  `costo_local / costo_por_request`. Tu reflexión dice que local siempre gana: revisa qué
  pasa a 20.000 requests vs el equilibrio de 730.000 — local cuesta 36× más ahí."

## Conexión con el proyecto / capstone

- Este número es el corazón del **ADR de serving** del [Capstone F6](/fase-6-ai-engineering/proyecto/):
  justifica usar una API ahora y bajo qué volumen/requisito migrarías a vLLM on-prem.
  Alimenta directo el budget de costo/latencia de
  [6.16](/fase-6-ai-engineering/6-16-costo-latencia-llmops/).
