---
ejercicio_id: fase-8/monolito-vs-microservicios-decision
fase: fase-8
sub_unidad: "8.3"
version: 1
---

# Rúbrica — Decisor: ¿monolito modular o microservicios?

> Rúbrica **analítica** para un ejercicio de **razonamiento**. Lo que se evalúa es el **criterio de
> decisión** (la restricción dominante y el trade-off), no si el alumno coincidió con una respuesta
> única. Los escenarios 1–4 tienen una respuesta claramente mejor; el **escenario 5 admite ambas**
> decisiones si están bien defendidas. Un alumno puede acertar la decisión "por moda" y seguir sin
> entender; otro puede defender la opción menos común con un trade-off impecable. La rúbrica distingue
> ambos casos.

## Objetivos evaluados
- **O1** — Decidir nombrando la **restricción dominante**.
- **O2** — Nombrar un **costo asumido** (microservicios) o un **gatillo** (monolito) por decisión, y
  reconocer microservicios prematuros.

## Criterios y niveles

### C1 — Corrección de las decisiones 1–4 · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan escenarios, o las decisiones contradicen la restricción presente (p. ej. microservicios para el MVP de tres personas "porque escala mejor"). |
| **en-progreso** | Acierta 2–3 decisiones, pero justifica con motivos genéricos ("más limpio", "más moderno") en vez de la restricción real. |
| **competente** | Acierta las cuatro (1→monolito, 2→microservicios, 3→microservicios/extraer ese componente, 4→monolito) y nombra la restricción dominante correcta en cada una. |
| **excelente** | Además distingue que las razones 2 y 3 son distintas (organizacional vs escala), y que 1 y 4 comparten la misma falla (no hay restricción real, solo especulación / estética). |

### C2 — Costo o gatillo por decisión · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra costos ni gatillos; las decisiones son afirmaciones sin consecuencia. |
| **en-progreso** | Nombra costos/gatillos vagos ("es más complejo", "cuando crezca"). |
| **competente** | Cada decisión de microservicios nombra un costo concreto (red, saga, N despliegues); cada decisión de monolito nombra un gatillo **observable** (p. ej. "cuando un componente necesite escalar 10x distinto", "cuando 3+ equipos bloqueen releases"). |
| **excelente** | Los gatillos son métricas o eventos medibles, y el alumno nota que el gatillo de monolito = una de las cuatro razones reales activándose. |

### C3 — Calidad del trade-off en el caso 5 (juicio) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Esquiva el caso 5, o decide sin defender contra la alternativa. |
| **en-progreso** | Decide y da una fuerza a favor, pero no nombra qué renuncia / qué riesgo acepta. |
| **competente** | Decide, da una fuerza a favor **y** una en contra, y nombra el desempate (¿la fuerza pro-microservicios es real-y-presente o especulada?). |
| **excelente** | Reconoce que "un par de conflictos al mes" no es bloqueo crítico → favorece gobernar mejor el monolito (ownership por módulo, dueños de despliegue) antes de pagar el costo distribuido; o defiende extraer el primer servicio con un plan incremental. Cualquiera de las dos, con el trade-off nombrado, es excelente. |

## Errores típicos a marcar
- **"Microservicios escalan mejor" sin contexto** en el escenario 1 o 4: un monolito escala horizontalmente igual; lo que cambia es escalar *por componente* (solo aplica al escenario 3).
- **Confundir el escenario 2 (organizacional) con el 3 (escala):** son razones distintas; mezclarlas indica que no internalizó las cuatro causas.
- **Gatillos no observables:** "cuando sea grande", "a futuro" — no son gatillos. Pedir una métrica o evento concreto.
- **Decidir el caso 5 por reflejo** ("30 ingenieros ya es para microservicios") sin medir que el dolor (conflictos de despliegue) aún no es crítico.
- (transversal) **No nombrar ningún costo de microservicios:** señal de que vendió la opción sin verla completa; falta un trade-off defendible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Cinco decisiones "correctas" con justificaciones genéricas idénticas en estructura, sin la restricción específica de cada caso (texto plausible pero intercambiable).
- El caso 5 resuelto con una respuesta tajante y sin trade-off, como si tuviera respuesta única (la lección y el README insisten en que no la tiene).
- Vocabulario de arquitectura por encima del resto del razonamiento, sin poder defenderlo.
- **Verificación sugerida:** pídele que invente un **sexto escenario** propio donde la decisión correcta sea la menos intuitiva, y que lo defienda. Si razonó de verdad, lo construye; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar las respuestas antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada escenario, recorre las cuatro razones reales de la sección 4.4 y marca cuáles están **presentes de verdad hoy**. Si ninguna lo está, ¿qué te dice eso?"
- **Pregunta socrática (nivel 2):** "En el escenario 4, ¿qué problema concreto resolverían los microservicios que el equipo tenga **hoy**? Si no encuentras ninguno, ¿en qué se parece a la pattern-itis de 2.5?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Revisa que cada decisión de monolito tenga un gatillo **medible** (un número o un evento), no 'cuando crezca'. Y en el caso 5, nombra explícitamente qué renuncias al elegir lo que elegiste: sin eso, no es un trade-off, es una preferencia."

## Conexión con el proyecto / capstone
- Es el músculo exacto del [capstone F8](/fase-8-system-design/proyecto/): para cada uno de los tres
  sistemas en papel, la primera decisión es "monolito modular o servicios", y debe quedar justificada en
  un ADR con su restricción dominante y su trade-off. Este ejercicio entrena esa decisión en frío.
