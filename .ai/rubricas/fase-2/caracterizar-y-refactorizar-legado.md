---
ejercicio_id: fase-2/caracterizar-y-refactorizar-legado
fase: fase-2
sub_unidad: "2.3"
version: 1
---

# Rúbrica — Caracteriza y refactoriza código legado (sin red)

> Rúbrica **analítica** atada a los `objetivos`. El núcleo de este ejercicio NO es el
> refactor (es sencillo): es el **orden** (red primero) y la **disciplina de los dos
> sombreros** (preservar la rareza de la `zona` desconocida en vez de "arreglarla").
> Evaluar que los characterization tests existieran y estuvieran verdes ANTES de tocar
> el código, y que el comportamiento —raro incluido— se preservara.

## Objetivos evaluados
- **O1** — Construir characterization tests (golden master) que pinten el comportamiento actual, con bordes y casos raros, ANTES de refactorizar.
- **O2** — Refactorizar eliminando la duplicación entre ramas con la red en verde, sin alterar el comportamiento.
- **O3** — Aplicar los dos sombreros: preservar el comportamiento raro y registrarlo como deuda separada, no arreglarlo dentro del refactor.

## Criterios y niveles

### C1 — Red de caracterización (el prerrequisito) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay tests, o solo el caso de ejemplo; o los tests afirman lo que la función "debería" hacer y por eso fallan contra el código real. |
| **en-progreso** | Tests para el camino central pero sin **bordes** (499/500, 1999/2000, 999/1000) o sin el caso de `zona` desconocida. |
| **competente** | Cubre cada rama y cada borde de peso por zona + el caso de `zona` desconocida, todo **verde** contra el código sin modificar. |
| **excelente** | Además organiza los casos con `parametrize` legible, comenta por qué cada borde importa, y deja claro que el `esperado` es "lo que hace hoy", no "lo correcto". |

### C2 — Refactor con comportamiento preservado · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Refactorizó **antes** de tener la red, o algún test quedó en rojo, o cambió una salida. |
| **en-progreso** | Aplanó condicionales pero dejó la **duplicación** entre zonas 1 y 2; o extrajo a medias. |
| **competente** | Extrajo `tamano_por_peso` (o equivalente) y compuso con el prefijo de zona; condicionales aplanados; **toda** la suite sigue verde sin tocar `esperado`s. |
| **excelente** | Refactor en pasos pequeños evidenciados (commits/log); la rama internacional (umbral distinto) queda clara y separada de la doméstica. |

### C3 — Dos sombreros / comprensión demostrada · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Arregló" la `zona` desconocida (cambió su salida) dentro del refactor — cambió el comportamiento sin querer (o queriendo). |
| **en-progreso** | Preservó el comportamiento pero `notas.md` no menciona la rareza ni la disciplina de los dos sombreros. |
| **competente** | `notas.md` nombra los smells, los refactorings, y declara explícitamente que preservó la `zona` desconocida porque refactorizar ≠ arreglar bugs. |
| **excelente** | Además propone el arreglo como **deuda separada** (un `fix:` futuro con su test que primero falla), demostrando que entiende los dos sombreros como flujo, no como eslogan. |

## Errores típicos a marcar
- **Refactorizar primero, testear después** (o nunca): invierte el orden; es justo lo que el ejercicio combate. Sin red previa, no hay forma de saber si el refactor cambió algo.
- **Tests que afirman el comportamiento "ideal"**: characterization test pinta lo que HAY, no lo que debería; si fallan contra el código original, están mal planteados para este fin.
- **"Arreglar" la `zona` desconocida** dentro del refactor (que devuelva error, o "desconocida"): cambia el comportamiento → ya no es refactoring.
- **Olvidar los bordes**: probar solo 100/1000/3000 g y perderse 499 vs 500 (donde vive el típico off-by-one).
- **No eliminar la duplicación** zona 1 ≈ zona 2: el objetivo O2 pide exactamente esa extracción.
- (transversal spec-driven) no separar el refactor del eventual fix en commits distintos.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Suite y refactor "perfectos" entregados juntos, sin rastro de que la red existió primero; sospechoso si el `notas.md` no menciona el caso raro (una IA que "arregla" tiende a normalizar la `zona` desconocida).
- `notas.md` con jerga impecable de "golden master / two hats" pero tests que no cubren los bordes: explicación que no calza con el trabajo.
- No puede explicar por qué un characterization test que **pasa** desde el inicio sigue siendo valioso (pinta, no descubre).
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué devuelve `etiqueta_envio(700, 5)` en su versión refactorizada y en la original, y que confirme que coinciden (debe ser `internacional-estandar` en ambas).

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Tu suite está verde contra el código **sin tocar**? Si todavía no, ese es el paso cero — no refactorices nada hasta tenerla. Y revisa los bordes: ¿qué pasa exactamente en 500 g?"
- **Pregunta socrática (nivel 2):** "¿Qué devuelve hoy la función con `zona=5`? ¿Tu refactor mantiene esa misma respuesta? Si la cambiaste 'porque parecía un bug', ¿qué sombrero te pusiste sin querer?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Zona 1 y 2 comparten umbrales 500/2000: extrae `tamano_por_peso(peso)` → `'ligero'/'medio'/'pesado'` y compón `f'{prefijo}-{tamano}'`. La rama internacional (zona 3 y cualquier otra) conserva su umbral 1000 — eso preserva el caso `zona` desconocida. Anota ese caso en `notas.md` como deuda, no lo arregles. Repasa secciones 4.1 y 5 antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Es la habilidad central del **Capstone F2** llevada al caso realista: casi todo el código que tocarás en producción llega sin tests. Caracterizar antes de mover es el método; los dos sombreros son la disciplina. Profundiza en 2.12 (Debugging y código legado).
