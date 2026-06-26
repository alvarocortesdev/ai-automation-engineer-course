---
ejercicio_id: fase-3/graphql-rest-decidir
fase: fase-3
sub_unidad: "3.11"
version: 1
---

# Rúbrica — Decide: REST o GraphQL para tres escenarios

> Rúbrica **analítica** de un ejercicio de **razonamiento**. No hay respuesta única: se evalúa la **calidad del criterio**, no qué estilo eligió. Una elección "contraria a la esperada" bien defendida con criterios y trade-offs vale más que la "esperada" con un eslogan. Los errores a marcar son decidir por moda ("GraphQL es más moderno") o por simplismo ("REST es más fácil") sin atarlo al contexto.

## Objetivos evaluados
- **O1** — Decidir con criterios concretos (heterogeneidad de clientes, caching HTTP, over/under-fetching real, complejidad del servidor).
- **O2** — Nombrar el trade-off de cada elección y qué evidencia la cambiaría.
- **O3** — Defender que un cliente único favorece REST y muchos clientes heterogéneos favorecen GraphQL, sin caer en moda.

## Criterios y niveles

### C1 — Calidad del criterio de decisión · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Elige por eslogan ("más moderno", "más simple", "lo que se usa") o sin justificar. No aparece el criterio de **heterogeneidad de clientes**. |
| **en-progreso** | Justifica con algún criterio real pero superficial ("GraphQL pide menos datos") sin atarlo al contexto de cada escenario (SPA única / 3 clientes distintos / webhook). |
| **competente** | Cada decisión se apoya en criterios pertinentes: número y heterogeneidad de clientes, caching HTTP, over/under-fetching real. Las tres son defendibles (típicamente A→REST, B→GraphQL, C→REST). |
| **excelente** | Además expone una **tensión** explícita donde no es obvio (p. ej. A si la SPA crece, o B si los partners pudieran vivir con endpoints fijos) en vez de fingir que todo es trivial. |

### C2 — Trade-offs y evidencia que cambia la decisión · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Vende su elección como perfecta; no nombra ningún costo ni qué lo haría cambiar. |
| **en-progreso** | Menciona un costo genérico ("tiene curva") sin atarlo al escenario, o solo en uno de los tres. |
| **competente** | Cada escenario nombra un costo real (GraphQL: caching perdido, autorización por campo, observabilidad, DoS por queries no acotadas; REST: over/under-fetching, round trips, endpoints a medida) y un dato que cambiaría la decisión. |
| **excelente** | Los costos son específicos del caso y la evidencia-que-cambia-la-decisión es accionable (p. ej. "si los partners se redujeran a uno con necesidades fijas, volvería a REST"). |

## Errores típicos a marcar
- **Decidir por moda/popularidad** ("GraphQL es lo que se usa ahora").
- **Simplismo** ("REST es más fácil") sin medir si el over/under-fetching duele de verdad en el escenario.
- **GraphQL para el webhook (C)** "porque es más flexible": overkill; no hay ni un cliente que elija campos.
- **GraphQL para la SPA única (A)** sin reconocer que pierdes caching HTTP gratis y métricas por ruta por un beneficio marginal.
- **Vender una opción como perfecta**: no nombrar ningún costo es la señal #1 de razonamiento inmaduro.
- **No reconocer ninguna ambigüedad** en los tres.
- (transversales) confundir "lo que me gusta" con "lo correcto para el contexto"; olvidar que GraphQL abre una superficie de DoS (queries no acotadas) que REST no tiene por defecto.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto pulido que recita ventajas genéricas de GraphQL (copiables de cualquier comparativa) sin aterrizarlas en SPA / 3-clientes / webhook.
- Tres decisiones "de manual" sin una sola tensión ni costo específico — sospechosamente limpias.
- **Verificación sugerida:** pedir el contrafactual del escenario B: "¿qué tendría que ser verdad para que REST siguiera ganando con 3 clientes distintos?". Quien razonó lo construye (p. ej. que las tres formas de datos fueran casi iguales y el caching importara mucho); quien copió se queda sin material.

## Feedback sugerido (graduado)
> Es razonamiento: el feedback empuja a defender mejor, no a "la respuesta correcta". **Nunca dar la solución.**
- **Pista (nivel 1):** "¿Cuál es el primer criterio que inclina la decisión casi siempre? Pista: cuántos clientes distintos piden formas distintas de los mismos datos."
- **Pregunta socrática (nivel 2):** "Para la SPA única, ¿qué ganas con GraphQL que no tengas ya con REST, y qué pierdes (piensa en el caching del navegador/CDN)? Para los 3 clientes heterogéneos, ¿qué problema concreto te resuelve que GraphQL deje al cliente elegir la forma?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El eje dominante es la heterogeneidad de clientes y necesidades de datos, no una superioridad abstracta. Reescribe cada decisión añadiendo (a) el criterio que más pesó y (b) un costo concreto de tu elección."

## Conexión con el proyecto / capstone
- Esta decisión es justo un **ADR** del Capstone F3 (el estilo de la API). Poder escribir "elegí REST sobre GraphQL porque la API tiene un solo cliente y quiero el caching HTTP y las métricas por ruta gratis, aceptando reevaluar si sumo una app móvil" es el tipo de trade-off defendible que pide el Definition of Done de la fase.
