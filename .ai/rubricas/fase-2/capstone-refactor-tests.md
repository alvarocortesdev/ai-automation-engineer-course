---
ejercicio_id: fase-2/capstone-refactor-tests
fase: fase-2
sub_unidad: "2.P"
version: 1
---

# Rúbrica — Capstone Fase 2: Refactor + suite de tests

> Rúbrica **analítica** del capstone, atada a los `objetivos` del contrato y al
> **Definition of Done único** (§B, IDs 1, 2, 8, 9). No es una nota: es el mapa de
> qué observar. El producto no es "código más bonito": es **evidencia** de que el
> comportamiento se conservó (caracterización), de que la red sirve (mutation
> score), y de que cada decisión se defiende (ADRs). Un alumno puede dejar el
> código precioso y haber **reescrito** (no refactorizado); otro puede dejar un
> diseño modesto pero impecablemente probado y documentado. La rúbrica premia al
> segundo.

## Objetivos evaluados
- **O1** — Refactorizar un módulo legado con SOLID guiado por smells, **sin cambiar
  el comportamiento observable**, probado por una red de tests de caracterización.
- **O2** — Diseñar una suite cuya calidad se mide por **mutation score / aserciones
  reales** (no coverage%), y justificar qué se testeó y qué no.
- **O3** — Documentar el diseño en `ARQUITECTURA.md` (inglés) + ADRs y montar un
  **CI** que corre lint + tests.

> **Vara mínima de "competente":** caracterización verde **antes** del primer
> cambio de producción · al menos un núcleo puro extraído · mutation score
> reportado (partida → final) con sobrevivientes justificados · 2–3 ADRs · CI
> verde · Conventional Commits.

## Criterios y niveles

### C1 — Refactor que conserva el comportamiento (corrección) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay tests de caracterización, o se reescribió el módulo desde cero (no hay forma de probar que el comportamiento se conservó), o la herramienta ya no produce la misma salida. |
| **en-progreso** | Hay caracterización, pero se escribió **después** de empezar a cambiar el código, o el refactor es cosmético (renombres) sin separar responsabilidades. |
| **competente** | Caracterización verde **antes** del primer cambio; el comportamiento observable es idéntico; se extrajo al menos un **núcleo puro** sin I/O (SRP) con dependencias inyectadas (DIP light); los smells nombrados fueron eliminados. |
| **excelente** | Además, el historial muestra el refactor en **pasos pequeños** (cada commit deja la red verde), y el alumno aplicó SOLID **solo donde el smell lo justificaba**, resistiendo la sobre-abstracción (lo argumenta en un ADR). |

### C2 — Calidad de la suite medida por mutation, no por coverage · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No corrió mutation testing, o presenta el **% de coverage** como métrica de calidad ("92%, listo"). |
| **en-progreso** | Corrió `mutmut` pero no contrasta partida vs. final, o quedan sobrevivientes no-equivalentes sin matar y sin justificar, o confunde score con coverage. |
| **competente** | Reporta mutation score de partida y final; los sobrevivientes restantes están **justificados** (equivalentes, con la entrada que *debería* distinguirlos); hay tests de **borde exacto** (umbrales) y el alumno dice qué decidió **no** testear. |
| **excelente** | Además, integra el mutation testing como **gate de CI** (o explica en un ADR por qué lo deja manual y con qué umbral), y articula la regla general: los mutantes de comparación solo mueren en el borde exacto. |

### C3 — Documentación y comunicación (ARQUITECTURA + ADRs, en inglés) · mapea: O3 · DoD 1, 8
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `SPEC.md` ni ADRs, o el `ARQUITECTURA.md` no existe / está vacío. |
| **en-progreso** | Hay documentos, pero los ADRs solo registran lo obvio ("extraje una función") sin contexto ni opciones, o la documentación está solo en español (DoD 8 pide inglés). |
| **competente** | `SPEC.md` + `ARQUITECTURA.md` en inglés que explica el diseño; **2–3 ADRs** con contexto, opciones y consecuencia; write-up de trade-offs (qué elegí, qué medí, qué falló). |
| **excelente** | Algún ADR documenta una decisión que el alumno **dudó** (incluida una abstracción que decidió **no** crear) con un razonamiento defendible; el `ARQUITECTURA.md` enlaza los ADRs y trae un diagrama. |

### C4 — Pipeline e higiene de repo (CI + Conventional Commits) · mapea: O3 · DoD 2, 9
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay workflow de CI, o no corre (rojo permanente), o el historial es un único commit gigante. |
| **en-progreso** | CI corre tests pero no lint, o pasa pero el historial mezcla pasos sin convención. |
| **competente** | CI **verde** con lint + tests en cada push; **Conventional Commits** en pasos pequeños que dejan la red verde. |
| **excelente** | El pipeline incluye (o el alumno justifica la ausencia de) un paso de mutation; commits atómicos legibles que cuentan la historia del refactor (`test:` → `refactor:` → `test:`). |

## Errores típicos a marcar
- **Rewrite disfrazado de refactor:** borró y reescribió; no hay caracterización previa que pruebe la conservación del comportamiento. Es **el** error que invalida el capstone aunque el código final sea bueno.
- **Coverage como métrica de calidad:** entrega "X% de coverage" en vez de mutation score / aserciones reales (contradice el DoD 2 y la 2.9).
- **Tests fuera del borde:** usa `cantidad == 3` o `99` creyendo que mata el mutante `<=`→`<`; solo el **valor exacto** del umbral lo distingue.
- **Sobre-abstracción ("pattern-itis"):** Factory + interfaz por clase + capas en un script de 80 líneas, sin un smell que lo justifique. SOLID donde duele, no en todas partes.
- **Big-bang commit:** todo en un único commit "refactor", imposible de revisar/revertir; sin Conventional Commits.
- **Caracterización no determinista:** test que depende de `date.today()` real (pasa hoy, falla mañana) en vez de inyectar la fecha.
- **ADRs vacíos:** registran lo obvio sin contexto/opciones, o documentan solo lo que salió bien (nunca la decisión dudada).
- (transversal) sustituir `print` por logging estructurado se valora como *bonus* de observabilidad, no se exige.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código final pulido y "perfecto" pero **sin** historial de pasos pequeños ni tests de caracterización: huele a "pídele a la IA el refactor terminado".
- `ARQUITECTURA.md` sofisticado que menciona patrones que el código **no usa**, o ADRs que defienden decisiones que no están en el diseño (la explicación no calza con el código).
- Mutation score reportado "100%" sin evidencia de sobrevivientes intermedios ni de qué tests de borde los mataron.
- **Verificación sugerida:** pídele que, sin ejecutar, prediga qué mutante sobrevive si cambia un umbral `<=` por `<`, y qué test exacto lo mataría. Si refactorizó de verdad, lo resuelve al instante. Pídele también que justifique **una abstracción que NO creó**: si solo sabe defender lo que añadió, no internalizó la crítica a SOLID.

## Feedback sugerido (graduado)
> Nunca dar el refactor ni los tests de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tienes un test que pruebe que la salida de la herramienta es la misma **antes** y **después** de tu refactor? Si no, ¿cómo sabes que no rompiste nada? Empieza por ahí, antes de tocar producción."
- **Pregunta socrática (nivel 2):** "Corre `mutmut`. ¿Sobrevive algún mutante con tu coverage alto? Toma uno: ¿qué **entrada exacta** distinguiría el código original del mutado? ¿Tu suite usa esa entrada?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Extrae la lógica de decisión a una función pura `evaluar(item, hoy)` sin `open` ni `print`; deja `run` como adapter que la orquesta; mantén la caracterización verde en cada paso. Para el score, agrega tests en los umbrales **exactos** (`cantidad == 2`, días `== 0`, días `== 3`). Documenta en un ADR por qué NO añadiste una capa extra. Repasa la lección del capstone, sección del ciclo de tres pasos."

## Conexión con el proyecto / capstone
- **Es** el capstone de la fase: cierra el constructive alignment de la Fase 2 (clean code + smells + SOLID + testing + mutation + ADRs) en una sola entrega medida por el DoD único. El núcleo puro que el alumno extrae aquí es la **capa de dominio** que en la [Fase 3](/fase-3-backend/) vivirá detrás de un endpoint con ports & adapters de verdad; la red de tests es la que le dará permiso de refactorizar bajo presión en cada fase siguiente; y el reflejo de medir la *fuerza real* de la suite es el mismo que en la [Fase 6](/fase-6-ai-engineering/) exigirá un **eval harness** antes de confiar en un LLM.
