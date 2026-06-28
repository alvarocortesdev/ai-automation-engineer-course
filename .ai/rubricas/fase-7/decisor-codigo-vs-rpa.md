---
ejercicio_id: fase-7/decisor-codigo-vs-rpa
fase: fase-7
sub_unidad: "7.4"
version: 1
---

# Rúbrica — Decisor: ¿código, navegador o RPA?

> Rúbrica **analítica** para un ejercicio **de código** que codifica un criterio. Los tests dan el
> piso (verde/rojo); la rúbrica evalúa lo que los tests no ven: que la escalera esté bien razonada, que
> el caso "rediseñar" se entienda (no se acierte por casualidad) y que el `motivo` explique. El
> corrector **no** entrega la implementación: guía hasta que el alumno la reconstruya.

## Objetivos evaluados

- **O1** — Codificar la escalera de integración como función pura que elige por la restricción dominante.
- **O2** — Reconocer cuándo la UI-automation no es base aceptable (sin API + crítico/alto volumen) y subir el problema.
- **O3** — Justificar cada recomendación con un motivo que explique el porqué, no solo el qué.

## Criterios y niveles

### C1 — Corrección de la escalera · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Tests en rojo, o la lógica acierta algunos casos por suerte (orden de `if` inconsistente con la escalera). |
| **en-progreso** | La mayoría de tests pasan, pero falla un destino (típicamente confunde `rpa-ui` con `navegador`, o no prioriza `api` sobre el resto). |
| **competente** | Los 12 tests pasan; la escalera está escrita de arriba hacia abajo y `api` gana siempre, sin importar otras flags. |
| **excelente** | Además la función es claramente pura (sin I/O ni estado), los `if` siguen el orden de la escalera de forma legible, y agregó un test propio significativo (no un duplicado trivial). |

### C2 — El caso "rediseñar-proceso" · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No contempla "rediseñar": ante crítico/alto volumen sin API igual recomienda `rpa-ui` o `navegador`. |
| **en-progreso** | Acierta el test, pero el `motivo` no explica *por qué* la UI-automation no es base aceptable ahí. |
| **competente** | Recomienda `rediseñar-proceso` cuando no hay API y el proceso es crítico o de alto volumen, con motivo que menciona fragilidad/lentitud como base. |
| **excelente** | Articula que la decisión correcta es **subir el problema** (pedir API/export/ETL) y que la UI-automation, de usarse, sería solo un puente temporal. |

### C3 — Calidad del `motivo` (comunicación) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El `motivo` repite la estrategia ("usa api porque api") o está vacío. |
| **en-progreso** | El motivo describe la estrategia pero no la **restricción** que la decidió. |
| **competente** | Cada motivo nombra la restricción dominante (¿hay API?, ¿es web?, ¿crítico/volumen?) que llevó a esa estrategia. |
| **excelente** | Los motivos conectan con la mantención/costo (p. ej. selectores semánticos vs coordenadas, costo total de una API menor a largo plazo). |

## Errores típicos a marcar

- Invertir el orden de la escalera: chequear `es_web` antes que `tiene_api` (la API debe ganar siempre).
- Olvidar el caso crítico/alto volumen y recomendar `rpa-ui` para algo que no debería automatizarse por UI.
- Meter I/O en la función (leer un archivo, imprimir, consultar algo) — debe ser **pura**.
- Un `motivo` que es solo la palabra de la estrategia (no explica nada).
- Perseguir que "pasen los tests" tocándolos en vez de implementar la lógica (mira si modificó las aserciones dadas).
- (transversal) agregar un "test propio" que es copia de uno existente, sin pensar un borde nuevo.

## Señales de dependencia-IA

> Describir sin acusar; proponer verificación.

- Implementación con abstracciones impropias del nivel (un dict de reglas, una máquina de estados, un
  patrón Strategy) para un problema que pide 4 `if`, pero que el alumno no puede explicar línea a línea.
- Motivos redactados con vocabulario muy pulido pero que no calzan con casos del propio dominio.
- **Verificación sugerida:** pedir que, sin mirar, dibuje la escalera y diga qué `if` corresponde a
  cada escalón y por qué `api` va primero. Si codificó con criterio, lo hace al instante.

## Feedback sugerido (graduado)

> Nunca entregar la implementación completa antes de que el alumno cierre su intento.

- **Pista (nivel 1):** "Tu escalera, ¿está escrita en el mismo orden que la subida (API arriba)? Lee
  tus `if` de arriba hacia abajo y compáralos con la escalera de la lección."
- **Pregunta socrática (nivel 2):** "Sin API y proceso crítico: ¿de verdad la respuesta correcta es
  clickear una UI frágil para algo crítico? ¿Qué harías tú en ese trabajo antes de aceptar eso?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Devuelve apenas encuentres el escalón: el
  primer `if` es `tiene_api`. Después, antes de elegir navegador vs rpa-ui, intercepta el caso
  crítico/alto volumen → `rediseñar-proceso`. El orden de los `if` ES la escalera."

## Conexión con el proyecto / capstone

Este decisor es el criterio que aplicarás al elegir cómo el agente del **capstone de la Fase 7**
integra con sistemas externos: API primero; navegador semántico si no hay; RPA solo como último
recurso. Decidirlo con una regla explícita (y un ADR) es lo que el Definition of Done de la fase
espera.
