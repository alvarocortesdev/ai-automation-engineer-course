---
ejercicio_id: fase-4/decidir-estado-global
fase: fase-4
sub_unidad: "4.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — ¿Dónde vive cada pieza de estado?

## Clasificación canónica

| # | Pieza | Tipo | Justificación |
|---|---|---|---|
| 1 | Texto del input | **local (`useState`)** | Solo lo usa el componente del input (controlado); nadie más necesita verlo hasta que se envía. |
| 2 | Lista de conversaciones | **server state (TanStack Query)** | Vino de `GET /api/conversaciones`; la UI guarda una cache, con refetch/staleness/invalidación que TanStack Query ya da. |
| 3 | Id de conversación abierta | **URL state** | Define qué pantalla veo, debe sobrevivir un refresh y ser compartible por link (`/chat/abc123`). |
| 4 | Modelo seleccionado | **global de cliente (Zustand)** | Dato de cliente que leen y cambian componentes lejanos (input, cabecera, ajustes); no vino de una API. |
| 5 | Sidebar abierto/cerrado | **local levantado** (o store pequeño) | Es UI; suele bastar `useState` en el layout. Si muchísimos componentes lejanos lo togglean, un mini-store es defendible: ahí está el trade-off. |
| 6 | Tema claro/oscuro | **global de cliente + `persist`** | Lo lee toda la app y debe sobrevivir recargas; cambia poco (Context también valdría, pero `persist` lo hace cómodo en Zustand). |
| 7 | Mensajes de la conversación | **server state (TanStack Query)** | Vienen de `GET .../mensajes` y se refrescan; misma razón que la pieza 2. |
| 8 | Token de sesión / API key | **secreto — fuera del store/`persist`** | No es estado de UI: es una credencial. Va en una **cookie httpOnly** (inaccesible a JS), no en `localStorage`. |

## Respuestas trampa

**T1 — Lista de conversaciones en Zustand.** Crea **dos fuentes de verdad**: la cache de TanStack Query y el store. Cuando llega una conversación nueva o se renombra una, ¿cuál copia está fresca? Tendrías que **reimplementar a mano** refetch, invalidación y *staleness* —justo lo que TanStack Query ya hace gratis—. El síntoma observable: la UI muestra datos viejos y nadie sabe por qué. Server state tiene dueño; no se duplica en un store de cliente.

**T2 — Token con `persist` a `localStorage`.** No. `localStorage` es texto plano legible por **cualquier script** de la página; ante un XSS, el atacante lee el token y secuestra la sesión. Un secreto nunca se persiste ahí. Debe vivir en una **cookie httpOnly** (el JavaScript no puede leerla; el navegador la envía sola en cada request), gestionada por el backend. El token no es "estado global de UI": es autenticación, y eso lo saca del store.

## Pieza ambigua (trade-off esperado)
La **pieza 5 (sidebar)** es el caso ambiguo legítimo. Respuesta competente: empezar **local levantado** (`useState` en el componente de layout que envuelve sidebar y contenido) por simplicidad; subir a un mini-store de UI **solo** si el toggle se dispara desde componentes lejanos (un atajo de teclado global, un botón en el footer, etc.) y el prop drilling se vuelve molesto. Reconocer que no hay una única respuesta correcta —y justificar la elegida— es lo que distingue C1-excelente.

## Qué premiar y qué penalizar
- **Premiar:** que 2 y 7 sean server state, 3 sea URL, y la respuesta T2 ataque desde seguridad (XSS + httpOnly). Esos tres puntos son el corazón del ejercicio.
- **Penalizar (marcar como antipatrón, no como "error de etiqueta"):** meter 2/7 en Zustand; poner 3 en un store; decir que el token va en el store con `persist`.
- **No penalizar:** clasificar 5 como global **si** justifica el trade-off; usar Context en vez de Zustand para 6 (válido, es low-frequency) siempre que note la diferencia de re-render.

## Variantes aceptables
- Pieza 6 con Context + un hook de tema en vez de Zustand: válido (es estado que casi nunca cambia). Lo importante es que NO la trate como server state ni la deje sin persistencia.
- Pieza 1 "levantada" al formulario si hay validación compartida: aceptable; sigue siendo local, no global.
- Llamar "client state" a 4/5/6 en inglés: válido (terminología técnica en inglés).
