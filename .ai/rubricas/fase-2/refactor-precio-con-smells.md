---
ejercicio_id: fase-2/refactor-precio-con-smells
fase: fase-2
sub_unidad: "2.3"
version: 1
---

# Rúbrica — Refactoriza una función con smells (red ya puesta)

> Rúbrica **analítica** atada a los `objetivos`. El producto no es "código bonito":
> es la **disciplina** (pasos pequeños, suite verde tras cada paso, comportamiento
> preservado) y la **capacidad de nombrar** smell → refactoring. Evaluar el `smells.md`
> tanto como el `solucion.py`. La suite provista es la verdad: si está roja, el refactor falló.

## Objetivos evaluados
- **O1** — Identificar ≥6 code smells y nombrar el refactoring de Fowler que cada uno gatilla.
- **O2** — Refactorizar en pasos pequeños y reversibles sin alterar el comportamiento observable.
- **O3** — Eliminar la duplicación (vip/frecuente) vía Extract Function preservando los montos.

## Criterios y niveles

### C1 — Comportamiento preservado (corrección) · mapea: O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | La suite provista queda en **rojo**, o el alumno la modificó (aserciones/casos) para que pase. |
| **en-progreso** | Verde, pero "logrado" reescribiendo de más (p. ej. cambió `t - t*0.20` por `t*0.80` y rompió un `approx` ajustado, o tocó una aserción). |
| **competente** | Los 9 tests pasan **sin tocar las aserciones**; mismas entradas → mismas salidas. Si renombró `calc`, ajustó solo la línea de `import`. |
| **excelente** | Verde + evidencia de pasos pequeños (commits `refactor:` separados, o un log de "paso → corrí tests → verde"); nada de comportamiento alterado. |

### C2 — Smells nombrados y refactorings con nombre · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `smells.md`, o lista cambios genéricos ("lo ordené") sin nombrar smell ni refactoring. |
| **en-progreso** | Nombra algunos smells pero <6, o no asocia el refactoring del catálogo (dice "saqué los números" sin "Replace Magic Literal with Symbolic Constant"). |
| **competente** | ≥6 filas smell → refactoring de Fowler → por qué; incluye la **duplicación** vip/frecuente resuelta con **Extract Function**. |
| **excelente** | Además distingue refactorings de bajo riesgo (Rename) de los estructurales (Extract Function), y justifica el **orden** (barato y reversible primero). |

### C3 — Calidad del resultado (clean code aplicado) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Siguen los nombres de una letra, los números mágicos y los condicionales anidados. |
| **en-progreso** | Mejoró nombres pero quedaron magic numbers, o aplanó un condicional y dejó otro, o quedan comentarios-desodorante. |
| **competente** | Nombres con intención, constantes nombradas, condicionales aplanados a guardas, sin comentarios-desodorante, función descompuesta en piezas con un solo propósito. |
| **excelente** | Funciones puras y testeables por separado (subtotal/descuento/envío/IVA); paró **antes** de sobre-extraer (no hay Speculative Generality). |

## Errores típicos a marcar
- **Tocar las aserciones de los tests** para "que pase": invalida la red; el comportamiento ya no está garantizado.
- **Cambiar la fórmula del descuento** (`t - t*0.20` → `t*0.80`): aritméticamente equivalente, pero si el alumno endurece el `approx` o asume igualdad exacta puede engañarse; lo importante es no alterar el resultado observable.
- **`smells.md` que describe acciones, no nombres**: "lo limpié" en vez de "Extract Function / Replace Magic Literal…". El objetivo O1 pide el vocabulario.
- **No eliminar la duplicación** vip/frecuente (el corazón del ejercicio): dejar dos bloques anidados gemelos.
- **Refactorizar todo de una y correr tests al final**: contradice O2; se pierde el "qué paso lo rompió".
- **Sobre-ingeniería**: clases/Strategy/registries para 4 ramas — Speculative Generality; aquí no se pide (eso es 2.4/2.5).
- (transversal spec-driven) un solo commit gigante en vez de `refactor:` separados: el historial deja de ser revisable.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Solución "perfecta de una", con abstracciones impropias del nivel (Strategy pattern, dataclasses, enums) que el enunciado no pide y que delatan código pegado más que derivado de smells.
- `smells.md` con nombres correctísimos del catálogo pero un `solucion.py` que no los refleja (o viceversa): la explicación no calza con el código.
- No puede decir **por qué** corre los tests después de cada paso, ni en qué orden hizo los refactorings.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué test se pondría rojo si en `descuento_por_cliente` invierte por error las tasas de vip alto y base, y que señale en qué paso del refactor lo habría cazado.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Corriste `pytest` ANTES de tocar nada y confirmaste el verde? Ese es el permiso para empezar. Y empieza por lo más barato: renombrar."
- **Pregunta socrática (nivel 2):** "Mira el bloque vip y el bloque frecuente. ¿Qué tienen en común su *forma*? Si extrajeras esa forma a una función, ¿qué parámetros necesitaría para cubrir ambos casos sin un `if` por tipo dentro?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Extrae `descuento_por_cliente(tipo, monto)` que devuelva el monto a restar; dentro, elige la tasa con las constantes según tipo y umbral. Extrae también `subtotal`, `costo_envio` e `iva`. Compón el total al final. Corre la suite después de CADA extracción. Repasa secciones 4.3–4.5 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es el ensayo en pequeño del **Capstone F2 (Refactor + suite de tests)**: ahí harás esto sobre tu propia API, con la red de tests como prerrequisito y `refactor:` separados en el historial. Los smells que cazas aquí son los que justifican el SOLID de 2.4 y los patrones de 2.5.
