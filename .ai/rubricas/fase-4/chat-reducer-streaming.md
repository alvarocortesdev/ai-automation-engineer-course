---
ejercicio_id: fase-4/chat-reducer-streaming
fase: fase-4
sub_unidad: "4.11"
version: 1
---

# Rúbrica — chatReducer: la máquina de estados de un chat de IA

> Rúbrica analítica atada a los `objetivos` del contrato. Los tests (Vitest) verifican el
> **comportamiento** del reducer (optimistic UI, acumulación, error/cancelar, inmutabilidad).
> Pero no garantizan que el alumno **entienda** por qué cada caso es como es. El corrector
> abre `chatReducer.ts`, revisa el patrón (inmutable, guards, parcial conservado) y lo sondea.

## Objetivos evaluados
- **O1** — Modelar el estado del chat como máquina de estados con un reducer puro e inmutable.
- **O2** — Optimistic UI: mensaje de usuario al instante + asistente vacío que crece chunk por chunk.
- **O3** — Transiciones de streaming + caminos de error y cancelación sin perder el parcial.

> Resultado esperado (el corrector lo sabe; NO se lo entrega): `switch` por `accion.tipo`;
> `ENVIAR` empuja 2 mensajes (user con texto + assistant `""`), estado `enviando`, `error: null`;
> `CHUNK` con guards (array vacío / último no-assistant) acumula inmutable (`.slice(0,-1)` + spread)
> y pasa a `streaming`; `COMPLETAR`/`CANCELAR` → `idle`; `ERROR` → `error` + `error: mensaje` sin
> tocar `mensajes`.

## Criterios y niveles

### C1 — ENVIAR / optimistic UI (corrección) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No añade el mensaje del usuario, o no crea el de asistente; el test de ENVIAR falla. |
| **en-progreso** | Añade el del usuario pero el de asistente no nace vacío (o nace con el texto del usuario), o no limpia `error`. |
| **competente** | Añade ambos mensajes (usuario con texto + asistente `texto: ""`), pasa a `"enviando"`, limpia `error`. El test pasa. |
| **excelente** | Explica por qué el asistente nace vacío (es el contenedor que `CHUNK` va a rellenar) y por qué es optimista (no espera al servidor). |

### C2 — CHUNK / acumulación inmutable (corrección + clean code) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No acumula, o **muta** el último mensaje en sitio (`ultimo.texto += ...`), o no tiene guards. |
| **en-progreso** | Acumula pero falta un guard (array vacío o último no-assistant), o reconstruye el array de forma frágil. |
| **competente** | Guards presentes; concatena al último mensaje de forma **inmutable** (`.slice(0,-1)` + objeto nuevo con spread); pasa a `"streaming"`. Tests de CHUNK e inmutabilidad pasan. |
| **excelente** | Articula por qué la inmutabilidad importa aquí (detección de cambios de React, lección 4.5) y por qué el guard de "último no-assistant" protege el invariante. |

### C3 — Error y cancelación (corrección) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `ERROR` borra el texto parcial o no guarda el mensaje; o `CANCELAR` no vuelve a `idle`. |
| **en-progreso** | Maneja uno de los dos bien pero el otro a medias (p. ej. `ERROR` borra `mensajes`). |
| **competente** | `ERROR` → `"error"` + `error: mensaje`, **sin** tocar `mensajes`; `CANCELAR` → `"idle"` conservando el parcial. Tests pasan. |
| **excelente** | Explica por qué conservar el parcial es mejor UX que borrarlo (no destruir lo que el usuario ya leía). |

### C4 — Calidad de ingeniería (testing + pureza) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Tests en rojo, o el reducer no es puro (efectos secundarios, depende de algo externo). |
| **en-progreso** | Todos los tests pasan pero no agregó el test propio, o el reducer tiene ramas muertas/duplicadas. |
| **competente** | Reducer puro; todos los tests pasan **y** agregó un test propio significativo. |
| **excelente** | El test propio cubre un caso real no trivial (p. ej. dos vueltas de conversación, o `CHUNK` tras `COMPLETAR`) y revela comprensión, no relleno. |

## Errores típicos a marcar
- Mutar el último mensaje en sitio (`ultimo.texto += delta`) en vez de copiar → rompe inmutabilidad (C2).
- El mensaje de asistente nace con el texto del usuario (copia el `texto` a ambos) → no es el contenedor vacío que streaming rellena (C1).
- `ERROR` que hace `mensajes: []` o borra el parcial → mala UX, contradice el objetivo (C3).
- Falta el guard de array vacío / último no-assistant en `CHUNK` → revienta o corrompe estado (C2).
- Olvidar `error: null` en `ENVIAR` → un error viejo queda pegado en la siguiente vuelta (C1).
- (transversal) tests verdes sin entender: persigue "que pase" en vez de razonar el optimismo y el parcial.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Reducer impecable con tipos sofisticados pero el alumno no sabe explicar por qué el asistente nace vacío ni qué pasa si `ERROR` borrara el parcial.
- Usa utilidades poco habituales para el nivel (Immer, librerías de máquinas de estado) sin poder defender la elección.
- **Verificación sugerida:** pídele que, en vivo, prediga el estado tras `ENVIAR → CHUNK("a") → ERROR → CHUNK("b")`; o que explique por qué el guard de "último no-assistant" existe. Si entiende, responde al instante; si copió, titubea.

## Feedback sugerido (graduado)
> Nunca pegar la solución de referencia ni el reducer completo.
- **Pista (nivel 1):** "En `ENVIAR`, ¿cuántos mensajes empujas y con qué texto cada uno? ¿El de asistente nace con algo dentro?"
- **Pregunta socrática (nivel 2):** "Cuando llega un `CHUNK`, ¿sobre cuál mensaje escribes? Si copiaras mal el array, ¿qué test se pondría en rojo? ¿Y si mutaras el objeto en sitio?"
- **Dirección concreta (nivel 3, solo tras intento real):** "En `CHUNK`: guard de array vacío, toma el último, guard de que sea del asistente, crea una copia con el texto concatenado, y devuelve el estado con `[...mensajes.slice(0,-1), copia]`. En `ERROR` no toques `mensajes`. No te doy el cuerpo exacto."

## Conexión con el proyecto / capstone
- Este reducer es **idéntico** en espíritu a lo que `useChat` mantiene en el [Capstone F4](/fase-4-frontend/proyecto/): el mensaje del usuario aparece al instante, la respuesta crece chunk por chunk, y un fallo de red no borra el parcial. Dominarlo aquí evita el bug clásico de los chats (la respuesta a medias que desaparece tras un error).
