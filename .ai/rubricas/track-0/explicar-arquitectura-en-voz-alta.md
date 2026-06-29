---
ejercicio_id: track-0/explicar-arquitectura-en-voz-alta
fase: track-0
sub_unidad: "T0.1"
version: 1
---

# Rúbrica — Explica tu arquitectura en voz alta, en inglés, bajo timer

> Rúbrica **analítica** atada a los `objetivos`. Se evalúa la **estructura de la explicación**
> y la **honestidad y calidad del auto-diagnóstico**, **no** que el inglés hablado sea
> perfecto. Un alumno con inglés tropezado pero con los 4 movimientos y un buen
> auto-diagnóstico está mejor que uno fluido que solo dice "es un programa que procesa
> archivos". El corrector trabaja sobre la **transcripción + autoevaluación** que dejó el
> alumno (no escucha el audio), así que la honestidad de la transcripción es clave.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Explicar en voz alta, en inglés y bajo timer (60–120s), la arquitectura usando la
  estructura de 4 movimientos.
- **O2** — Incluir al menos una decisión técnica con su porqué (trade-off) y un punto de
  mejora honesto.
- **O3** — Diagnosticar los propios puntos débiles a partir de la grabación y proponer su
  corrección.

## Criterios y niveles

### C1 — Estructura de 4 movimientos · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Sin transcripción, o la explicación es una frase vaga ("it processes files") sin estructura; o claramente leyó un guion palabra por palabra (sin muletillas ni titubeos, sospechoso de no ser hablado real). |
| **en-progreso** | Aparecen 1–2 movimientos (what it does + algo del flow) pero faltan el 3 y/o el 4; la duración se va fuera de rango (mucho menos de 60s o muy por encima de 120s). |
| **competente** | Los **4 movimientos** presentes y reconocibles en la transcripción; duración 60–120s; el flujo (input→process→output) es claro. |
| **excelente** | Los 4 movimientos fluidos y bien encadenados; arranca con la frase 1 sólida; el movimiento 4 muestra visión real, no un "podría mejorarlo todo" genérico. |

### C2 — Decisión técnica con porqué (trade-off) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona ninguna decisión técnica, o solo describe qué usó sin ningún "porqué". |
| **en-progreso** | Menciona una herramienta/estructura ("I used a dictionary") pero sin el porqué, o el porqué es circular ("porque funciona"). |
| **competente** | Una decisión con un porqué **defendible** ("a dictionary instead of sorting first because counting is O(n)"); el punto de mejora es concreto. |
| **excelente** | El trade-off contrasta alternativas reales y conecta con una restricción (memoria, latencia, simplicidad); el "what I'd improve" es honesto y específico. |

### C4 — Calidad del auto-diagnóstico · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `autoevaluacion.md`, o "todo bien" sin listar debilidades; o la transcripción está "pulida" (no refleja muletillas/errores reales). |
| **en-progreso** | Lista debilidades genéricas ("mi inglés es malo") sin frases concretas ni correcciones; menos de 3 puntos. |
| **competente** | **3 frases/palabras reales** donde el inglés se cayó, **cada una con su corrección idiomática**; identifica qué atacar primero. |
| **excelente** | El diagnóstico distingue tipos de error (gramática vs muletillas vs velocidad de recuperación de palabras) y prioriza con criterio; las correcciones son idiomáticas, no calcos. |

<!-- C3 (Seguridad) y C5 (Observabilidad/eval) no aplican: ejercicio de comunicación. -->

## Errores típicos a marcar
- **Explicación sin movimiento 3:** describe el qué y el flujo, pero nunca una decisión con
  su porqué. Es lo que separa junior de semi-senior; marcarlo siempre.
- **"What I'd improve" genérico:** "I'd make it better / add more features" en vez de un
  punto concreto (streaming, manejo de errores, tests…).
- **Transcripción demasiado pulida:** sin un solo "um/eh" ni error → probablemente leyó un
  guion o lo "limpió" después; pierde el sentido del ejercicio (auto-espejo honesto).
- **Auto-diagnóstico sin correcciones:** lista los errores pero no escribe la versión correcta.
- **Duración fuera de rango** (30s atropellados o 4 minutos divagando).
- (transversal inglés) Confunde fluidez social con técnica; no detecta que se trabó en el
  vocabulario técnico específico (no en el conversacional).

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- `transcript.md` con prosa perfecta, cero muletillas, vocabulario avanzado uniforme — pero
  `autoevaluacion.md` no detecta ninguna debilidad real: señal de que se transcribió un texto
  generado, no una grabación hablada.
- El auto-diagnóstico usa metalenguaje sofisticado de lingüística que el alumno no podría
  defender.
- **Verificación sugerida:** pedir una **2ª toma en vivo** sobre OTRO proyecto (o el mismo,
  con una variante de la pregunta). El inglés hablado real es consistente entre tomas; un
  texto memorizado/generado se derrumba ante una pregunta inesperada.

## Feedback sugerido (graduado)
> Nunca darle al alumno un guion perfecto para memorizar. De menos a más directo.

- **Pista (nivel 1):** "Repasa tu transcripción contra los 4 movimientos. ¿Cuál de los cuatro
  no aparece? Empieza por agregar ese."
- **Pregunta socrática (nivel 2):** "Dijiste qué usaste, pero no por qué. Si el entrevistador
  pregunta '¿por qué esa estructura y no otra?', ¿qué responderías en una frase?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu transcripción está pulida y sin
  titubeos: eso sugiere que leíste o limpiaste el texto. El valor está en escucharte crudo.
  Vuelve a grabar de una toma, transcribe los errores tal cual, y recién ahí diagnostica. La
  corrección de cada frase la escribes tú — yo solo te confirmo si es idiomática."

## Conexión con el proyecto / capstone
- Esta explicación de 4 movimientos es el ensayo directo de las **mock interviews** de T0.3 y
  del **write-up de trade-offs** que el Definition of Done (§B, punto 8) exige en cada
  capstone. Quien la domina defiende su portafolio en inglés sin congelarse.
