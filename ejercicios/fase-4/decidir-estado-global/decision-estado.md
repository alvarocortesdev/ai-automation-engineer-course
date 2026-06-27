# Decisión de estado — ChatLab

> Completa la tabla y las dos respuestas. Una frase de justificación por pieza.
> Tipos válidos: `local (useState)` · `server state (TanStack Query)` · `URL state` · `global de cliente (Zustand)`.

## Clasificación de las 8 piezas

| # | Pieza de estado | Tipo | Justificación (1 frase: por qué ahí y no en otro cubo) |
|---|---|---|---|
| 1 | Texto del input del chat (sin enviar) | _TODO_ | _TODO_ |
| 2 | Lista de conversaciones (`GET /api/conversaciones`) | _TODO_ | _TODO_ |
| 3 | Id de la conversación abierta (`/chat/abc123`) | _TODO_ | _TODO_ |
| 4 | Modelo de IA seleccionado | _TODO_ | _TODO_ |
| 5 | Barra lateral abierta/cerrada | _TODO_ | _TODO_ |
| 6 | Tema claro/oscuro (sobrevive recarga) | _TODO_ | _TODO_ |
| 7 | Mensajes de la conversación abierta (`GET .../mensajes`) | _TODO_ | _TODO_ |
| 8 | Token de sesión / API key | _TODO_ | _TODO_ |

## Preguntas trampa

**T1 — Lista de conversaciones en Zustand "para tenerla a mano". ¿Por qué es mala idea?**

_TODO: nombra el problema concreto (qué se rompe / qué tienes que reimplementar)._

**T2 — ¿Token con `persist` a `localStorage`? Justifica desde seguridad y di dónde debería vivir.**

_TODO._

## Pieza ambigua: trade-off

_TODO: elige una pieza (típicamente la 5) y explica el trade-off de tu elección
(p. ej. local levantado vs. store pequeño)._
