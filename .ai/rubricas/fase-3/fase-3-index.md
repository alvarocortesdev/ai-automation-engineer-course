---
ejercicio_id: fase-3/fase-3-index
fase: fase-3
sub_unidad: "3.0"
version: 1
---

# Rúbrica — Diagnóstico, plan y mapa al capstone de Fase 3

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa
> con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué
> observar y cómo dar feedback. Este es un ejercicio de **orientación**: se
> evalúa **honestidad, concreción y alineación**, nunca una "respuesta correcta".

## Objetivos evaluados

- O1: Autoevaluar con honestidad el nivel de partida en las 16 sub-unidades.
- O2: Diseñar un plan realista que decida explícitamente sobre las 5 opcionales según el rol objetivo.
- O3: Mapear cada punto del Definition of Done del Capstone F3 a las sub-unidades que lo enseñan.

## Criterios y niveles

### C1 — Diagnóstico honesto y completo · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan sub-unidades en la tabla (cubre menos de 16), o no asigna nivel. |
| **en-progreso** | Cubre las 16 pero los niveles son inverosímiles (casi todo "lo sé hacer" sin haber tocado el tema) o usa etiquetas distintas a las pedidas. |
| **competente** | Las 16 con nivel defendible; la mezcla es realista (varios `nuevo` si el alumno parte de cero); aplica el criterio concreto de "lo sé hacer". |
| **excelente** | Además, junto a cada "lo sé hacer" añade la **evidencia** ("escribí un JOIN de 3 tablas la semana pasada") y reconoce zonas grises con matiz. |

### C2 — Plan realista con decisión sobre opcionales · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay bloques concretos (solo "estudiar más"), o no menciona las opcionales. |
| **en-progreso** | Hay bloques pero vagos (sin día/hora/duración), o decide sobre las opcionales sin justificar, o las deja en "quizás". |
| **competente** | Bloques semanales concretos + ritual de repaso; **decide hacer o saltar cada una de las 5 opcionales** con una razón. |
| **excelente** | La justificación de las opcionales está **ligada al rol objetivo y a fases futuras** (ej.: Redis por *semantic caching* de F6; salta GraphQL/NestJS por foco IA/Python) y el plan es sostenible (pocas horas reales > muchas idealizadas). |

### C3 — Mapa al Definition of Done (constructive alignment) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No existe el mapa, o conecta menos de la mitad de los 7 puntos del DoD. |
| **en-progreso** | Conecta varios puntos pero con asociaciones forzadas o erróneas (p. ej. mapea "seguridad" solo a 3.8). |
| **competente** | Los **7** puntos conectados con al menos una sub-unidad correcta cada uno (seguridad→3.12/3.13; resiliencia→3.14; datos→3.1–3.5; etc.). |
| **excelente** | Mapeo fino y defendible: ubica bien los puntos difíciles (ADRs/arquitectura→3.9; tests en CI como hábito de F2 reaplicado; observabilidad mínima como nueva), y nota qué puntos la fase aún **no** cubre del todo (trazas OTel, IA). |

### C4 — Comprensión demostrada (honestidad metacognitiva) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Autoevaluación sin reflexión; copia las etiquetas sin pensar. |
| **en-progreso** | Reconoce algunas debilidades pero sin conectar el diagnóstico con el plan. |
| **competente** | El plan **responde** al diagnóstico: dedica más tiempo a lo marcado `nuevo`. |
| **excelente** | Explicita el vínculo diagnóstico→plan→capstone y nombra el riesgo de sobreconfianza en su propia tabla. |

## Errores típicos a marcar

- Diagnóstico inflado: casi todo en "lo sé hacer" sin evidencia (sobreconfianza / Dunning-Kruger).
- Plan de buenas intenciones ("estudiaré 2 h diarias") sin bloques concretos ni ritual de repaso.
- Ignorar las opcionales o dejarlas en "quizás" en vez de decidir con criterio.
- Mapa al DoD con asociaciones forzadas (mapear todo a 3.8 "porque es el backend") o que omite puntos.
- Confundir el camino crítico con las opcionales (tratar Prisma/NestJS como obligatorios).
- Plan que no se deriva del diagnóstico (marca 3.3 como `nuevo` pero no le asigna tiempo extra).

## Señales de dependencia-IA

- Plan genérico y pulido que podría aplicar a cualquier persona (sin día/hora reales ni mención al contexto del alumno) → señal de texto generado.
- Diagnóstico que usa vocabulario sofisticado de las sub-unidades sin haberlas cursado ("optimistic locking", "PKCE") junto a un nivel "nuevo" contradictorio.
- Mapa al DoD perfecto y exhaustivo pero el plan ignora por completo la seguridad o la resiliencia: la coherencia interna no calza.
- Verificación sugerida: pídele que explique, en una frase suya, **por qué** decidió saltar o hacer una opcional concreta.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Revisa tu columna de niveles: ¿cuántos marcaste 'lo sé hacer'? Para cada uno, ¿tienes una evidencia concreta y reciente? Si no, probablemente sea 'lo reconozco'."
- **Pregunta socrática (nivel 2):** "Tu plan, ¿le da más tiempo a lo que marcaste 'nuevo'? Si dedicas lo mismo a todo, el diagnóstico no está sirviendo de nada."
- **Dirección concreta (nivel 3, solo tras intento real):** "Para decidir cada opcional, hazte dos preguntas: ¿el rol que busco la pide? ¿me desbloquea una fase posterior? Si ambas son 'no', sáltala y déjala anotada para después. Escribe esa razón en una línea junto a cada una."

## Conexión con el proyecto / capstone

- Este ejercicio convierte el capstone `3.P` (API de producción) en el **norte
  explícito** de la fase: el alumno entra sabiendo qué construye y qué
  sub-unidad le aporta cada pieza del Definition of Done.
