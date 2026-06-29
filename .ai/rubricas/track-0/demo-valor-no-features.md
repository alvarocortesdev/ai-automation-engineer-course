---
ejercicio_id: track-0/demo-valor-no-features
fase: track-0
sub_unidad: "T0.8"
version: 1
---

# Rúbrica — Demo de valor para no-ingenieros + manejo de expectativas

> Rúbrica analítica para un ejercicio de **diseño/razonamiento**. Lo que se evalúa es el **criterio de
> traducción**: hablar en outcomes (no features), ser honesto sobre los límites de la IA, y manejar un
> scope creep sin sobre-prometer. No hay un único guion correcto, pero sí criterios correctos: un alumno
> puede redactar distinto y estar bien; puede impresionar con jerga o prometer de más y estar mal.

## Objetivos evaluados
- **O1** — Traducir una feature técnica a una demo de valor para no-ingenieros (outcome, no jerga).
- **O2** — Manejar expectativas honestamente (qué hace / qué NO hace) y responder a un scope creep.

## Criterios y niveles

### C1 — Demo de valor (cero jerga, outcome) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | El guion repite la jerga del insumo (RAG, embeddings, pgvector, reranking, p95). |
| **en-progreso** | Mezcla: algo de valor pero con términos técnicos sueltos que la stakeholder no entendería. |
| **competente** | Cero jerga; explica la feature como **valor/outcome** con un **antes / después** concreto (15-20 min de búsqueda → segundos). |
| **excelente** | Usa un **caso real del cliente** (no genérico), conecta con lo que la stakeholder mide (tiempo de respuesta, errores por info desactualizada), y aún menciona la cita a la fuente como "para que confíes en la respuesta". |

### C2 — Honestidad de expectativas (qué hace / qué NO) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla, o solo lista "lo bueno" (vende perfección). |
| **en-progreso** | Tabla presente pero los "no hace" son triviales o evita el límite real de la IA (alucinación, % de revisión humana). |
| **competente** | ≥3 "hace" y ≥3 "no hace" honestos, incluido que **puede equivocarse** y que ~13% conviene revisión humana. |
| **excelente** | Traduce el límite a lenguaje de negocio sin esconderlo ("en ~1 de cada 8 casos te dirá 'no estoy seguro' y conviene que un humano mire": eso es *bueno*, no malo) y cita un número (precisión/faithfulness, % HITL). |

### C3 — Manejo del scope creep · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | "Sí, claro" reflejo (mete la feature nueva al plazo) o "no" seco que cierra la relación. |
| **en-progreso** | Reconoce que es nuevo pero no acota ni registra (queda ambiguo si entra o no). |
| **competente** | **Reconocer + acotar + registrar**: valida la idea, la manda a fase 2, y deja constancia por escrito. |
| **excelente** | Protege el MVP explícitamente (entregar lo prometido primero), propone estimar la fase 2 después, y el registro es accionable (dónde queda anotado y quién decide). |

### C4 — Comprensión del principio (sub-prometer) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **competente** | La línea de cierre explica que sub-prometer y sobre-entregar construye confianza. |
| **excelente** | Liga sobre-prometer en IA (precisión perfecta) al daño concreto: el primer fallo destruye la confianza, y la confianza es lo que sostiene al cliente que paga bien. |

## Errores típicos a marcar
- **Demo con jerga:** dejar "RAG", "embeddings", "p95", "reranking" en el guion → la stakeholder se pierde y la confianza baja.
- **Vender perfección:** omitir que la IA puede equivocarse → la primera alucinación en producción quema la relación.
- **Sí reflejo al scope creep:** aceptar la feature nueva dentro del plazo del MVP → revienta la entrega.
- **No registrar:** manejar el scope creep solo de palabra, sin dejar constancia → "pero yo pedí eso" después.
- **Features en vez de outcome:** listar lo que el sistema *tiene* en vez de lo que *cambia* para el usuario.
- (transversal) ignorar que el costo/latencia y la precisión son argumentos de negocio (segundos vs. 20 min; "no inventa") y no detalles técnicos a esconder.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Guion pulido pero que conserva 1-2 términos técnicos que el alumno no podría explicar en palabras simples si se le pide.
- Tabla "qué NO hace" genérica que no menciona el límite real del insumo (el ~13% de grounding débil).
- **Verificación sugerida:** pedir que explique, sin notas y en una frase, "qué gana Marta con esto" y "qué pasa cuando el sistema no está seguro". Si tradujo de verdad, le sale natural; si lo generó, vuelve a la jerga.

## Feedback sugerido (graduado)
> Nunca reescribir el guion por el alumno.
- **Pista (nivel 1):** "Subraya cada palabra de tu guion que Marta tendría que googlear. Si hay aunque sea una, esa frase todavía no es una demo de valor."
- **Pregunta socrática (nivel 2):** "¿Qué mide Marta en su equipo? ¿Tu guion habla de eso (tiempo, errores) o habla de cómo está construido el sistema? Cuando dices 'sí, de paso lo hago', ¿qué le pasa al plazo de lo que ya prometiste?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Reescribe el guion empezando por el antes/después que Marta vive (busca 20 min hoy → segundos), sin un solo término técnico. En la tabla, di de frente que la IA puede no estar segura y que por eso hay revisión humana —eso suma confianza. Para el scope creep: reconoce, manda a fase 2, registra."

## Conexión con el proyecto / capstone
- Es el músculo que convierte la demo de cualquier capstone de [T0.5] en algo que un no-ingeniero entiende y valora; y la honestidad de expectativas es la base de la historia de falla en producción de [T0.4] (manejar bien lo que la IA puede y no puede). En remoto-USD, esta demo se hace en inglés ([T0.1]).
