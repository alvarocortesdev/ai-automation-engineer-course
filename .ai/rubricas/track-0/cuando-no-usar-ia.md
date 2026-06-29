---
ejercicio_id: track-0/cuando-no-usar-ia
fase: track-0
sub_unidad: "T0.9"
version: 1
---

# Rúbrica — Defiende el cuándo-NO en una entrevista hostil

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio**: si
> el alumno rompe la falsa dicotomía "o sabes o usas IA" anclando en evidencia (no en adjetivos), y si sabe
> defender el **cuándo-NO** con porqués de ingeniería que tienen un costo real detrás. No hay una única
> defensa correcta, pero sobrevender o evadir son señales de no haberlo entendido.

## Objetivos evaluados
- **O1** — Defender el uso de IA sin sobrevender: romper la dicotomía, anclar en evidencia, cerrar con
  Primero-Sin-IA.
- **O2** — Explicar el trade-off del cuándo-NO: situaciones concretas con porqué de ingeniería y costo.

## Criterios y niveles

### C1 — Respuesta hablada: rompe la dicotomía + evidencia + Primero-Sin-IA · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Cae en una de las dos trampas: "la IA hace casi todo" (vibe-coder) o "no uso IA" (purista); o se pone a la defensiva/se disculpa. |
| **en-progreso** | Intenta el punto medio pero es genérico ("uso IA con responsabilidad") sin evidencia concreta ni cierre con Primero-Sin-IA. |
| **competente** | Rompe la dicotomía ("las dos cosas, esa es la habilidad"), ancla en **evidencia concreta del repo** (spec propio, tests, review, evals) y cierra conectando con Primero-Sin-IA. |
| **excelente** | Suena natural para decir en voz alta (no ensayo), usa un artefacto **específico** ("este ADR", "estos tests") y toma la honestidad de la reclutadora como aliada ("te lo muestro abriendo el repo ahora"). |

### C2 — Lista cuándo-NO con porqué de ingeniería · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Menos de 3 situaciones, o los porqués son preferencias ("no me gusta") sin costo de ingeniería. |
| **en-progreso** | 3 situaciones pero algún porqué es vago o no se distingue de "porque sí"; o son todas la misma idea repetida. |
| **competente** | **≥3** situaciones **distintas** (aprendizaje, debugging con modelo mental, código crítico/seguridad, costo de revisar > costo de escribir), cada una con un porqué que nombra un **costo real**. |
| **excelente** | Los porqués citan el costo en términos medibles o concretos (tiempo de revisión, riesgo de un bug en auth/pagos, deuda de aprendizaje que se paga en la próxima entrevista) y conecta al menos uno con la regla Primero-Sin-IA. |

### C3 — Trade-off explícito (gano / pierdo) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Solo nombra lo que gana (vende el "no usar IA" como gratis) o solo lo que pierde. |
| **en-progreso** | Menciona ambos lados pero de forma trivial o sin que se entienda por qué el cambio vale la pena ahí. |
| **competente** | Nombra **qué gana y qué pierde** explícitamente, y deja claro por qué en **esa** situación el trade vale la pena. |
| **excelente** | Cuantifica o concreta el costo (p. ej. "pierdo velocidad pero un error en cobro le cuesta dinero al cliente y confianza al equipo") y muestra que el criterio es *situacional*, no dogmático. |

### C4 — Línea anti-sobreventa · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **competente** | Identifica una frase autodestructiva concreta (vibe-coder o purista) y por qué hunde. |
| **excelente** | La frase prohibida es realista (la que un candidato diría por nervios) y el porqué conecta con la lógica del puesto (indefendible en live coding / suena lento e irrelevante). |

## Errores típicos a marcar
- **Caer en la trampa:** responder "la IA hace casi todo" o "no la uso" —las dos descalifican; el punto es romperla.
- **Ponerse a la defensiva o disculparse:** la pregunta es una dicotomía falsa; disculparse la acepta.
- **Evidencia abstracta:** "soy buen ingeniero", "uso buenas prácticas" no es evidencia; la reclutadora tiene el repo abierto, hay que apuntar a algo abrible.
- **Cuándo-NO como preferencia:** "no me gusta usar IA para X" no es ingeniería; falta el costo real.
- **Trade-off de un solo lado:** vender el "no usar IA" como gratis (sin costo) o como puro sacrificio (sin ganancia) —toda decisión cuesta y rinde algo.
- (transversal) no conectar con Primero-Sin-IA: la defensa más fuerte cierra ahí ("la uso para multiplicar, no para pensar; por eso puedo defenderlo sin la IA al lado").

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Defensa pulida y "perfecta" pero genérica, sin un solo artefacto específico que el alumno podría abrir en su repo.
- Lista cuándo-NO que suena a viñetas de un blog (correcta pero impersonal), sin un ejemplo propio.
- **Verificación sugerida:** pedir que **diga la respuesta en voz alta en 45 segundos** o que dé un ejemplo real propio de "una vez NO usé IA en X porque…". Si lo interiorizó, fluye; si lo generó, suena recitado y sin caso propio.

## Feedback sugerido (graduado)
> Nunca reescribir la defensa por el alumno.
- **Pista (nivel 1):** "Lee tu primera frase. ¿Estás aceptando la dicotomía (defendiéndote) o rompiéndola? Si empieza con 'la verdad es que sí uso bastante IA, pero…', ya entraste a la defensiva."
- **Pregunta socrática (nivel 2):** "La reclutadora tiene tu repo abierto. ¿Qué archivo concreto le pedirías que abra para probar tu punto? Y en tu lista cuándo-NO: cada porqué, ¿tiene un costo que podrías ponerle número o nombre, o es una preferencia?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Reestructura: (1) rompe la dicotomía en la primera frase ('las dos, y esa es la habilidad'); (2) ancla en un artefacto específico de tu repo; (3) cierra con Primero-Sin-IA. Para el cuándo-NO, asegúrate de que cada porqué nombre un costo (deuda de aprendizaje, riesgo en código crítico, tiempo de revisión). Para el trade-off, escribe las dos columnas —gano / pierdo— y por qué aquí el saldo es a favor de no delegar."

## Conexión con el proyecto / capstone
- Esta defensa es una de las respuestas-ancla que se practican en los mocks de [T0.3], y el músculo
  cuándo-NO alimenta la honestidad de la historia de falla en producción de [T0.4] (reconocer límites es
  seniority). En remoto-USD, esta misma defensa se da en inglés ([T0.1]).
