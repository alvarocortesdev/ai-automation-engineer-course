---
ejercicio_id: fase-2/piramide-decidir-nivel
fase: fase-2
sub_unidad: "2.6"
version: 1
---

# Rúbrica — Ubica los tests en la pirámide y caza el sobre-mockeo

> Rúbrica **analítica** para un ejercicio de **razonamiento** (no hay código que
> correr). Lo que se evalúa es el **juicio** y la capacidad de **defenderlo**: una
> clasificación con justificación coherente vale más que la etiqueta correcta sin
> razón. El corrector evalúa el `respuestas.md`.

## Objetivos evaluados
- **O1** — Clasificar tests como unit/integration/e2e justificando por las fronteras reales que tocan.
- **O2** — Detectar el sobre-mockeo (mockear lógica pura) y proponer no mockearla.
- **O3** — Detectar tests de detalle interno y reorientarlos a comportamiento; nombrar el cono de helado.

## Criterios y niveles

### C1 — Clasificación en la pirámide con justificación · mapea: O1
> Clave de referencia: 1=unit · 2=e2e · 3=integration · 4=unit · 5=integration · 6=unit.

| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Clasifica de memoria sin justificar, o confunde integration con e2e/unit en ≥3 casos. |
| **en-progreso** | Acierta la mayoría pero la justificación es débil (etiqueta sin mencionar la frontera) o falla 1–2 casos (típico: confundir "app en memoria" del caso 5 con unit, o el caso 3 con e2e). |
| **competente** | Clasifica los 6 correctamente y justifica cada uno por la **frontera real** que toca (o que no toca) y el número de piezas reales. |
| **excelente** | Además explicita el trade-off (p. ej. "el caso 2 e2e da confianza de flujo pero es lento/frágil; lo querría como uno de pocos") y reconoce que el caso 5 es integration por usar la app real aunque sea en memoria. |

### C2 — Detección de los antipatrones · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No detecta el sobre-mockeo del Fragmento A ni el detalle interno del B, o "arregla" cambiando cosas irrelevantes. |
| **en-progreso** | Detecta uno de los dos, o detecta ambos pero la corrección propuesta es vaga ("hazlo mejor") sin nombrar el principio. |
| **competente** | A: identifica que `_sumar_items` es pura → mockearla acopla a la implementación y deja sin probar el cálculo; propone no mockear y verificar el total real. B: identifica que afirmar sobre `_saldo`/`_ultima_operacion` ata el test a internos; propone testear comportamiento observable (un `saldo()` público o el efecto de una operación posterior). |
| **excelente** | Conecta ambos con la regla general (mock solo en la frontera; testea comportamiento, no implementación) y nota que ambos tests se romperían en un refactor que no cambia el comportamiento. |

### C3 — Diagnóstico de la pirámide invertida · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra el antipatrón o no propone acción. |
| **en-progreso** | Dice "faltan unit" sin nombrar el cono de helado ni explicar el costo (lentitud/flakiness). |
| **competente** | Nombra el **cono de helado** (ice-cream cone), explica los problemas concretos (suite lenta, frágil, que falla por razones ajenas al bug, difícil de localizar) y propone empujar la base (más unit, menos e2e). |
| **excelente** | Propone un plan concreto: identificar la lógica cubierta por e2e que podría ser unit, mantener solo unos pocos e2e de *happy paths* críticos, y añadir integration para el pegamento. |

## Errores típicos a marcar
- **Confundir e2e con integration**: el caso 5 (app real en memoria, cliente HTTP de prueba) es integration, no e2e (no hay navegador ni el sistema completo desplegado).
- **Llamar unit al caso 3** porque "es un solo repositorio": toca Postgres real → integration.
- **No justificar**: poner solo la etiqueta. El objetivo O1 pide el *porqué* (la frontera).
- **"Arreglar" el Fragmento A** endureciendo el mock en vez de eliminarlo: el problema es que el mock sobra.
- **Confundir "privado" con "no testeable"**: el punto del Fragmento B no es que `_saldo` sea privado, sino que el test verifica *cómo* se guarda en vez de *qué* comportamiento se observa.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Respuestas con vocabulario impecable ("acoplamiento estructural", "test fragility") pero sin aplicarlo al caso concreto (no señala *cuál* línea sobra en el Fragmento A).
- Clasificación perfecta sin una sola justificación propia, o justificaciones que repiten la definición sin mapearla al escenario.
- **Verificación sugerida:** pedir que invente un séptimo escenario y lo clasifique, o que explique por qué el caso 5 no es e2e con sus palabras.

## Feedback sugerido (graduado)
> Nunca dar la clasificación completa antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada test, hazte una sola pregunta: ¿toca una frontera real (DB, red, navegador)? Eso casi siempre decide el nivel."
- **Pregunta socrática (nivel 2):** "En el Fragmento A, ¿qué quedaría sin probar si `_sumar_items` siempre devuelve 100 mockeado? ¿El test seguiría rojo si `_sumar_items` tuviera un bug?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Revisa los casos 3 y 5: ambos usan una pieza real (DB / app en memoria) → integration, no unit ni e2e. Para el Fragmento B, reescribe la aserción para que mire un método público o el efecto de una operación, no `_saldo`. Repasa la sección 4.6 y los non-examples de la sección 5."

## Conexión con el proyecto / capstone
- El juicio que ejercitas aquí decide **cómo repartes** los tests del Capstone F2: la mayoría unit sobre la lógica de negocio, algunos de integración para el acceso a datos, y los e2e reservados para [`2.10`](/fase-2-ingenieria/2-10-playwright-e2e/). Sin este criterio, la suite del capstone termina siendo un cono de helado.
