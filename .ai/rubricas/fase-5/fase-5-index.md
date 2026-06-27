---
ejercicio_id: fase-5/fase-5-index
fase: fase-5
sub_unidad: "5.0"
version: 1
---

# Rúbrica — Diagnóstico de Fase 5 y plan de ruta a producción

> Rúbrica analítica para un ejercicio **a-mano** de placement/metacognición de
> entrada a la fase de DevOps. No hay "respuesta correcta": se evalúa la
> **honestidad** del autodiagnóstico, la **concreción y coherencia** del plan (con
> su orden de apilado) y si la definición de listo es **verificable**. Un plan
> precioso pero irreal, o evidencias que nadie puede abrir, valen menos que algo
> modesto y comprobable. El corrector premia realismo y verificabilidad, no
> ambición.

## Objetivos evaluados
- **O1** — Autoevaluar el punto de partida en DevOps por sub-unidad de ruta-crítica, distinguiendo "lo sé hacer" de "lo reconozco".
- **O2** — Diseñar un plan con bloques semanales concretos, ritual de repaso y un orden de apilado del pipeline que termina en usuarios reales + observabilidad.
- **O3** — Traducir los 7 puntos del DoD del Capstone F5 en evidencias verificables.

## Criterios y niveles

### C1 — Honestidad y cobertura del diagnóstico · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta la tabla, o cubre menos de las 8 sub-unidades de ruta-crítica, o no asigna niveles. |
| **en-progreso** | Cubre las 8 pero el nivel no es defendible (todo en "lo sé hacer" sin evidencia, o todo "nuevo" pese a experiencia declarada), o falta la razón por fila. |
| **competente** | Las 8 con nivel **y** razón coherente; aplica la prueba "¿podría resolverlo sin notas ahora?" de forma consistente. |
| **excelente** | Además matiza (p. ej. "usé Compose pero nunca un multi-stage / nunca un gate de seguridad") y usa el diagnóstico para priorizar el tiempo del plan. |

### C2 — Concreción, realismo y orden de apilado del plan · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay plan, o son intenciones ("estudiaré DevOps") sin días/horas, o sin orden de apilado. |
| **en-progreso** | Hay bloques pero irreales, o falta el ritual de repaso, o el orden de apilado contradice el flujo (p. ej. automatizar deploy antes de empaquetar). |
| **competente** | Bloques concretos (día/hora/duración) plausibles + ritual de repaso explícito + orden de apilado coherente (contenedor → config → CI/tests → gates → deploy → observabilidad) que termina en ≥3 usuarios reales. |
| **excelente** | Ata el repaso al *spacing* (al día siguiente + a los pocos días), ajusta carga según el diagnóstico, y nombra **quiénes** serán los usuarios reales y cómo los conseguirá. |

### C3 — Verificabilidad de la definición de listo · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No traduce el DoD, o lista menos de los 7 puntos, o los copia sin evidencia. |
| **en-progreso** | Cubre los 7 puntos pero las "evidencias" son intenciones ("tendré tests", "habrá observabilidad") sin nada abrible. |
| **competente** | Cada uno de los 7 puntos tiene una evidencia **verificable** y específica (link al run de Actions, captura de una traza con su correlation ID, nombre de los usuarios reales, etc.). |
| **excelente** | Distingue evidencia de *proceso* vs de *resultado*, y conecta la observabilidad/costo con su uso en F6 (traza del LLM, USD/request) por iniciativa. |

## Errores típicos a marcar
- **Sobreconfianza** (Dunning-Kruger): "lo sé hacer sin notas" en temas que solo "usó" (clásico: confundir `docker compose up` con saber escribir un Dockerfile multi-stage, o haber usado Compose pero nunca un secret-scanning gate). Pedir la prueba: "¿lo resolverías ahora sin notas?".
- **Orden de apilado incoherente:** automatizar el deploy (5.3/5.9) de algo que aún no se empaquetó (5.1) ni se hizo configurable (5.2).
- **Plan de fantasía:** bloques irreales sin día/hora; ausencia de ritual de repaso (*spacing*).
- **DoD decorativo:** copiar los 7 puntos sin una evidencia abrible; "tendré observabilidad" en vez de "esta traza con este correlation ID".
- **Olvidar los usuarios reales:** el plan no nombra cómo conseguir ≥3, que es justo lo que distingue el capstone F5.
- (transversales) confundir logs/métricas/trazas como si fueran lo mismo; tratar la seguridad como "fase posterior" en vez de gate; ignorar el costo hasta la factura.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Plan o DoD con redacción genérica de "buenas prácticas DevOps" que no menciona **su** app concreta (la de F3/F4) ni ninguna sub-unidad específica: suena a plantilla de IA.
- Diagnóstico uniforme (todo el mismo nivel) sin razones específicas por fila.
- **Verificación sugerida:** pedir que justifique en voz alta por qué 5.4 (gates de seguridad) quedó en el nivel que eligió y que describa qué evidencia mostraría para el punto 3 del DoD. Si se autoevaluó de verdad, lo hace; si la IA lo escribió, se traba.

## Feedback sugerido (graduado)
> Nunca "darle el plan". Empujar a que el suyo sea honesto, coherente y verificable.
- **Pista (nivel 1):** "Mira la fila que marcaste 'lo sé hacer sin notas'. ¿Podrías resolver un ejercicio de ese tema ahora, sin abrir nada? Y en tu orden de apilado, ¿qué necesitas tener listo **antes** de automatizar el deploy?"
- **Pregunta socrática (nivel 2):** "Tu definición de listo dice que 'tendrás observabilidad'. Si yo fuera tu revisor, ¿qué exactamente me mostrarías en pantalla para creerte? ¿Y en qué día/hora ocurre tu primer bloque de estudio esta semana?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Convierte cada punto del DoD en una evidencia que yo pueda abrir (un link, una captura, un nombre). Reordena el apilado para que cada capa dependa solo de las anteriores. Recorta el plan hasta que quepa de verdad en tu semana: sostenible le gana a ambicioso."

## Conexión con el proyecto / capstone
- Este diagnóstico **es** el plan de vuelo del **Capstone F5 — Pipeline a producción**: el orden de apilado que defines aquí es el orden en que lo construirás, y la definición de listo es, literalmente, la checklist con la que sabrás que el capstone está terminado. Además entrena el músculo de observabilidad/costo que reaparece en F6.
