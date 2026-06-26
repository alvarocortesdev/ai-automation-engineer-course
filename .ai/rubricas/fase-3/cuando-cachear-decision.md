---
ejercicio_id: fase-3/cuando-cachear-decision
fase: fase-3
sub_unidad: "3.15"
version: 1
---

# Rúbrica — ¿Cachear o no? Decide y elige la estructura

> Rúbrica analítica para un ejercicio de **razonamiento/diseño**. No hay tests: se evalúa el **criterio**
> y la **justificación con métricas**. Un alumno que cachea los cuatro escenarios "porque acelera" no
> entendió la lección, aunque la prosa suene bien. La señal de dominio es decir "no" con argumentos al
> menos una vez y elegir la estructura por el caso de uso, no por costumbre.

## Objetivos evaluados
- **O1** — Decidir cuándo cachear y cuándo no, con base en las métricas.
- **O2** — Elegir la estructura Redis adecuada al caso.
- **O3** — Razonar TTL/invalidación y el riesgo asociado.

## Criterios y niveles

### C1 — Calidad de la decisión (¿cachear o no, y por qué?) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Decide "cachear" en los cuatro sin mirar las métricas, o no decide. |
| **en-progreso** | Decide bien en 1–2 escenarios pero justifica con generalidades ("es más rápido") en el resto. |
| **competente** | Las cuatro decisiones citan la métrica relevante (frecuencia de lectura vs. de cambio; cuello de botella) y al menos una es un "no/primero otra cosa" defendido. |
| **excelente** | Distingue explícitamente "el patrón de acceso favorece cache" de "pero el problema concreto aquí se arregla mejor de raíz" (escenario A: índice primero). |

### C2 — Elección de estructura · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No elige estructura, o usa "string para todo". |
| **en-progreso** | Elige estructuras pero alguna no calza (p. ej. una list para un contador). |
| **competente** | Cada estructura elegida es razonable para su caso (sesión→hash; contador→string con INCR; etc.). |
| **excelente** | Justifica por qué la estructura elegida es mejor que la alternativa obvia (p. ej. hash vs. string-JSON para una sesión que se edita campo a campo; sorted set vs. string para rate limit de ventana deslizante). |

### C3 — TTL, invalidación y riesgo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona TTL ni invalidación ni riesgos. |
| **en-progreso** | Pone un TTL sin justificar el número, o no nombra ningún riesgo. |
| **competente** | El TTL se ata a la tolerancia de staleness del dato; nombra al menos un riesgo por escenario relevante. |
| **excelente** | Conecta el TTL con la decisión de producto (cuánta desactualización tolera el negocio) y reconoce el thundering herd o la race donde aplica. |

## Errores típicos a marcar
- **Cachear el precio en vivo (escenario C)** con un TTL largo: sirve precios rancios; el negocio exige fidelidad al último segundo. Cachear aquí es contraproducente (puro stale o puro MISS).
- **Saltarse el índice en el escenario A:** proponer cache sin mencionar que el `seq scan` sin índice es la causa raíz y el arreglo permanente/barato.
- **Tratar B y D como "caching":** son usos de Redis (store de sesión compartido; contador distribuido) que no son una cache de la DB. Confundirlo señala que el alumno memorizó "Redis = cache".
- **Estructura por costumbre:** string-JSON para una sesión que conviene como hash; list para un contador.
- **No decir "no" nunca:** si los cuatro terminan en "cachear", falta criterio (releer métricas de C).
- (transversales) decidir sin nombrar la métrica; ignorar el costo/latencia o la observabilidad (medir antes).

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Prosa pulida que recita estrategias de caching (write-through, write-behind, read-through) sin aplicarlas a las métricas concretas de cada escenario.
- Todas las decisiones "cachear" con TTLs redondos sin atarlos a la tolerancia de staleness del caso.
- No reconocer que B y D no son caching, pese a que la lección lo separa explícitamente.
- **Verificación sugerida:** pedir que defienda, sin notas, por qué en el escenario A agregaría el índice **antes** que la cache, y qué pasaría si cacheara el precio en vivo del escenario C con TTL de 5 min.

## Feedback sugerido (graduado)
> Nunca dar la decisión "correcta" antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada escenario, escribe primero dos números: ¿cuánto se lee y cada cuánto cambia el dato? Deja que esa relación guíe la decisión."
- **Pregunta socrática (nivel 2):** "En el escenario A, ¿qué arregla el problema de raíz: cachear, o el índice que falta? ¿Y en el C, qué le pasa a un precio que cambia cada segundo si lo cacheas 5 minutos?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Revisa que al menos una decisión sea 'no cachear': el precio en vivo (C) no se cachea con TTL largo; el catálogo (A) primero necesita el índice. Y separa los usos de Redis que NO son caching (sesión compartida en B, contador en D) del caching de la DB."

## Conexión con el proyecto / capstone
- Esta decisión razonada es el contenido del **ADR de caching** que el [Capstone F3 — API de producción](/fase-3-backend/proyecto/) espera si decides agregar Redis: "agregué/no agregué cache porque medí X; elegí TTL Y porque el dato tolera Z". El criterio vale tanto como el código.
