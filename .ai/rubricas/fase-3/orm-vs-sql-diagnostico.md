---
ejercicio_id: fase-3/orm-vs-sql-diagnostico
fase: fase-3
sub_unidad: "3.5"
version: 1
---

# Rúbrica — Diagnostica el N+1 y decide ORM vs SQL crudo

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio **a-mano**: no hay test. Se evalúa el
> razonamiento en `diagnostico.md` y `decisiones.md`. El valor está en el **proceso** (cómo cuenta
> y por qué decide), no en una respuesta única — hay decisiones de diseño con más de una respuesta
> defendible, pero el N+1 del log tiene una lectura correcta.

## Objetivos evaluados
- **O1** — Diagnosticar el N+1 del log: contar queries, nombrar el patrón, identificar la causa.
- **O2** — Proponer la cura correcta (`joinedload` vs `selectinload`) coherente con la relación.
- **O3** — Decidir ORM vs SQL crudo por escenario, con trade-off defendible.

## Criterios y niveles

### C1 — Diagnóstico del N+1 (Parte A) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No cuenta las queries o no reconoce el N+1; dice "está lento" sin diagnóstico. |
| **en-progreso** | Cuenta 5 queries pero no nombra el patrón o no identifica el acceso a relación que lo causa. |
| **competente** | Cuenta 5 = 1 + 4, nombra el N+1 (N = 4), e identifica que `pedido.cliente` (lazy) dentro del bucle lo dispara. |
| **excelente** | Además explica el `id = 1` repetido: el lazy loading no cachea entre objetos distintos, así que cada `pedido.cliente` se re-consulta (conecta con observabilidad: el log es la evidencia). |

### C2 — La cura (Parte A) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No propone cura, o propone "un índice" como solución al N+1 (no reduce el número de queries). |
| **en-progreso** | Propone eager loading pero elige la estrategia sin ligarla al tipo de relación. |
| **competente** | `joinedload` por ser `pedido.cliente` **to-one**; el endpoint queda en 1 query. |
| **excelente** | Justifica que to-one → `joinedload` (sin `.unique()` por no ser colección) y contrasta con `selectinload` (round-trip extra innecesario aquí). |

### C3 — Decisiones ORM vs SQL crudo (Parte B) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin justificación, o "siempre ORM" / "siempre SQL" sin matiz. |
| **en-progreso** | Decide bien 1–2 escenarios; el resto sin argumento defendible. |
| **competente** | CRUD → ORM; reporte con window functions → SQL crudo; carga masiva → SQL/bulk. Cada uno con una razón. |
| **excelente** | Razones precisas (el ORM brilla en CRUD/navegación; el SQL es más claro en analítica; el ORM objeto-por-objeto es lento para millones de filas) **y** menciona el SQL parametrizado como requisito de seguridad. |

## Errores típicos a marcar
- **Confundir N+1 con "falta un índice":** un índice acelera **cada** query, pero el problema es que son **demasiadas** queries. La cura es eager loading, no un índice.
- **Proponer `selectinload` para un to-one** sin notar que `joinedload` lo resuelve en 1 query (no en 2).
- **No explicar el `id = 1` repetido:** señal de que no entendió que el lazy loading re-consulta en cada acceso.
- **"Siempre ORM" o "siempre SQL crudo":** ambos extremos delatan falta de criterio; el punto del ejercicio es el trade-off.
- (transversal seguridad) olvidar que el SQL crudo debe ir **parametrizado**; concatenar strings = SQL injection.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diagnóstico correcto pero sin poder explicar el `id = 1` repetido ni por qué `joinedload` es to-one y `selectinload` to-many.
- Decisiones de la Parte B muy pulidas pero genéricas, sin atarse a los detalles de cada escenario (window function, 2 millones de filas).
- Vocabulario sofisticado (CQRS, read replicas) impropio del nivel, sin poder defenderlo.
- **Verificación sugerida:** pídele que cuente, sin ayuda, cuántas queries quedarían con `joinedload` (1) y con `selectinload` (2) en el caso del log, y que explique por qué para `pedido.cliente` no hace falta `.unique()`.

## Feedback sugerido (graduado)
> Nunca dar la respuesta antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Cuenta las líneas `SELECT` del log. ¿Cuántas traen pedidos y cuántas traen un cliente cada una? ¿Te recuerda al patrón 1 + N?"
- **Pregunta socrática (nivel 2):** "El cliente `id = 1` se consulta dos veces. Si el ORM hubiera cacheado la primera carga, no habría una segunda. ¿Qué te dice eso sobre cuándo decide lazy loading ir a la base? Y como `pedido.cliente` es **un** objeto por pedido, ¿qué tipo de eager loading lo trae en la misma query?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "La cura es `joinedload(Pedido.cliente)`: un `LEFT JOIN` que trae el cliente en el mismo `SELECT`, dejando el endpoint en 1 query (sin `.unique()`, porque no es colección). Para la Parte B, revisa 4.9: window functions y cargas masivas son los casos donde el SQL crudo gana."

## Conexión con el proyecto / capstone
- El diagnóstico por conteo de queries es la herramienta que usarás para auditar cada endpoint del capstone; la decisión ORM-vs-SQL-crudo de alguna query, justificada, va en un **ADR** del proyecto.
