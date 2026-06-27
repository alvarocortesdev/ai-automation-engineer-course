---
ejercicio_id: fase-6/ruteo-y-medidor-costo
fase: fase-6
sub_unidad: "6.16"
version: 1
---

# Rúbrica — Medidor de costo en vivo + router de modelos

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector evalúa el **proceso**
> (¿calculó a mano antes de codear?) y la **comprensión** (¿la reflexión explica el premium del
> cache write?), no solo si los tests pasan. Lee la solución de referencia **al final**, cuando
> ya formaste tu propio juicio.

## Objetivos evaluados

- **O1** — Calcular el USD por request desde `usage` con las tres tarifas de input + output.
- **O2** — Rutear barato→caro, manejando el borde exacto y el fuera de rango.
- **O3** — Agregar el costo mensual reusando medidor + router, con desglose por modelo.
- **O4** — Explicar por qué cachear de un solo uso pierde plata y cuándo el ruteo barato degrada.

## Criterios y niveles

### C1 — Corrección del costo (las tres tarifas) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No pasa los tests; o suma `cache_read` a `input_tokens` y lo cobra a 1×; o ignora `cache_creation`. |
| **en-progreso** | Cuenta input/output bien pero trata mal una tarifa de cache (read a 1×, o write como si fuera read). |
| **competente** | Todos los tests de costo verdes: input 1.0×, cache_read 0.1×, cache_write 1.25×, output a su precio; 0 tokens = 0.0. |
| **excelente** | Además calcula las cuatro componentes por separado y legibles; o añade un test propio con `cache_write` mayor que 0. |

### C2 — Ruteo barato→caro · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Devuelve siempre el mismo modelo, o ignora la dificultad, o no maneja el fuera de rango. |
| **en-progreso** | Rutea bien el caso medio pero falla el **borde exacto** (`dificultad == techo`) o el fuera de rango. |
| **competente** | Borde exacto entra en el escalón (`techo >= dificultad`), fuera de rango → último, escalones vacío → ValueError. |
| **excelente** | Comenta que la señal de dificultad viene de heurísticas/clasificador y que el router debe evaluarse. |

### C3 — Agregación mensual y reuso · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `costo_mensual`, o reimplementa la fórmula de costo en vez de llamar a `costo_usd`. |
| **en-progreso** | Devuelve el total pero no el desglose por modelo, o no acumula requests del mismo modelo. |
| **competente** | Reusa `costo_usd` + `rutear_modelo`, devuelve `{"total", "por_modelo"}` y acumula bien por modelo. |
| **excelente** | Estructura limpia (un acumulador dict), y la reflexión lo conecta con "la cuenta para el cliente / budget del capstone". |

### C4 — Comprensión demostrada (proceso + reflexión) · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `prediccion.md` o `verificacion.md` ausentes; o la predicción está calcada de la salida real. |
| **en-progreso** | Predijo, pero la reflexión dice "el cache write es caro" sin el porqué (el 1.25×) ni el riesgo del ruteo barato. |
| **competente** | `prediccion.md` antes de ejecutar con las cuentas; reflexión explica que cache write a 1.25× pierde plata si no se relee, y que ruteo barato degrada si subestima la dificultad. |
| **excelente** | Conecta con el budget de costo/latencia del capstone o con calibrar el router/umbral con el eval (6.9). |

## Errores típicos a marcar

- **Sumar `cache_read_input_tokens` a `input_tokens`** y cobrarlo a 1× → el ahorro del cache desaparece del número; `test_cache_read_cuesta_un_decimo` lo atrapa.
- **Tratar `cache_creation` como input fresco** (olvidar el 1.25×) → `test_cache_write_tiene_premium` lo atrapa.
- **Dividir por 1000 en vez de 1e6** (confundir "por mil" con "por millón"): costo 1000× mal.
- **Borde del router con `<` en vez de `<=`** → `dificultad == techo` cae al escalón equivocado.
- **`costo_mensual` que reimplementa la fórmula** en vez de reusar `costo_usd`: duplicación que se desincroniza.
- **`costo_mensual` que casa por posición** o pierde el desglose por modelo.
- (transversal) Hardcodear precios reales dentro de la función en vez de usar los inyectados.

## Señales de dependencia-IA

> Describir sin acusar; proponer una verificación.

- Implementación correcta pero `prediccion.md` ausente o idéntica a la salida real (calculó "después").
- `verificacion.md` usa "el cache es caro de escribir" como eslogan pero no puede decir, en una pregunta de seguimiento, **cuánto** (el 1.25×) ni cuándo paga (releer muchas veces).
- **Verificación sugerida:** pedir que calcule a mano el costo de una request con `cache_write = 5000`, `input = 0`, `output = 0` en opus, y que diga si convino cachear si ese prefijo se usa una sola vez.

## Feedback sugerido (graduado)

> Nunca pegar el código de la solución.

- **Pista (nivel 1):** "¿Estás cobrando los `cache_read_input_tokens` al mismo precio que el input fresco? Revisa el multiplicador de cada tarifa."
- **Pregunta socrática (nivel 2):** "Si el cache write cuesta 1.25× y el read 0.1×, ¿cuántas veces tienes que **leer** un prefijo para que cachearlo salga a cuenta?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Calcula las cuatro componentes por separado (`tokens/1e6 * precio * multiplicador`) y súmalas. Para el router, itera de menor a mayor y devuelve el primero con `techo >= dificultad`; si el bucle no encuentra, el último. Para `costo_mensual`, por request: rutea, busca precio, suma `costo_usd`, y lleva un dict acumulador por modelo."

## Conexión con el proyecto / capstone

- Este medidor es la base del **budget de costo/latencia** que el **Capstone F6 (RAG de producción)** exige como entregable de primera clase: medir el USD por consulta en vivo y justificar la elección de modelo por tarea en un ADR, con el budget actuando como gate junto al eval de 6.9.
