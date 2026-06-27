---
ejercicio_id: fase-4/capstone-frontend-ia
fase: fase-4
sub_unidad: "4.P"
version: 1
---

# Rúbrica — Capstone Fase 4: Frontend de una app de IA

> Rúbrica analítica para el **capstone integrador** de la Fase 4. No hay una única respuesta correcta: el
> alumno elige su layout y su diseño. Lo que se evalúa es si el frontend cumple el estándar de **producción
> usable y accesible** (no si "se ve bien" en su pantalla): frontera de estado correcta, server-state en
> TanStack Query, chat con streaming, y —el gate de la fase— **accesibilidad WCAG 2.2 y los cuatro estados de
> primera clase**. Una UI que "se ve linda" pero no se puede usar con el teclado, guarda datos del servidor en
> Zustand o renderiza la salida del LLM como HTML **no** cumple el objetivo.
>
> Se mide contra el **Definition of Done único** (§B de `CURRICULUM-REVIEW.md`). En la Fase 4 aplican los
> puntos **1** (spec + ADR), **2** (tests/lint en CI), **3** (seguridad del frontend), **4** (observabilidad:
> latencia/tokens), **7** (a11y WCAG 2.2 + estados completos — **el gate**), **8** (demo + README inglés +
> write-up) y **9** (Conventional Commits). Los puntos **5** (eval IA) y **6** (agente) se *siembran* aquí y se
> *exigen* en F6 — no los penalices si faltan.

## Objetivos evaluados
> De `objetivos` en `ejercicio.yml`.

- **O1** — Frontend Next.js + TS de producción sobre una API REST: App Router, Server/Client Components,
  server-state en TanStack Query, formularios con RHF + zod, Zustand solo para client-state.
- **O2** — UI de chat de IA con streaming token por token (optimistic UI, estados, cancelar) y seguridad de
  renderizar salida de un LLM.
- **O3** — Pasar el gate de calidad: a11y WCAG 2.2 + cuatro estados de primera clase, demo que corre, README
  en inglés y write-up de trade-offs.

## Criterios y niveles

### C1 — Spec-first + ADR + frontera de estado · mapea: O1 · DoD 1 · hilo: spec-driven
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `SPEC.md`, o se escribió **después** del código, o no enumera estados; no hay ADR. La frontera de estado no se decidió (server-state mezclado con client-state ad hoc). |
| **en-progreso** | Hay spec pero sin inventario de estados; el ADR no justifica nada real ("usé TanStack Query porque sí"); la frontera existe en la cabeza pero el código la contradice (datos del servidor en Zustand en algún punto). |
| **competente** | `SPEC.md` con pantallas, rutas, **inventario de estados** de cada vista y la tabla de frontera (server/chat/client), commiteada **antes** del primer componente; ADR con contexto/decisión/alternativas/consecuencias. |
| **excelente** | El ADR anticipa la migración de la IA al backend en F6 (la UI no cambia) y nombra el costo aceptado; cada estado de la spec es trazable a un componente y a un test. |

### C2 — Server-state, formularios y corrección React/Next · mapea: O1 · DoD 2 · hilo: testing
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Server-state a mano (`useEffect` + `useState`) o en Zustand; formularios validados a mano en el submit; todo en Client Components sin razón; mutaciones sin invalidar la caché. |
| **en-progreso** | Usa `useQuery` pero sin invalidar tras mutar (lista obsoleta); RHF presente pero el schema de zod no es la fuente de validación; frontera Server/Client confusa. |
| **competente** | `useQuery`/`useMutation` con **invalidación** tras mutar; **RHF + zod** con el schema como validación; separación Server/Client coherente (interactivo = `"use client"`); sin server-state en Zustand. |
| **excelente** | Maneja estados de mutación (pending/optimistic donde aplica), keys de query bien diseñadas; Server Components usados donde de verdad ayudan; tipado estricto sin `any`. |

### C3 — Chat de IA con streaming · mapea: O2 · DoD 8
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El chat espera la respuesta completa (`await res.json()`), sin streaming; sin optimistic UI; sin poder cancelar. |
| **en-progreso** | Hay streaming pero sin optimistic UI (el mensaje del usuario no aparece al instante), o sin estado para cancelar, o el parcial se pierde al terminar/errar. |
| **competente** | `useChat` (`@ai-sdk/react`) + Route Handler con `streamText`; optimistic UI; el mensaje de asistente crece chunk por chunk; estados pensando/streaming/error/cancelar funcionan. |
| **excelente** | Renderiza solo los `parts` que conoce; conserva el parcial en error/cancelar; el Route Handler está limpio y el modelo es intercambiable en una línea; la latencia percibida se siente profesional en la demo. |

### C4 — Seguridad del frontend · mapea: O2 · DoD 3 · hilo: seguridad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Renderiza la salida del LLM con `dangerouslySetInnerHTML` (XSS); API key del modelo expuesta en el cliente (`NEXT_PUBLIC_`); CORS `*`. |
| **en-progreso** | Salida como texto pero el markdown se renderiza con un parser que permite HTML crudo; secretos en env pero el token en `localStorage` sin nombrar el trade-off. |
| **competente** | Salida del LLM como **texto** (o markdown sanitizado sin HTML); API key **server-only**; CORS acotado en el backend; secretos en `.env.local` (gitignored). |
| **excelente** | Test que prueba que un `<script>` del modelo aparece escapado; decisión consciente del almacenamiento del token (cookie `HttpOnly` vs `localStorage`) argumentada en el write-up. |

### C5 — Accesibilidad + estados de primera clase (EL GATE) · mapea: O3 · DoD 7
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No navegable con teclado; foco no manejado (se pierde al abrir el modal); contraste insuficiente; solo el happy path (sin empty/loading/error). |
| **en-progreso** | Teclado parcial (algún control no alcanzable); `aria-live` ausente en el chat; dos de los cuatro estados dibujados; contraste a medias. |
| **competente** | Toda la app operable con teclado, foco visible y manejado en el modal; contraste WCAG 2.2; `aria-live` en el chat; **los cuatro estados** (empty/loading/error/success) en cada vista con datos + los seis del chat. |
| **excelente** | Chequeo axe en CI **más** evidencia de la pasada manual de teclado; landmarks/headings correctos; el estado de error lee el `detail` del RFC 9457 del backend; loading con skeleton (no spinner mudo). |

### C6 — Calidad de tests y observabilidad · mapea: O3 · DoD 2 y 4 · hilos: testing, observabilidad
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin tests, o "se ve bien en mi pantalla"; sin lint en CI; no registra nada del chat. |
| **en-progreso** | Algún test pero solo del happy path; no prueba los estados ni la máquina del chat; observabilidad ausente. |
| **competente** | Tests de componentes (los cuatro estados de una lista) + de la máquina de estados del chat (Vitest + Testing Library) + chequeo axe; lint en CI; **latencia/tokens por respuesta** registrados. |
| **excelente** | El test anti-XSS prueba el escapado; los tests no se acoplan a detalles de implementación (consultan por rol/texto, no por clases); la observabilidad ya distingue costo por pregunta (semilla de F6). |

### C7 — Entregables y comunicación · mapea: O3 · DoD 8 y 9 · hilo: inglés
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin README usable o sin demo; historial con `wip`/un commit gigante; sin write-up; README en español (con el hilo de inglés ya activo). |
| **en-progreso** | README incompleto (falta `pnpm dev` o capturas) o demo no mostrada; algunos commits no Conventional; write-up superficial. |
| **competente** | README **en inglés** que un desconocido sigue (qué es, `pnpm dev`, demo con capturas/GIF); historial 100% Conventional Commits; write-up de trade-offs (3–6 líneas). |
| **excelente** | El historial se lee como la historia del proyecto (spec → ADR → providers → features verticales → gate de a11y → docs); el write-up nombra un trade-off **defendible** (p. ej. token en cookie vs localStorage) y qué mediría distinto. |

### C8 — Autonomía y comprensión demostrada · gate Primero-Sin-IA · señal anti-dependencia
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No puede explicar partes de su propio código; sofisticación (abstracciones, hooks genéricos) que no calza con lo que defiende; indicios de UI pegada de un chat. |
| **en-progreso** | Explica el qué pero no el porqué; titubea al justificar por qué la lista no va en Zustand o por qué el parcial no se borra en error. |
| **competente** | Explica **cada decisión sin notas**: la frontera server/client/chat-state, los seis estados del chat, la regla anti-XSS, las tres medidas de a11y. |
| **excelente** | Reflexiona sobre dónde sintió el impulso de delegar a la IA; anticipa cómo evolucionará la UI en F6 (la IA al backend sin tocar el frontend); convierte una dificultad (a11y) en una regla reutilizable. |

## Errores típicos a marcar
- **Server-state en Zustand (o en `useEffect`):** la lista queda obsoleta, sin loading/error de primera clase ni invalidación. Va en TanStack Query.
- **Chat sin streaming:** `await res.json()` para un LLM = pantalla en blanco y muro de texto. El streaming es el baseline, no un extra.
- **`dangerouslySetInnerHTML` con salida del LLM:** XSS. Texto plano (React escapa) o markdown sanitizado sin HTML crudo.
- **a11y al final / solo con extensión:** axe no valida foco de teclado ni orden de lectura; falta la pasada manual. El gate exige teclado completo + foco manejado.
- **Solo el happy path:** faltan empty/loading/error. Una lista vacía mientras carga es indistinguible del estado vacío real.
- **Borrar el parcial del chat en error:** destruye lo que el usuario leía; hay que conservarlo + Reintentar.
- **API key del modelo en el cliente** (`NEXT_PUBLIC_`) o llamando al modelo desde el navegador.
- **Mutación sin invalidar la caché** de TanStack Query: la UI no refleja el cambio.
- (transversales) confía en la salida del LLM sin sanitizar; README en español con el hilo de inglés activo; falta un trade-off defendible en el write-up.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación. Nunca dar la solución.
- UI "de libro" (componentes pulidos, hooks genéricos) que el alumno no puede explicar pieza por pieza.
- `SPEC.md`/ADR con prosa pulida **desconectada** del código (menciona una frontera de estado que el código no respeta).
- Historial con **un commit gigante** o mensajes genéricos: señal de que pegó un resultado.
- a11y impecable en la spec pero la app pierde el foco al abrir el modal (la describió, no la implementó).
- **Verificación sugerida:** pídele que **en vivo** añada una vista nueva con sus cuatro estados y que la navegue solo con el teclado, explicando dónde vive cada dato. Si lo construyó de verdad, lo hace en minutos; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca entregar la arquitectura ni el código de la solución de referencia. El alumno eligió su layout: el feedback se ancla en *su* spec.
- **Pista (nivel 1):** "Apaga el backend y abre tu lista de colecciones. ¿Qué ve el usuario? Si es una pantalla en blanco o un error crudo, te falta el estado de error de primera clase (4.10)."
- **Pregunta socrática (nivel 2):** "Tu lista de colecciones, ¿de dónde saca su fuente de verdad? Si está en el servidor, ¿qué te da TanStack Query que tu store de Zustand te obliga a reimplementar a mano? ¿Qué pasa con tu lista si otro cliente crea una colección?"
- **Dirección concreta (nivel 3, solo tras intento real):** "La regla es **server-state en TanStack Query, client-state en Zustand**. Mueve la lista a un `useQuery` con su `queryKey`, invalida esa key en el `onSuccess` de la mutación de crear, y dibuja las cuatro ramas (isPending/isError/vacío/datos). Vuelve a probar apagando el backend antes de seguir."

## Conexión con el proyecto / capstone
- Este **es** el capstone de la Fase 4: cierra el constructive alignment de toda la fase (HTML/CSS de `4.1-4.3`, a11y de `4.4`, React/Next de `4.5-4.6`, TanStack Query/RHF de `4.7`, Zustand de `4.8`, estados de `4.10`, UI de IA de `4.11`). Consume el contrato OpenAPI + RFC 9457 del backend de la Fase 3 y es la **cara reutilizable** que la Fase 6 llena con RAG y agentes reales —sin tocar la UI, gracias a la frontera de estado y al contrato de streaming—. El gate de a11y/estados que se ejercita aquí reaparece en todo capstone con UI.
