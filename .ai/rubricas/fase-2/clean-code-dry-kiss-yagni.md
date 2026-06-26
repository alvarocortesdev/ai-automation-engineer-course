---
ejercicio_id: fase-2/clean-code-dry-kiss-yagni
fase: fase-2
sub_unidad: "2.2"
version: 1
---

# Rúbrica — DRY/KISS/YAGNI con criterio

> Rúbrica analítica atada a los `objetivos` del contrato. El núcleo de este ejercicio es el
> **juicio**, no el código: los tests pasan tanto si el alumno hace lo correcto como si comete el
> error clásico (unir los validadores). La señal de aprendizaje está en `decisiones.md`, no en el
> color verde. **Evalúa el write-up con el mismo peso que el código.**

## Objetivos evaluados
- **O1** — Aplicar DRY a duplicación real (mismo conocimiento) extrayéndola a un solo lugar.
- **O2** — Distinguir duplicación incidental de real y **resistir la falsa DRY** (no acoplar lo que cambia por razones distintas).
- **O3** — Aplicar KISS/YAGNI simplificando una función sobre-parametrizada a su uso real, sin cambiar el comportamiento.
- **O4 (comunicación)** — Justificar por escrito cada decisión, incluida la de NO unificar.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): fórmula del IVA en un solo
> `con_iva(neto)` que usa la constante `IVA`; validadores `es_rut_valido`/`es_sku_valido`
> **separados**; `formatear_precio(monto)` con un solo parámetro.

## Criterios y niveles

### C1 — DRY real aplicado · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | La fórmula del IVA sigue duplicada en las dos funciones; la constante `IVA` sigue sin usarse. |
| **en-progreso** | Extrajo la fórmula pero dejó el literal `0.19` en vez de usar la constante `IVA`, o solo lo aplicó en una de las dos funciones. |
| **competente** | La fórmula del IVA vive en un solo lugar (`con_iva`), usa la constante `IVA`, y ambas funciones la reusan; tests verdes. |
| **excelente** | Además explica que la extracción es correcta **porque** boleta y factura cambian por la misma razón si el IVA sube. |

### C2 — Resistir la falsa DRY (duplicación incidental) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Unificó `es_rut_valido` y `es_sku_valido` en un genérico (los acopló); o no menciona el caso. |
| **en-progreso** | Los dejó separados pero **por inercia**, sin poder explicar por qué unirlos sería un error. |
| **competente** | Los mantuvo separados y su `decisiones.md` explica que validan conceptos independientes que cambiarían por razones distintas. |
| **excelente** | Da el escenario concreto del daño ("si el RUT pasa a exigir dígito verificador, un validador genérico rompería el SKU en silencio") y nombra el concepto: duplicación incidental. |

### C3 — KISS/YAGNI · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `formatear_precio` sigue con sus cinco parámetros y ramas muertas. |
| **en-progreso** | Quitó algunos parámetros pero dejó ramas/knobs que nadie usa, o cambió el comportamiento del caso real. |
| **competente** | Simplificó a `formatear_precio(monto)`, conservando exactamente la salida del caso real; tests verdes. |
| **excelente** | Justifica con evidencia (cómo se llama en los tests) y nombra la deuda evitada al no construir para un futuro imaginado. |

### C4 — Comunicación del criterio (write-up) · mapea: O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No entregó `decisiones.md` o repite el enunciado sin razonar. |
| **en-progreso** | Describe **qué** hizo pero no **por qué**; falta la decisión de NO unificar. |
| **competente** | Las tres decisiones con su porqué, en lenguaje claro, incluida la de resistir la falsa DRY. |
| **excelente** | Escribe como un mini-ADR defendible: regla general ("extrae cuando cambian por la misma razón") aplicada a cada caso. |

## Errores típicos a marcar
- **Unir los dos validadores** "porque son iguales": es el error central que el ejercicio busca; la duplicación incidental se deja.
- Extraer el IVA pero dejar el literal `0.19` en vez de la constante `IVA` (DRY a medias).
- "Simplificar" `formatear_precio` cambiando su salida (rompe `test_formatear_precio_*`): la simplificación NO debe alterar comportamiento.
- Sobre-abstraer al revés: crear una jerarquía/clase para el IVA "por si vienen más impuestos" (vuelve a caer en YAGNI).
- `decisiones.md` que solo dice "apliqué DRY/KISS/YAGNI" sin el razonamiento por caso.
- (transversal) no agregar test propio o agregar uno que replica un caso existente.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Refactor impecable pero `decisiones.md` genérico/vago (la IA refactoriza fácil; el porqué específico delata si hubo pensamiento).
- Justifica la NO unificación con la frase correcta pero, al preguntar, no puede inventar otro ejemplo propio de duplicación incidental.
- **Verificación sugerida:** pídele un caso NUEVO (no el del ejercicio) de dos funciones que se parezcan pero NO deban unirse, y otro donde SÍ. Si entiende el criterio, los distingue al instante; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el código completo.
- **Pista (nivel 1):** "Por cada par de funciones parecidas, hazte una sola pregunta: si la regla de una cambia mañana, ¿la otra debería cambiar con ella? Tu respuesta decide si extraes o dejas."
- **Pregunta socrática (nivel 2):** "El RUT y el SKU hoy validan `len >= 3`. ¿Esa regla es la *misma decisión de negocio* o una coincidencia? ¿Qué pasaría con el SKU si mañana el RUT exige otra cosa y compartieran función?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Extrae la fórmula del IVA a `con_iva(neto)` con la constante `IVA` y reúsala en ambas; deja los dos validadores separados y escribe en `decisiones.md` por qué; borra los parámetros de `formatear_precio` que los tests nunca usan. No te doy el código."

## Conexión con el proyecto / capstone
- El `decisiones.md` de este ejercicio es el embrión de los **ADRs** del **Capstone F2**: documentar no solo lo que refactorizaste, sino lo que decidiste **no** tocar y por qué. Ese criterio es lo que [2.13 Colaboración, spec-driven y ADRs](/fase-2-ingenieria/2-13-colaboracion-spec-driven-adrs/) formaliza.
