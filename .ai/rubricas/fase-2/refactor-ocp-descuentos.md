---
ejercicio_id: fase-2/refactor-ocp-descuentos
fase: fase-2
sub_unidad: "2.4"
version: 1
---

# Rúbrica — Refactor a Open/Closed con red de tests

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa no es "¿compiló?": es si el
> refactor **preservó el comportamiento** (tests originales intactos y verdes) y si el diseño de verdad queda
> **cerrado a modificación**. Un alumno puede tener todo verde con un `if/elif` apenas disfrazado; otro puede
> tener un diseño limpio pero haber cambiado un test para "que pase". La rúbrica distingue ambos.

## Objetivos evaluados
- **O1** — Refactorizar el `if/elif` a Open/Closed preservando el comportamiento (tests verdes sin modificar).
- **O2** — Diseñar una abstracción (`abc`/`Protocol`) + una clase por caso, con un punto de entrada cerrado.
- **O3** — Demostrar "cerrado a modificación" agregando `mayorista` sin tocar lo existente.

> Resultado esperado: tras el refactor, `pytest` pasa los 8 tests originales **sin cambios** + el test nuevo de
> `mayorista`. El corrector lo sabe; **no se lo dice al alumno** como atajo que evite el razonamiento.

## Criterios y niveles

### C1 — Corrección: comportamiento preservado · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Los tests no pasan, o el alumno **modificó los tests originales** para que pasaran (cambió el comportamiento sin notarlo). |
| **en-progreso** | Los tests pasan, pero hubo que ajustar algún valor esperado, o el refactor cambió la firma pública `calcular_descuento`. |
| **competente** | Los 8 tests originales pasan **sin modificarlos**; la firma pública se conserva; los valores (incluido el truncado a entero de 999→99) cuadran. |
| **excelente** | Además corrió la suite **antes** del refactor para confirmar el verde de partida (red de seguridad consciente) y lo menciona; `mypy` limpio. |

### C2 — Diseño Open/Closed real · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sigue habiendo un `if/elif`/`isinstance` sobre `cliente_tipo` para decidir el cálculo (no se refactorizó, se maquilló). |
| **en-progreso** | Hay clases, pero la lógica de despacho aún ramifica por tipo (p. ej. un `if tipo == "vip": return DescuentoVip()...`), o falta la abstracción común. |
| **competente** | Abstracción `Descuento` (con `abc` o `Protocol`) + una clase por tipo con `calcular(monto) -> int`; el despacho es un **registro** (`dict`) o equivalente, sin condicional ramificado en la lógica de precio. |
| **excelente** | El punto de entrada no conoce los tipos concretos; la elección de `Protocol` vs `ABC` está justificada; nombres limpios; sin estado innecesario en las clases-estrategia. |

### C3 — Extensión sin modificación · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó `mayorista`, o para agregarlo tuvo que **editar** clases existentes o un `if/elif`. |
| **en-progreso** | Agregó `mayorista` pero editando más de lo necesario (p. ej. tocó otra clase), o no agregó su test. |
| **competente** | `mayorista` (25%) agregado con **una clase nueva** + una entrada en el registro + su test verde; nada más se tocó. |
| **excelente** | Articula por qué esto prueba OCP ("no reabrí código probado") y agrega un caso borde propio pertinente. |

### C4 — Comprensión demostrada (write-up / explicación) · mapea: O1–O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar qué quedó "cerrado" ni por qué; o la explicación no calza con el código entregado. |
| **en-progreso** | Explica "usé clases" sin conectar con la idea de razón de cambio / punto de extensión. |
| **competente** | Explica con precisión qué función quedó cerrada a modificación y por qué agregar un tipo ya no la reabre. |
| **excelente** | Nombra el trade-off honesto: cuándo este refactor **no** habría valido la pena (Rule of Three) — conecta con el ejercicio de juicio. |

## Errores típicos a marcar
- **Modificar los tests para que pasen:** el síntoma #1 de un refactor que cambió el comportamiento. Un refactor honesto deja los tests intactos.
- **Maquillar el `switch`:** mover el `if/elif` a una "factory" que sigue siendo un `if/elif` por tipo. Si agregar un caso obliga a editar el despacho con una rama nueva, no es OCP (un `dict`-registro sí lo es).
- **Romper el truncado a entero:** usar `float` o `round` distinto y fallar `vip` de 999 (debe dar 99, no 100).
- **Cambiar la firma pública** y romper a quien llama `calcular_descuento`.
- **Sobre-abstraer:** meter una metaclase, auto-registro vía `__init_subclass__` o un framework de DI para 6 casos triviales — anótalo como señal de la lección de crítica (sección 5), no como mérito.
- (transversales) confiar en que "pasa pytest" sin revisar que los **valores** sean correctos; no agregar un caso borde propio.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Diseño con auto-registro/metaclases/decoradores sofisticados **impropio del nivel F2** que el alumno no puede explicar línea a línea.
- El refactor está impecable pero el alumno no sabe decir **qué queda cerrado** ni por qué (código sin modelo mental detrás).
- Aparecen patrones con nombre (Strategy, Registry) usados correctamente pero sin que el alumno pueda justificar la elección.
- **Verificación sugerida:** pedir que agregue **en vivo** un tipo `"socio"` (5%) y explique qué archivos toca y cuáles NO. Si entendió OCP, toca solo lo nuevo; si dependió de la IA, duda o reabre código probado.

## Feedback sugerido (graduado)
> Nunca pegar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira tu lógica de despacho: para agregar un tipo, ¿tienes que **editar** algo que ya pasaba sus tests? Si la respuesta es sí, todavía no está 'cerrado a modificación'."
- **Pregunta socrática (nivel 2):** "¿Qué tienen en común las cinco clases de descuento? Si comparten exactamente un método con la misma firma, ¿quién debería declarar ese contrato, y cómo evita eso el `if isinstance`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El despacho por tipo debe ser un **mapa** de string→instancia (un registro), no una cadena de `if/elif`. Así agregar un caso es una clase nueva + una entrada en el mapa, y la función de precio nunca se reabre. Reescribe el despacho como `dict` y vuelve a correr los tests sin tocarlos."

## Conexión con el proyecto / capstone
- Es el ensayo directo del **Capstone F2 — Refactor + suite de tests**: identificar un smell, refactorizar con SOLID y **demostrar con tests verdes** que el comportamiento se preservó. El registro de descuentos es el mismo patrón que aplicarás a tu propio proyecto de la Fase 1.
