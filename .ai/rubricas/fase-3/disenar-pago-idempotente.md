---
ejercicio_id: fase-3/disenar-pago-idempotente
fase: fase-3
sub_unidad: "3.14"
version: 1
---

# Rúbrica — Diseña un endpoint POST idempotente

> Rúbrica **analítica** atada a los `objetivos`. Ejercicio de **diseño**: no hay tests.
> Evalúa `diseno.md` + `esquema.sql` contra los escenarios. Lo que se mide es el **razonamiento**:
> que el diseño resista la carrera concurrente y que cada decisión esté justificada.

## Objetivos evaluados
- **O1** — Esquema con un constraint que arbitra la carrera + alcance + representación de "en vuelo".
- **O2** — Flujo INSERT-primero para los tres escenarios (primer request, reintento terminado, concurrencia).
- **O3** — Status HTTP por caso (incluido 409 en-vuelo) + trade-off fail-open vs fail-closed.

## Criterios y niveles

### C1 — Solidez del esquema · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `esquema.sql` sin constraint único sobre la clave, o sin forma de guardar la respuesta. |
| **en-progreso** | Tiene la clave como `UNIQUE`/PK pero le falta el alcance (usuario/endpoint) o el timestamp para TTL. |
| **competente** | Clave como PK o `UNIQUE` (el árbitro), campo `respuesta` (nullable = en vuelo), `usuario_id`, `creado_en` para TTL. |
| **excelente** | Razona el alcance (`UNIQUE(clave, usuario_id)` para que dos usuarios puedan reusar una misma clave sin colisión), y/o guarda un hash del body para detectar reuso con payload distinto. |

### C2 — Flujo bajo concurrencia · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Diseño "leer y luego escribir" (SELECT, si no está, INSERT): tiene la ventana de carrera abierta. |
| **en-progreso** | Usa INSERT-primero pero no explica qué le pasa al request que pierde la carrera. |
| **competente** | INSERT-primero; el `UNIQUE` hace que el segundo `INSERT` falle; lee la fila y decide según `respuesta` (llena → resultado; NULL → 409). |
| **excelente** | Menciona que el claim va en una transacción y que el `UPDATE` de la respuesta ocurre en la misma; conecta con el locking de `3.3` y nombra la carrera como idéntica a la del stock. |

### C3 — Status HTTP y trade-off · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Devuelve 200 para todo, o no aborda el caso "en vuelo". |
| **en-progreso** | Acierta el caso feliz y el reintento, pero no el 409 del "en vuelo" ni el caso "mismo key, body distinto". |
| **competente** | 201/200 primer cobro; 200 reintento terminado (mismo resultado); **409** en vuelo; identifica el conflicto de "misma clave, body distinto" (422/409). Justifica el pago como **fail-closed**. |
| **excelente** | Defiende fail-closed con el argumento del cargo fantasma; contrasta con un endpoint no crítico (fail-open con fallback); menciona el TTL y la idempotency key como input no confiable (validar formato). |

## Errores típicos a marcar
- **Diseño "SELECT y luego INSERT":** la ventana entre ambos es la carrera; dos requests ven "no existe" y ambos cobran. El INSERT-primero (apoyado en el `UNIQUE`) la cierra.
- **No distinguir "en vuelo" de "terminada":** sin un `respuesta` nullable, no se sabe si devolver el resultado o un 409.
- **Clave generada por el servidor:** sería distinta por request; anula la idempotencia.
- **Sin TTL:** la tabla crece sin límite; falta la columna de tiempo y la política de expiración.
- **Ignorar "misma clave, body distinto":** un cliente que reusa una clave con otro monto debería recibir un error (no el resultado viejo silenciosamente, ni un cobro nuevo).
- **Fail-open en un pago:** degradar un cobro a "éxito asumido" crea inconsistencias de plata; el pago es fail-closed.
- (transversal seguridad) tratar la `Idempotency-Key` como dato confiable sin validar su formato/longitud.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Documento extenso y pulido que describe el patrón de Stripe al pie de la letra pero no responde la pregunta de la **carrera concurrente** con su propio razonamiento.
- Usa términos avanzados (outbox, saga) sin conectarlos al diseño concreto pedido.
- **Verificación sugerida:** pídele que dibuje la línea de tiempo de dos requests concurrentes y señale la línea EXACTA donde el `UNIQUE` arbitra. Y que diga qué status devuelve al request que pierde (409) y por qué no 500. Si no puede, copió el patrón sin entender la carrera.

## Feedback sugerido (graduado)
> Es diseño: el feedback empuja el razonamiento, no entrega el esquema.
- **Pista (nivel 1):** "Tu flujo hace SELECT y después INSERT. Dibuja dos requests que ejecuten el SELECT antes de que cualquiera haga el INSERT: ¿qué ven ambos?"
- **Pregunta socrática (nivel 2):** "Si en vez de comprobar primero, INSERTAS primero, ¿qué pasa con el segundo INSERT que usa la misma clave? ¿Qué te dice esa violación de unicidad sobre quién llegó antes?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Reclama con `INSERT` (clave PK/UNIQUE). Si falla por unicidad, `SELECT respuesta`: llena → devuélvela (200); NULL → 409 'procesando'. Cobra y `UPDATE respuesta` en la misma transacción. Repasa 4.2–4.3."

## Conexión con el proyecto / capstone
- Es el ADR de idempotencia del capstone: dónde vive el almacén (Postgres o Redis de `3.15`), qué TTL, qué alcance, qué status por caso. Y es la semilla directa del outbox y la reconciliación de la Fase 7, donde la entrega at-least-once vuelve la idempotencia un requisito, no un lujo.
