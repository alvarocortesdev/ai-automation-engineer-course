---
ejercicio_id: track-0/logros-medibles-xyz
fase: track-0
sub_unidad: "T0.7"
version: 1
---

# Rúbrica — Reescribe 5 responsabilidades como logros medibles (fórmula XYZ)

> Rúbrica analítica para un ejercicio de **diseño/comunicación**. Lo que se evalúa es la **estructura**
> del logro (verbo de acción + impacto + número + decisión técnica) y la **honestidad** con los datos,
> no que las frases coincidan con un ejemplo. No hay una única redacción correcta: un bullet puede estar
> bien con números distintos si la estructura es sólida y los datos son defendibles (o marcados `[N]`).

## Objetivos evaluados
- **O1** — Transformar responsabilidad → logro medible (verbo + impacto + número).
- **O2** — Explicar el origen honesto de los números (capstones instrumentados), sin inventar.

## Criterios y niveles

### C1 — Verbo de acción y eliminación de la "silla" · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Mantiene "Responsable de" / "Encargado de" / "Trabajé con" en la mayoría; los bullets siguen describiendo deberes, no resultados. |
| **en-progreso** | Cambia algunos verbos pero deja 2+ bullets abriendo con responsabilidad pasiva, o usa verbos débiles ("Apoyé", "Colaboré"). |
| **competente** | Los 5 bullets abren con un verbo de acción fuerte (Construí, Reduje, Automaticé, Desplegué, Diseñé, Migré). |
| **excelente** | Verbos precisos y variados que calzan con la acción real; cada uno deja claro qué *hizo* el candidato, no qué cargo tuvo. |

### C2 — Impacto cuantificado (el número) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Bullets sin números, o con vaguedades ("mejoró mucho", "varios usuarios"). |
| **en-progreso** | Algunos bullets con número, otros sin; o números genéricos sin unidad clara. |
| **competente** | Los 5 bullets tienen al menos un número de impacto con unidad (%, latencia, /día, usuarios, USD/request, cobertura), real o marcado `[N]`. |
| **excelente** | Usa un antes→después o un % de mejora donde aporta; los números cuentan una historia de impacto, no solo una métrica suelta. |

### C3 — Decisión técnica que prueba criterio · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Ningún bullet nombra cómo se logró; solo el qué. |
| **en-progreso** | Menciona tecnologías sueltas ("usé Python/FastAPI") en vez de una decisión. |
| **competente** | Al menos 2 bullets nombran una decisión técnica concreta (caching semántico, reintentos backoff, validación de salida + HITL, reranking…). |
| **excelente** | La decisión técnica conecta con un hilo transversal del curso (evals, observabilidad, seguridad, manejo de fallas) y explica por qué importó. |

### C4 — Honestidad del dato (origen de los números) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica de dónde saldrían los números, o propone inventarlos sin marcarlos. |
| **en-progreso** | Menciona "de mis proyectos" pero sin concretar qué se mide ni dónde. |
| **competente** | Identifica los capstones instrumentados (T0.5) como fuente y nombra métricas concretas (p95, score de eval, usuarios, cobertura). |
| **excelente** | Distingue explícitamente "marcar `[N]` para practicar" de "mentir en el CV real", y nombra cómo verificaría cada número antes de ponerlo. |

### C5 — Comunicación / inglés (transversal) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **competente** | Bullets concisos y legibles (una línea, no un párrafo). |
| **excelente** | Bullets en **inglés** correcto y natural, listos para un CV de remoto-USD. |

## Errores típicos a marcar
- **Mantener la "silla":** abrir con "Responsable de" / "Encargado de" → describe el cargo, no el impacto.
- **Bullet sin número:** "mejoré el rendimiento" sin cuánto → no es falsable, no impresiona.
- **Número inventado sin marcar:** pone "94%" como si fuera real cuando no lo midió → en el CV real esto se cae en la entrevista; aquí debe ir como `[N]`.
- **Tecnología en vez de decisión:** "usé Python" no prueba criterio; "con reintentos backoff+jitter" sí.
- **Párrafo final ausente o vago:** no reconoce que los capstones instrumentados son la fuente honesta.
- (transversal) ignorar el inglés aunque el objetivo sea remoto-USD; ningún bullet cita un hilo transversal.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Cinco bullets perfectamente pulidos pero con números redondos y genéricos que no podrían venir de un proyecto real (texto plantilla).
- El alumno no puede explicar **qué mide** cada número que puso ni cómo lo obtendría.
- **Verificación sugerida:** pedir que tome uno de sus bullets y explique, sin notas, cómo mediría ese número en su propio capstone (qué herramienta, qué unidad). Si lo construyó, lo dice al instante; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca reescribir los bullets por el alumno.
- **Pista (nivel 1):** "Lee tu bullet #1 en voz alta. ¿Describe una **silla** que ocupaste o un **resultado** que dejaste? Si empieza con 'Responsable de', es una silla."
- **Pregunta socrática (nivel 2):** "De este proyecto, ¿qué número podrías defender si te lo preguntan en la entrevista? ¿Cuántos por día? ¿Cuánto más rápido que antes? Ese número es el corazón del bullet."
- **Dirección concreta (nivel 3, solo tras intento real):** "Aplica la fórmula entera: empieza con un verbo de acción, mete el número al medio, cierra con la decisión técnica. Y si no mediste nada, ese es el hueco que T0.5 te pide tapar: tu capstone debe estar instrumentado."

## Conexión con el proyecto / capstone
- Estos logros son el cuerpo de tu CV (T0.7) y los "Resultados" de tus historias STAR de [T0.3]. El número que escribes aquí solo existe si tu capstone de [T0.5] estuvo instrumentado. El capstone del track es conseguir el trabajo; un logro medible es lo que hace que un reclutador agende la llamada.
