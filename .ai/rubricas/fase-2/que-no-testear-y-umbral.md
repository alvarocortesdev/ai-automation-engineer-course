---
ejercicio_id: fase-2/que-no-testear-y-umbral
fase: fase-2
sub_unidad: "2.9"
version: 1
---

# Rúbrica — Qué NO testear + tu política de umbral honesta

> Rúbrica **analítica** para un ejercicio de **razonamiento**. No hay código que
> ejecutar: se evalúa la **calidad del juicio** y la **defensa**. Un alumno puede
> clasificar bien por suerte; lo que importa es que la justificación de cada caso y la
> política revelen que entendió *por qué* coverage-como-meta es Goodhart y *qué* medir
> en su lugar. Premia las decisiones defendibles, no las "correctas" memorizadas.

## Objetivos evaluados
- **O1** — Decidir, con justificación de valor/costo, qué testear unitariamente, qué no, y qué en integración.
- **O2** — Explicar Goodhart aplicado a coverage-como-meta y proponer qué medir en su lugar.
- **O3** — Diseñar una política honesta: umbral defendible + cadencia de mutation testing acorde a su costo.

> Clasificación de referencia (el corrector la usa como vara, **no como única respuesta
> válida**; hay matices defendibles): **A** getter → no-testear; **B** wrapper → no-testear
> (o un test de contrato/integración mínimo, nunca unitario mockeando `requests`);
> **C** IVA → testear-unitario (el centro); **D** logging → no-testear; **E** DTO generado
> → no-testear; **F** parser de fechas → testear-unitario (bordes y errores); **G** `__main__`
> → no-testear; **H** orquestador → testear-en-integración.

## Criterios y niveles

### C1 — Clasificación con criterio de valor/costo · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Clasifica "todo se testea" (o casi), o sin justificación; trata getter, DTO y lógica de IVA por igual. |
| **en-progreso** | Acierta los casos obvios pero falla en H (lo testea unitario mockeando todo) o en B (lo testea unitario), o justifica con "buenas prácticas" sin valor/costo. |
| **competente** | Clasifica los 8 de forma defendible: C y F como centro unitario; A, D, E, G fuera; B sin test unitario; H en integración. Cada justificación liga a "puede fallar de forma interesante" y/o "se rompe al refactorizar sin atrapar bugs". |
| **excelente** | Además matiza: p. ej. un test de **contrato** para B (que el schema externo no cambió), o nota que el DTO generado se cubre indirectamente al testear C/F que lo consumen. |

### C2 — Comprensión de Goodhart / qué medir · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | La política propone "coverage ≥ X" como objetivo, sin cuestionarlo. |
| **en-progreso** | Menciona que coverage tiene límites pero no nombra el mecanismo (ejecutar ≠ verificar) ni propone un reemplazo concreto. |
| **competente** | Explica que coverage como meta se vuelve gameable (Goodhart / ejecutar sin afirmar) y propone usarlo como **diagnóstico de mínimos** + mutation score sobre la lógica crítica. |
| **excelente** | Da un ejemplo propio de cómo se infla el número (test sin aserción, testear triviales) y distingue "0% es alarma" de "90% no certifica nada". |

### C3 — Política honesta y realista (costo) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay política, o es una lista de deseos sin cadencia ni costo ("corre mutation testing siempre"). |
| **en-progreso** | Política razonable pero ignora el costo del mutation testing (lo pone en cada PR) o no dice qué excluir. |
| **competente** | Umbral defendible (o explícitamente "sin gate de coverage, gate de mutation sobre lógica crítica"), cadencia realista (diff/nightly por costo), y exclusiones justificadas (generado/infra). |
| **excelente** | Conecta el costo con el hilo de la Fase 6 (la métrica de calidad de IA también cuesta), o propone gate de mutation **solo sobre el código cambiado** en el PR y nightly completo. |

## Errores típicos a marcar
- **Testear el wrapper (B) unitariamente mockeando `requests`**: prueba el mock, no tu código.
- **Testear el orquestador (H) unitariamente con los tres servicios mockeados**: solo prueba que llamaste a los mocks; el valor está en integración.
- **Testear el getter (A) o el DTO (E)** "para subir coverage": test que se rompe al refactorizar sin atrapar bugs.
- **Política con `coverage ≥ 80%` como objetivo** sin reconocer Goodhart: el error que la lección ataca de frente.
- **"Corre mutation testing en cada push"**: ignora el costo; inviable en el camino crítico del PR.
- **Excluir código sin justificar** (o no excluir nada): la exclusión de generado/infra debe argumentarse, no asumirse.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Política impecablemente redactada con vocabulario de manual pero sin un solo ejemplo propio ni un trade-off concreto del codebase de `casos.md`.
- Clasificación correcta de los 8 pero justificaciones intercambiables/genéricas ("es buena práctica") que no podría defender.
- **Verificación sugerida:** pídele que defienda el caso **H** en voz alta: "¿por qué integración y no unitario?" Si entendió, explica que mockear los tres servicios solo prueba los mocks; si dependió de IA, repite la consigna sin el porqué.

## Feedback sugerido (graduado)
> Nunca redactar la política por el alumno.
- **Pista (nivel 1):** "Para cada caso, pregúntate: si escribo este test, ¿qué bug real atraparía? Si la respuesta es 'ninguno, pero sube el coverage', ya tienes tu decisión."
- **Pregunta socrática (nivel 2):** "Si testeas el orquestador (H) mockeando inventario, pago y notificación, y todos los mocks devuelven OK, ¿qué te dice ese test verde sobre el comportamiento real del sistema cuando el pago falla?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu política necesita tres piezas: (1) coverage solo como diagnóstico (mira el 0%, no celebres el 90%), (2) mutation score sobre la lógica crítica (C, F) como medida de fuerza, (3) cadencia por costo (nightly o diff, no cada push). Reescríbela con esas tres y un argumento para cada una. Repasa secciones 4 y 5 de la lección."

## Conexión con el proyecto / capstone
- Es la justificación escrita del **gate de calidad del Capstone F2**: ahí documentarás en tu ADR por qué tu criterio no es "coverage ≥ X" y qué mides en su lugar. La misma disciplina sostiene el DoD de todos los capstones: medir calidad real, no teatro de métricas — incluido el eval harness de la Fase 6.
