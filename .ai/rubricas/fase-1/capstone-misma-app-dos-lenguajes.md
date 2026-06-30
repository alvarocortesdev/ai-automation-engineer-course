---
ejercicio_id: fase-1/capstone-misma-app-dos-lenguajes
fase: fase-1
sub_unidad: "1.P"
version: 1
---

# Rúbrica — Capstone F1: La misma app, dos lenguajes (despensa HomeBase)

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corazón del
> capstone NO es "hacer una API" (no hay framework, es stdlib): es **resolver el
> mismo problema dos veces** con validación declarativa, tests reales y separación
> dominio/HTTP, y **defender por escrito** qué cambió entre lenguajes. Es también un
> capstone: el corrector verifica los puntos del **Definition of Done** que aplican
> en F1 (`definition_of_done: [1, 2, 8, 9]`).

## Objetivos evaluados
- **O1** — Construir la misma mini-API en Python y TS cumpliendo un contrato HTTP idéntico.
- **O2** — Validar la entrada de forma declarativa (pydantic / zod) antes de persistir.
- **O3** — Separar la lógica de dominio (`PantryStore`) de la capa HTTP (testeable sin servidor).
- **O4** — Proteger la lógica con tests de aserciones reales (pytest / vitest), red-green.
- **O5** — Explicar y defender por escrito los trade-offs entre la versión Python y la TS.

## Criterios y niveles

### C1 — Corrección del contrato en ambas versiones · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Solo existe una de las dos versiones, o alguna no levanta; rutas que no respetan el contrato (status equivocados, no persiste). |
| **en-progreso** | Las dos versiones existen y cubren el caso feliz, pero faltan casos borde (p. ej. 400 para `id` no numérico, 400 para JSON roto, distinción 422 vs 400). |
| **competente** | Ambas versiones cumplen las 5 rutas y los 6 casos borde de `CONTRATO-HTTP.md`; `curl` da el mismo status en las dos. |
| **excelente** | Además, las dos responden cuerpos equivalentes y el alumno detectó y documentó las diferencias inevitables (p. ej. Python serializa `quantity` como `2.0`, TS como `2`). |

### C2 — Validación declarativa · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida, o "valida" con `if`s a mano campo por campo; deja entrar `quantity` ≤ 0 o `name` vacío. |
| **en-progreso** | Usa pydantic/zod pero incompleto (valida tipos pero no `> 0` ni "no vacío"), o valida pero igual persiste el dato malo. |
| **competente** | Modelo pydantic + esquema zod con `name` no vacío, `quantity > 0`, `unit` no vacío; el dato inválido lanza y **no** se persiste; mapea a `422`. |
| **excelente** | Reusa el tipo derivado (`z.infer`, herencia `Item(NewItem)`) en vez de repetir la forma; entiende que el tipo *es* la validación. |

### C3 — Separación dominio/HTTP y testeo · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Lógica y HTTP mezcladas en un archivo; tests ausentes o que levantan el servidor / tocan la red. |
| **en-progreso** | Hay un `PantryStore` separado pero los tests dependen de un archivo fijo (no temporal) o no agregó ningún test propio. |
| **competente** | `PantryStore` recibe el path por parámetro (seam); tests con archivo temporal (`tmp_path` / `mkdtempSync`), verdes, **+1 test propio** por suite. |
| **excelente** | Tests con aserciones de comportamiento (incluye "el dato inválido no se persiste"), nombres claros, y el alumno explica por qué el test no necesita HTTP. |

### C4 — Spec, decisiones y comunicación (DoD §1, §8) · mapea: O5
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `SPEC.md` o sin `DECISIONES.md`; README ausente o solo en español sin write-up. |
| **en-progreso** | Spec y/o ADRs presentes pero vacíos de contenido (plantilla sin rellenar); README en inglés pero sin write-up de trade-offs. |
| **competente** | `SPEC.md` con casos borde reales + `DECISIONES.md` con ≥2 ADRs defendibles + README **en inglés** con write-up de 5–8 frases Python vs TS. |
| **excelente** | El write-up nombra diferencias **concretas y vividas** (no genéricas): `None` vs `undefined`, `ValidationError` vs `ZodError`, coerción de tipos en runtime, ergonomía de `z.infer`. Conventional Commits limpios en el historial (DoD §9). |

<!-- C5 (seguridad), C6 (observabilidad/eval) NO aplican en F1: llegan en F3/F5/F6. -->

## Errores típicos a marcar
- **Empezar por el servidor HTTP** y terminar con todo enredado en un archivo (lógica + HTTP + validación). El `PantryStore` debe poder testearse sin levantar el server.
- **Validar con `if`s a mano** en vez de declarar el modelo: reimplementa peor lo que pydantic/zod ya hacen.
- **Confundir `400` con `422`**: JSON roto (no se pudo parsear) → `400`; JSON válido que no cumple las reglas → `422`. Colapsarlos pierde el sentido.
- **`GET /items/abc` → `404`** en vez de `400`: un id no numérico es un *request* mal formado, no un recurso ausente.
- **El dato inválido SÍ se persiste**: validar después de escribir, o escribir y luego validar. Debe lanzar **antes** de tocar el archivo.
- **Tests que tocan un archivo fijo** (no temporal): se contaminan entre corridas; usar `tmp_path` / `mkdtemp`.
- **No agregar ningún test propio**: el starter pide explícitamente +1 por suite.
- **README solo en español** o sin write-up de trade-offs: incumple DoD §8 (inglés + write-up).
- **Tratar las dos versiones como idénticas** (negar las diferencias) o como **sin relación** (no comparar). El valor está en nombrar *qué* cambia y *por qué*.
- (transversal costo) Si hizo la ruta opcional de IA: **confiar en la salida del LLM sin validar** con pydantic/zod, o no registrar tokens/costo.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- **Sofisticación impropia del nivel:** mete un framework (FastAPI/Express), una base de datos, async/await sin necesidad, o un router elaborado cuando el ejercicio es stdlib. Señal de haber pedido "haz una API REST" a una IA sin leer el alcance.
- **Las dos versiones son sospechosamente idénticas** hasta en los comentarios, sin rastro de las diferencias reales entre lenguajes: posible traducción automática 1:1 sin comprensión.
- **El write-up de trade-offs es genérico** ("Python es más simple, TS es más seguro") sin un solo ejemplo concreto del *propio* código.
- **No puede explicar** por qué `GET /items/abc` da `400` y no `404`, o por qué el test no necesita internet.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué devuelve cada versión para `POST /items` con `quantity: "2"` (string), y que explique la diferencia de coerción entre pydantic y zod. Pedir que muestre el commit donde el test estaba en rojo antes de implementar.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Revisa tu manejo de status: tienes tres situaciones de error distintas en `POST` (JSON ilegible, dato que no valida, todo bien) y en `/items/{id}` (id no numérico, id inexistente, existe). ¿Cada una devuelve un status distinto? Compáralo contra `CONTRATO-HTTP.md`."
- **Pregunta socrática (nivel 2):** "¿En qué punto exacto de tu `add` se rechaza un `quantity: 0`? ¿Ese rechazo ocurre **antes** o **después** de escribir el archivo? Y al comparar tus dos versiones: ¿qué hizo distinto cada lenguaje con un número `2` — lo dejó entero o lo volvió decimal? ¿Por qué?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura el dominio así: leer JSON → operar en memoria → escribir JSON; el id nuevo es `max(ids, default 0) + 1`; valida con el modelo **antes** del cálculo del id. En la capa HTTP, una sola responsabilidad por rama: parsear → llamar al store → elegir status. Para el write-up, abre tus dos archivos lado a lado y anota cada lugar donde tuviste que escribir algo distinto: ahí están tus trade-offs. Revisa las sub-unidades 1.4, 1.5 y 1.6 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- **Este ES el capstone de la fase.** Verificar los puntos del DoD que aplican (`[1, 2, 8, 9]`): mini-spec + ADRs, tests verdes con aserciones, demo que corre + README inglés + write-up, Conventional Commits.
- Alimenta el **Capstone F2** (refactor + SOLID + mutation testing): la frontera dominio/HTTP que el alumno trace aquí es exactamente lo que F2 endurecerá. Una mezcla sucia ahora = más dolor allá.
