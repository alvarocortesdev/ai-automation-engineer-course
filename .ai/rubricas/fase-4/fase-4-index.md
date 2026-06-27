---
ejercicio_id: fase-4/fase-4-index
fase: fase-4
sub_unidad: "4.0"
version: 1
---

# Rúbrica — Diagnóstico, plan y mapa al capstone de Fase 4

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa
> con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué
> observar y cómo dar feedback. Este es un ejercicio de **orientación**: se
> evalúa **honestidad, concreción y alineación**, nunca una "respuesta correcta".

## Objetivos evaluados

- O1: Autoevaluar con honestidad el nivel de partida en las 11 sub-unidades.
- O2: Diseñar un plan realista que decida explícitamente sobre la opcional (4.9) según el rol objetivo.
- O3: Mapear cada punto del Definition of Done del Capstone F4 a las sub-unidades que lo enseñan.

## Criterios y niveles

### C1 — Diagnóstico honesto y completo · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Faltan sub-unidades en la tabla (cubre menos de 11), o no asigna nivel. |
| **en-progreso** | Cubre las 11 pero los niveles son inverosímiles (casi todo "lo sé hacer" sin haber tocado el tema) o usa etiquetas distintas a las pedidas. |
| **competente** | Las 11 con nivel defendible; la mezcla es realista (varios `nuevo` si parte de cero); aplica el criterio concreto de "lo sé hacer" (maquetar / Server vs Client / modal accesible). |
| **excelente** | Además, junto a cada "lo sé hacer" añade la **evidencia** ("monté un formulario controlado en React la semana pasada") y reconoce zonas grises con matiz. |

### C2 — Plan realista con decisión sobre la opcional · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay bloques concretos (solo "estudiar más"), o no menciona la opcional 4.9. |
| **en-progreso** | Hay bloques pero vagos (sin día/hora/duración), o decide sobre 4.9 sin justificar, o la deja en "quizás". |
| **competente** | Bloques semanales concretos + ritual de repaso; **decide hacer o saltar 4.9** con una razón. |
| **excelente** | La justificación de 4.9 está **ligada al rol objetivo** (ej.: salta design systems por foco en capstone con Tailwind; o la hace porque apunta a roles de UI a escala) y el plan es sostenible (pocas horas reales > muchas idealizadas), con más tiempo a lo marcado `nuevo`. |

### C3 — Mapa al Definition of Done (constructive alignment) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No existe el mapa, o conecta menos de la mitad de los 7 puntos del DoD. |
| **en-progreso** | Conecta varios puntos pero con asociaciones forzadas o erróneas (p. ej. mapea "a11y" solo a 4.6 Next.js, o ignora que el gate vive en 4.4/4.10). |
| **competente** | Los **7** puntos conectados con al menos una sub-unidad correcta cada uno (a11y+estados→4.4/4.10; seguridad de salida del LLM→4.11; estado correcto→4.7/4.8). |
| **excelente** | Mapeo fino y defendible: ubica bien los difíciles (observabilidad→4.6 + contrato con la API de F3; spec/ADR como hábito de F0/F2 reaplicado), y nota qué puntos la fase aún **no** cubre del todo (trazas OTel, eval harness de IA), que llegan en F5/F6. |

### C4 — Comprensión demostrada (honestidad metacognitiva) · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Autoevaluación sin reflexión; copia las etiquetas sin pensar. |
| **en-progreso** | Reconoce algunas debilidades pero sin conectar el diagnóstico con el plan. |
| **competente** | El plan **responde** al diagnóstico: dedica más tiempo a lo marcado `nuevo`. |
| **excelente** | Explicita el vínculo diagnóstico→plan→capstone y nombra el riesgo de sobreconfianza en su propia tabla (sobre todo en React/Next.js, donde "ver un tutorial" se confunde con "saber hacer"). |

## Errores típicos a marcar

- Diagnóstico inflado: casi todo en "lo sé hacer" sin evidencia (sobreconfianza / Dunning-Kruger), típico en React por haber "visto tutoriales".
- Plan de buenas intenciones ("estudiaré 2 h diarias") sin bloques concretos ni ritual de repaso.
- Tratar 4.9 (design systems) como obligatoria, o dejarla en "quizás" en vez de decidir con criterio.
- Mapa al DoD con asociaciones forzadas (mapear todo a 4.6 "porque es Next.js") o que omite el punto 5 (a11y + estados), que es el gate estrella de la fase.
- Subestimar accesibilidad y estados como "extras": el ejercicio mide si entiende que son **gate**.
- Plan que no se deriva del diagnóstico (marca 4.5/4.6 como `nuevo` pero no les asigna tiempo extra).

## Señales de dependencia-IA

- Plan genérico y pulido que podría aplicar a cualquier persona (sin día/hora reales ni mención al contexto del alumno) → señal de texto generado.
- Diagnóstico que usa vocabulario sofisticado ("hydration", "server actions", "design tokens") junto a un nivel "nuevo" contradictorio.
- Mapa al DoD perfecto y exhaustivo pero el plan ignora por completo la accesibilidad o los estados: la coherencia interna no calza.
- Verificación sugerida: pídele que explique, en una frase suya, **por qué** decidió hacer o saltar 4.9, o por qué a11y es gate y no extra.

## Feedback sugerido (graduado)

- **Pista (nivel 1):** "Revisa tu columna de niveles: ¿cuántos marcaste 'lo sé hacer'? Para cada uno, ¿tienes una evidencia concreta y reciente (no 'vi un tutorial')? Si no, probablemente sea 'lo reconozco'."
- **Pregunta socrática (nivel 2):** "Tu plan, ¿le da más tiempo a lo que marcaste 'nuevo'? Y en tu mapa, ¿dónde pusiste el gate de accesibilidad y estados? Si no aparece, ¿de verdad lo viste como parte del 'terminado'?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Para decidir 4.9, hazte dos preguntas: ¿el rol que busco pide componentes a escala / design tokens? ¿me desbloquea algo del capstone? Si ambas son 'no', sáltala y déjala anotada. Para el mapa, ancla primero el punto 5 (a11y+estados) en 4.4 y 4.10 —es el corazón de la fase— y luego completa el resto."

## Conexión con el proyecto / capstone

- Este ejercicio convierte el capstone `4.P` (frontend de una app de IA) en el
  **norte explícito** de la fase: el alumno entra sabiendo que accesibilidad y
  estados son **gate**, no adorno, y qué sub-unidad le aporta cada pieza del
  Definition of Done.
</content>
