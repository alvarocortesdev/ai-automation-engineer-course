---
ejercicio_id: fase-2/solid-juicio-sobre-abstraccion
fase: fase-2
sub_unidad: "2.4"
version: 1
---

# Rúbrica — El juicio: ¿abstraer o no?

> Rúbrica **analítica** para un ejercicio de **razonamiento**. No hay respuesta correcta única: lo que se
> evalúa es la **calidad del trade-off**, no el bando elegido. Un alumno que decide "no abstraer" con un
> argumento sólido vale más que uno que decide "abstraer" porque "SOLID se cumple siempre". El corrector
> califica el razonamiento; **no** premia ni castiga la decisión por sí misma.

## Objetivos evaluados
- **O1** — Evaluar el trade-off aplicar-principio vs. sobre-abstracción (YAGNI / Rule of Three).
- **O2** — Justificar cada decisión con el smell presente/ausente + un argumento a favor y uno en contra.
- **O3** — Definir un gatillo observable que convertiría un "no abstraer" en un refactor futuro.

> Orientación del corrector (no es "la respuesta", es la dirección defendible): **(1)** dejar concreto es
> defendible (especulación pura, sin smell); abstraer aquí es speculative generality. **(2)** invertir la
> dependencia es lo razonable (DOS fuerzas presentes: testabilidad *hoy* + segundo proveedor *probable*); el
> dolor de testear ya es un smell real. **(3)** NO separar `Usuario` suele ser lo correcto (validar email y
> componer el nombre son la misma cohesión; separar crea fragmentos anémicos y shotgun surgery). Cualquier
> decisión contraria **bien defendida con un trade-off explícito** también es válida.

## Criterios y niveles

### C1 — Calidad del trade-off (a favor y en contra) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Decisiones sin argumento, o "hay que cumplir SOLID / hay que abstraer siempre" sin contrapeso. |
| **en-progreso** | Da un argumento por decisión, pero solo de un lado (solo a favor, o solo "no, por las dudas"). |
| **competente** | Cada escenario tiene un principio **a favor** y un argumento **en contra** nombrado (YAGNI / Rule of Three / costo de indirección / testabilidad). |
| **excelente** | Pesa las fuerzas explícitamente (p. ej. distingue por qué el escenario 2 inclina a abstraer y el 1 no) y reconoce la incertidumbre. |

### C2 — Diagnóstico del smell (presente o ausente) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra smells, o inventa uno que no aplica. |
| **en-progreso** | Nombra el smell solo cuando decide abstraer; cuando decide no abstraer, no articula la **ausencia** de smell. |
| **competente** | Identifica el smell presente (switch que crece, acoplamiento que impide testear) **y** reconoce la ausencia de smell como razón válida para no abstraer. |
| **excelente** | Distingue un eje de variación **real y presente** de uno **especulado**, con vocabulario preciso (speculative generality, divergent change). |

### C3 — Gatillo observable · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Las decisiones de "no abstraer" no traen ningún criterio de cambio futuro ("ya veré"). |
| **en-progreso** | Menciona vagamente "si crece" sin un evento observable. |
| **competente** | Cada "no abstraer" trae un gatillo concreto ("si aparece un 2.º exportador real", "si un canal supera N líneas"). |
| **excelente** | El gatillo es medible y conecta con la Rule of Three / con registrar la decisión en un ADR. |

## Errores típicos a marcar
- **Dogmatismo:** "SOLID se cumple siempre" → abstrae los tres sin pesar costo. Es justo el antipatrón de la lección.
- **Nihilismo opuesto:** "nunca abstraer, YAGNI todo" → deja el escenario 2 concreto pese a tener testabilidad rota *hoy* y un 2.º proveedor probable.
- **Separar `Usuario` por SRP mal entendido:** tratar "una clase = un método" como regla; no ver que validar y nombrar son la misma cohesión.
- **Decisión sin contrapeso:** dar solo el argumento del lado elegido (no hay trade-off si no nombras lo que sacrificas).
- **Gatillo ausente:** "no abstraigo" sin decir qué lo cambiaría = una opinión, no una decisión de ingeniería.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Prosa pulida y genérica que recita definiciones de SOLID pero **no se compromete** con una decisión por escenario.
- Los tres escenarios resueltos con la misma plantilla impersonal, sin enganchar con los detalles concretos (el "quizás algún día" del 1, las dos fuerzas del 2).
- Vocabulario de patrones avanzado sin poder defender la decisión en voz alta.
- **Verificación sugerida:** pedir que **invierta** una de sus decisiones y la defienda igual de bien. Si entendió el trade-off, puede argumentar ambos lados; si copió, solo sostiene el texto que ya tiene.

## Feedback sugerido (graduado)
> Nunca dar "la respuesta" — no la hay; guiar el razonamiento.
- **Pista (nivel 1):** "En el escenario que dejaste concreto, ¿hay un smell **hoy**, o estás imaginando uno futuro? Nombra cuál de los dos es."
- **Pregunta socrática (nivel 2):** "¿Qué te cuesta cada decisión? Si abstraes el reporte ahora, ¿qué pagas? Si no inviertes la dependencia de pagos, ¿qué no puedes hacer **hoy**?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Tu decisión está bien, pero le falta el contrapeso y el gatillo. Para cada 'no abstraigo', escribe el evento observable que te haría cambiar de opinión (la Rule of Three es un buen gatillo). Eso convierte una opinión en una decisión defendible en un ADR."

## Conexión con el proyecto / capstone
- Es el ensayo del **ADR del Capstone F2**: ahí documentarás dónde aplicaste SOLID y, sobre todo, **dónde decidiste no abstraer y por qué**. Este ejercicio entrena exactamente esa redacción de trade-offs que un reviewer semi-senior espera leer.
