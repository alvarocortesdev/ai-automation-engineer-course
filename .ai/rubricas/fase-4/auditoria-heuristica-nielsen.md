---
ejercicio_id: fase-4/auditoria-heuristica-nielsen
fase: fase-4
sub_unidad: "4.10"
version: 1
---

# Rúbrica — Auditoría de usabilidad con las heurísticas de Nielsen

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **a mano** (razonamiento/diseño): no
> hay test ni una única respuesta correcta. Lo que se evalúa es si el alumno **nombra la heurística correcta**,
> conecta los estados faltantes, y prioriza por impacto. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Nombrar la heurística de Nielsen concreta de cada problema (número + nombre), no un juicio de gusto.
- **O2** — Detectar al menos un estado faltante (empty/loading/error) y atarlo a su heurística.
- **O3** — Priorizar por impacto.

## Criterios y niveles

### C1 — Diagnóstico con vocabulario (heurística correcta) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Menos de cuatro problemas, o "se ve feo / poco moderno" sin nombrar heurística. |
| **en-progreso** | Encuentra problemas reales pero les asigna la heurística equivocada, o dice "usabilidad" en genérico sin número/nombre. |
| **competente** | ≥6 problemas, cada uno con la heurística correcta (número + nombre) y una razón clara. |
| **excelente** | Además distingue casos donde **dos** heurísticas se solapan y explica cuál es la dominante (p. ej. el número de estado es H2 *y* H4). |

### C2 — Estados como ciudadanos de primera (cruce con la lección) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona ningún estado faltante (loading/error/empty). |
| **en-progreso** | Menciona "falta feedback" pero sin atarlo a la heurística ni distinguir qué estado falta. |
| **competente** | Identifica al menos uno (típico: no hay loading al subir → H1; error inútil → H9; tabla vacía sin empty → H1/H8) y lo nombra. |
| **excelente** | Detecta los tres (loading, error, empty) y nota que el empty de la tabla es una oportunidad de onboarding desperdiciada. |

### C3 — Prevención vs. corrección (H5) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No distingue prevenir de avisar; trata todo como "mejorar el mensaje". |
| **en-progreso** | Propone mejorar el mensaje del error de tamaño, pero no propone **mostrar el límite antes** de subir. |
| **competente** | Identifica al menos un caso de H5: mostrar el límite/formato por adelantado; confirmar o permitir deshacer "PURGE ALL". |
| **excelente** | Propone **deshacer** (con ventana de gracia) por encima de un "¿estás seguro?", y argumenta por qué es mejor UX. |

### C4 — Priorización por impacto · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay top-3, o está por orden de aparición. |
| **en-progreso** | Hay top-3 pero la justificación es vaga ("es importante"). |
| **competente** | Top-3 justificado por impacto: lo que **bloquea o causa pérdida de datos** va antes que lo cosmético. |
| **excelente** | Pondera explícitamente dos ejes (¿bloquea/destruye? vs. ¿confunde/molesta?) y ubica "PURGE ALL sin deshacer" como #1 por pérdida de datos irreversible. |

## Errores típicos a marcar
- **"Se ve feo / anticuado"** sin nombrar heurística: el ejercicio entero existe para evitar esto.
- **Heurística mal asignada:** confundir H5 (prevention) con H9 (recovery) — prevenir es evitar que ocurra;
  recuperar es ayudar cuando ya ocurrió. El error de tamaño tiene ambas: prevenir = mostrar el límite;
  recuperar = mensaje útil cuando igual pasó.
- **Olvidar el empty de la tabla vacía:** lo más fácil de pasar por alto, justo el tema de la lección.
- **No notar la pérdida de datos** de "PURGE ALL" o no priorizarla como lo más grave.
- **Top-3 por orden de aparición** en vez de por impacto.
- (transversal seguridad) no notar que `ERR_PAYLOAD_413` filtra jerga interna al usuario (también roza
  exponer detalles del backend); un excelente lo menciona.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Lista pulida que cita las 10 heurísticas en orden perfecto pero sin conectarlas a los detalles concretos
  de **esta** pantalla (textos genéricos): pídele que señale, en la descripción, la frase exacta que
  evidencia cada problema.
- Asigna heurísticas con nombres impecables pero no sabe explicar la diferencia H5 vs H9: pídele que diga,
  para el error de tamaño, qué sería "prevenir" y qué sería "recuperar".
- Top-3 idéntico a una respuesta "de manual" sin razonar el caso de pérdida de datos: pídele que ordene por
  "qué le dolería más a un usuario real" y defienda el #1.

## Feedback sugerido (graduado)
> De menos a más directo. Nunca redactar la auditoría completa por el alumno.

- **Pista (nivel 1):** "Recorre las 10 heurísticas una por una sobre esta pantalla, en vez de mirarla 'en
  general'. ¿Qué pasa mientras sube un archivo? ¿Eso qué heurística toca?"
- **Pregunta socrática (nivel 2):** "El error de tamaño aparece **después** de intentar subir. ¿Podrías
  haber evitado que el usuario llegara a ese error? ¿Qué heurística habla de *evitar* el error en vez de
  *avisarlo*? ¿Y cuál habla de cómo ayudar a recuperarse una vez que ocurrió?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Te faltó el estado de la tabla vacía: cuando el
  usuario no ha subido nada, ve solo encabezados de columna. Eso viola H1 (no comunica) y desperdicia un
  empty de onboarding. Y 'PURGE ALL' borra sin deshacer: H3 (control y libertad) — debería ir primero en tu
  top-3 por pérdida de datos. No te doy la lista completa: completa las heurísticas que te faltan."

## Conexión con el proyecto / capstone
- Esta auditoría es el ensayo de la que harás sobre **tu propia** UI del Capstone F4 antes de entregar. El
  vocabulario de Nielsen es lo que convierte "creo que está bien" en un checklist defendible, y los estados
  faltantes que detectes aquí son justo el gate de "estados completos" del Definition of Done.
