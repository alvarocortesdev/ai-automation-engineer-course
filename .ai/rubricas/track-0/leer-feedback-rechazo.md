---
ejercicio_id: track-0/leer-feedback-rechazo
fase: track-0
sub_unidad: "T0.2"
version: 1
---

# Rúbrica — Lee el feedback: señal vs ruido

> Rúbrica **analítica** para un ejercicio de **diagnóstico**. Lo que se evalúa es el **criterio de
> clasificación**: si el alumno separa la señal accionable del ruido, ubica cada señal en la etapa
> correcta del funnel, y propone un ajuste concreto —sin leer el rechazo como un veredicto sobre su
> valor. Hay dos casos trampa (C1 silencio = señal; C4 vacante cerrada y C6 gap imposible = ruido) que
> revelan si entendió el modelo o si está clasificando por "se siente mal = señal".

## Objetivos evaluados
- **O3a** — Clasificar el desenlace como señal accionable o ruido.
- **O3b** — Para cada señal, nombrar el gap concreto y la etapa del funnel.
- **O3c** — Proponer un ajuste concreto, sin confundir señal con veredicto.

> Clasificación de referencia (el corrector la conoce; **no** se la entrega como atajo, la usa para
> medir): **C1 señal** (gap arriba del funnel: CV/keywords/posicionamiento) · **C2 señal** (skill puntual:
> embeddings/RAG, etapa técnica) · **C3 señal débil / casi-ruido** (estuviste cerca; ajuste = subir
> experiencia demostrable / portafolio, o seguir igual) · **C4 ruido** (vacante cerrada, no depende de
> ti) · **C5 señal** (inglés, etapa screening) · **C6 ruido / señal de mira** (gap de años imposible:
> el ajuste es ajustar la mira, no estudiar).

## Criterios y niveles

### C1 — Clasificación señal vs ruido, incluidos los casos trampa · mapea: O3a
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No clasifica, o clasifica todo como señal (todo rechazo = "algo que mejorar") o todo como ruido. |
| **en-progreso** | Acierta los casos obvios pero falla los trampa: lee C1 (silencio) como ruido, o C4/C6 como señal a la que inventa un gap. |
| **competente** | Clasifica bien los 6, incluidos C1 como señal fuerte y C4 como ruido; C6 como ruido o señal-de-mira. |
| **excelente** | Además explica *por qué* el silencio masivo es la señal más accionable (parte de arriba del funnel) y por qué inventarle un gap a C4/C6 lleva a ajustar por la razón equivocada. |

### C2 — Gap + etapa del funnel por cada señal · mapea: O3b
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No nombra gaps ni etapas, o son genéricos ("estudiar más"). |
| **en-progreso** | Nombra el gap pero no la etapa, o confunde la etapa (p. ej. atribuye C1 a un fallo técnico cuando no hubo evaluación técnica). |
| **competente** | Cada señal con su gap específico y la etapa correcta del funnel (C1 screening, C2 técnica, C5 screening). |
| **excelente** | Conecta la etapa con qué evalúa: "me caí antes de la técnica, luego el problema no es mi código sino lo que viene antes". |

### C3 — Ajuste concreto y accionable · mapea: O3c
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin ajuste, o ajustes genéricos no accionables. |
| **en-progreso** | Ajustes plausibles pero desconectados de la etapa/gap (p. ej. "practicar algoritmos" para un fallo de screening). |
| **competente** | Cada señal con un ajuste concreto y coherente (C1 → reescribir CV/keywords; C2 → adelantar/repasar la fase de IA; C5 → practicar screening en inglés). |
| **excelente** | Para C4/C6 (ruido) propone explícitamente **no** ajustar el estudio (o solo la mira), evitando el reflejo de "estudiar más" ante todo rechazo. |

### C4 — Señal vs veredicto (metacognición) · mapea: O3c
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay reflexión, o el tono revela que tomó los rechazos como un juicio sobre su valor. |
| **en-progreso** | Reflexión superficial ("no hay que rendirse") sin distinguir candidatura de persona. |
| **competente** | Distingue con claridad "señal sobre mi candidatura/CV/skill" de "veredicto sobre mi valor". |
| **excelente** | Convierte la distinción en una regla reutilizable ("antes de sentirme mal por un rechazo, pregunto en qué etapa fue y qué evalúa esa etapa"). |

## Errores típicos a marcar
- **Silencio = ruido** (clasificar mal C1): el silencio masivo en screening es la señal más accionable, no "el mercado está malo".
- **Inventarle un gap al ruido** (C4/C6): si la vacante se cerró o el gap de años es imposible, no hay nada que estudiar; el ajuste es la mira, no el plan.
- **Etapa equivocada:** atribuir a "fallo técnico" algo que ocurrió en el screening (antes de cualquier evaluación de código).
- **Ajuste genérico:** "estudiar más" en vez de un ajuste mapeado a la etapa y el gap concretos.
- **Tono de veredicto:** leer el rechazo como "no sirvo" en vez de como dato sobre una parte específica de la candidatura.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Clasificación perfecta de los 6 pero sin justificación de *por qué* C1 es señal y C4 ruido (resultado sin razonamiento).
- Ajustes sofisticados que no calzan con la etapa nombrada (texto generado, criterio ausente).
- **Verificación sugerida:** presenta un séptimo caso nuevo ("pasaste la técnica pero en la final te dijeron que el fit cultural no cuadró") y pide que lo clasifique y ubique en el funnel sin notas. Si entendió el modelo, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
- **Pista (nivel 1):** "Mira C1 y C4 otra vez: ¿cuál de los dos depende de algo que tú puedes cambiar? Esa es la frontera entre señal y ruido."
- **Pregunta socrática (nivel 2):** "En C1, ¿llegaron a evaluar tu código? Si no, ¿el problema puede ser técnico? ¿En qué etapa estás fallando y qué evalúa esa etapa?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Estás tratando todo rechazo como algo que se arregla estudiando. C4 (vacante cerrada) y C6 (gap de 8 años) no se arreglan con estudio: uno es ruido puro, el otro pide ajustar la mira. Reclasifícalos y deja su 'ajuste' en consecuencia."

## Conexión con el proyecto / capstone
- Leer el funnel es lo que hace que el pipeline vivo (ejercicio hermano) sirva: sin separar señal de ruido, ajustas tu plan por las razones equivocadas. Alimenta directamente las decisiones de T0.5 (portafolio), T0.7 (CV) y T0.3 (qué practicar en los mocks).
