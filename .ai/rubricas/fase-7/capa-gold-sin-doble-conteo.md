---
ejercicio_id: fase-7/capa-gold-sin-doble-conteo
fase: fase-7
sub_unidad: "7.5a"
version: 1
---

# Rúbrica — Construir la capa gold sin doble conteo

> Rúbrica **analítica** para un ejercicio de **código**. Los tests verdes son condición necesaria pero
> **no suficiente**: lo que se evalúa de verdad es si el alumno **entiende el fan-out** y por qué su
> solución lo evita, no si tropezó con la implementación correcta por casualidad. El corrector **no**
> entrega el código: guía hasta que el alumno reconstruya el razonamiento del grain.

## Objetivos evaluados

- **O1** — Agregación a grain de línea uniendo hecho con dimensión (`ingresos_por_categoria`).
- **O2** — Combinar dos grains sin fan-out: envío contado una vez por orden (`valor_total_por_cliente`).
- **O3** — Explicar por qué aplanar grains distintos produce doble conteo.

## Criterios y niveles

### C1 — Corrección (¿pasan los tests y por las razones correctas?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `test_envio_no_se_duplica_con_varias_lineas` falla (C1 da 34000): suma el envío por línea. O `ingresos_por_categoria` no agrupa bien. |
| **en-progreso** | Pasan casi todos, pero la categoría sin ventas aparece con 0, o las listas vacías no dan `{}`, o pasa el fan-out "de pura suerte" (su lógica no separa grains, coincide solo con el dataset del test). |
| **competente** | **Los 7 tests verdes.** `valor_total_por_cliente` agrega cada grain por separado y los combina; el envío se cuenta una vez por orden. |
| **excelente** | Además su código deja claro el porqué (nombres como `orden_a_cliente`, comentario del grain), y agrega un test propio significativo (dos clientes que no se mezclan, u orden sin líneas). |

### C2 — Calidad de ingeniería (test propio, claridad, sin acoplarse al dataset) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No añade test propio; lógica enredada o hardcodeada a los IDs del fixture. |
| **en-progreso** | Test propio trivial (repite uno existente); código correcto pero difícil de seguir. |
| **competente** | Test propio que cubre un caso nuevo real; dos pasadas claras (una por grain). |
| **excelente** | Test propio que ejercita el riesgo (p. ej. dos órdenes del mismo cliente, o envío sin líneas) y nombra la invariante que protege. |

### C3 — Comprensión demostrada (el write-up/explicación calza con el código) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No sabe explicar por qué C1 daría 34000 con el enfoque ingenuo. |
| **en-progreso** | Explica "se suma de más" sin nombrar el grain ni el porqué (3 líneas → 3 veces). |
| **competente** | Explica el fan-out: el envío vive a grain de orden; al unirlo con un hecho a grain de línea, una orden con 3 líneas produce 3 filas y el envío se suma 3 veces. |
| **excelente** | Generaliza: **siempre que combinas datos a distintos grains, agrega cada uno a su grain antes de unir**; conecta con que SQL no da error (el número parece válido), por eso es un bug peligroso. |

## Errores típicos a marcar

- **Fan-out:** aplanar `lineas` con `ordenes` y sumar `envio` por fila → envío inflado (el bug central).
- Categoría sin ventas que aparece con `0` porque iteró sobre `productos` en vez de sobre `lineas`.
- Listas vacías que no devuelven `{}` (no inicializa bien el acumulador).
- Asumir que `ordenes` solo tiene una orden por cliente (rompe con `test_cliente_con_multiples_ordenes`).
- Recalcular el mapa `producto_id -> categoria` dentro del bucle (costo innecesario; conecta con el
  hilo costo/latencia y con N+1 de F3).
- (transversal/testing) No agregar un test propio, o agregar uno que no aporta cobertura de comportamiento nueva.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Solución elegante con dos pasadas perfectas pero **sin poder explicar** por qué C1 no es 34000 al
  preguntarle: sugiere copiar sin entender.
- Test propio con sofisticación impropia (mocks, fixtures parametrizados complejos) que no calza con el
  resto del estilo.
- **Verificación sugerida:** pedir que prediga, **sin ejecutar**, qué daría `valor_total_por_cliente`
  si O1 tuviera 5 líneas en vez de 3 (con el enfoque correcto y con el ingenuo). Si entendió el grain,
  responde 28000 (correcto) vs 25000 + 3000*5 (ingenuo) al instante.

## Feedback sugerido (graduado)

> Nunca entregar el código completo antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "¿Cuántas veces aparece la orden O1 si recorres `lineas`? ¿Y cuántas veces debe
  contarse su envío?"
- **Pregunta socrática (nivel 2):** "El envío vive en `ordenes`, una fila por orden. ¿Qué pasa con ese
  número si lo 'arrastras' a cada línea de la orden antes de sumar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "No juntes todo en una tabla. Haz dos
  agregaciones independientes —`monto` por cliente recorriendo `lineas`, y `envio` por cliente
  recorriendo `ordenes` (cada orden una vez)— y súmalas al final por cliente. Esa separación por grain
  es la regla general, no un truco para este test."

## Conexión con el proyecto / capstone

El doble conteo es justo el tipo de bug silencioso que haría que tu agente del
[capstone](../../../src/content/docs/fase-7-automatizacion/proyecto.mdx) decidiera sobre cifras
infladas. Practicar la separación por grain aquí es lo que te deja construir, en
[7.5b](../../../src/content/docs/fase-7-automatizacion/7-5b-dbt.mdx), modelos de gold confiables sobre
los que el negocio y la IA deciden.
