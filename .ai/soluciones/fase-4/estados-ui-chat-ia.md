---
ejercicio_id: fase-4/estados-ui-chat-ia
fase: fase-4
sub_unidad: "4.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un ejercicio de diseño:
> esta solución es una **referencia de calidad**, no la única respuesta correcta. Evalúa el
> razonamiento contra la rúbrica; acepta variantes bien argumentadas.

# Solución de referencia — Estados y seguridad de una UI de chat de IA

## 1. Inventario de estados (referencia)

| Estado | Qué ve el usuario | Transición que lo activa |
|---|---|---|
| **vacío** | Pantalla limpia con sugerencias / "¿en qué te ayudo?" | Sin historial (`messages.length === 0`) |
| **enviando** | Su mensaje ya visible + "Pensando…" | Llamó a `sendMessage`; mandó, aún no llega ningún token (`status: "submitted"`) |
| **streaming** | La respuesta creciendo token a token + botón "Detener" | Llegó el primer chunk (`status: "streaming"`) |
| **completado** | La respuesta entera; input habilitado | El stream cerró (`status: "ready"`) |
| **error** | Aviso de error + "Reintentar", **conservando el parcial** | Falló la petición o se cortó el stream (`status: "error"`) |
| **cancelado** | El parcial congelado; input habilitado | El usuario apretó "Detener" (`stop()`) |

La distinción clave es **enviando vs streaming**: no son "cargando". En `enviando` no llegó nada todavía (latencia hasta el primer token); en `streaming` el texto ya está apareciendo. Y `cancelado`/`vacío` son estados de pleno derecho, no casos borde.

## 2. Diagnóstico del componente `ChatIA`

- **Defecto 1 — sin streaming.** `await res.json()` espera la respuesta completa del modelo (varios segundos de pantalla muerta). → Arreglo: streaming con `useChat` + `streamText` (secciones 4.2–4.4); el texto aparece a medida que se genera.
- **Defecto 2 — sin optimistic UI.** El mensaje del usuario nunca se muestra; el historial solo recibe la respuesta del modelo. → Arreglo: meter el mensaje del usuario al instante (lo hace `sendMessage` / el caso `ENVIAR` del reducer, sección 4.5).
- **Defecto 3 — XSS.** `dangerouslySetInnerHTML={{ __html: item }}` sobre salida del LLM. → Arreglo: renderizar como texto (`{texto}`) o markdown sanitizado sin HTML (sección 4.7).
- **Defecto 4 — sin estados.** No hay "pensando", ni error visible, ni botón de cancelar, ni estado vacío. → Arreglo: los seis estados de la sección 4.6 (`status`, `error`/`regenerate`, `stop`).
- **(Extra) sin a11y.** El texto que llega no se anuncia a un lector de pantalla. → Arreglo: `aria-live="polite"` en el contenedor de mensajes.
- **(Extra) error mudo.** Si la red falla, el botón "queda muerto" sin feedback. → Arreglo: estado `error` con aviso y reintento.

## 3. Seguridad

- **Riesgo:** la salida del LLM es **no confiable** —un modelo puede ser inducido (prompt injection) a devolver HTML o `<script>`—. Renderizarla con `dangerouslySetInnerHTML` ejecuta ese HTML en el navegador del usuario: **XSS**.
- **Regla correcta:** renderizar la salida como **texto** (React escapa el contenido de `{}` por defecto); si se necesita formato, usar un renderer de markdown que **sanitiza** y **no** permite HTML embebido.
- **Conexión con OWASP:** es la misma regla de la Fase 3 —nunca confiar en datos de un sistema externo—, y un LLM (aunque lo reenvíe tu propio backend) es un sistema externo. Defensa en profundidad: sanitizar/validar también del lado servidor.

## 4. Accesibilidad

- **Medida 1 — `aria-live="polite"`** en el contenedor de mensajes, para que un lector de pantalla anuncie el texto que va llegando sin interrumpir bruscamente.
- **Medida 2 — affordance de cancelar accesible por teclado** (el botón "Detener" alcanzable con tab y operable con Enter/Espacio) y manejo del foco al terminar la respuesta. (También válido: respetar `prefers-reduced-motion` si se anima la aparición del texto.) Conecta con [4.4 WCAG 2.2](/fase-4-frontend/4-4-accesibilidad-wcag/).

## 5. Trade-off

- **Beneficio:** streaming + optimistic UI bajan la **latencia percibida** —el usuario ve su mensaje y el primer token casi de inmediato— y dan sensación de control (puede cancelar). La respuesta tarda lo mismo en total; lo que cambia es la experiencia.
- **Costo:** más complejidad de estado (una máquina con `enviando`/`streaming`/`error`/`cancelado` en vez de un simple `cargando`/`listo`), y la responsabilidad de manejar bien los caminos de fallo.
- **Decisión:** para una app de IA, el beneficio domina: esperar la respuesta completa se siente roto. La complejidad se contiene usando `useChat` (o un reducer bien probado), que encapsula la máquina de estados.

## Notas para el corrector
- No exijas las palabras exactas de la tabla; exige los **seis** estados y la distinción enviando/streaming.
- El XSS es no negociable: si el alumno no lo detecta o cree que "como es mi backend es seguro", es C3-incompleto y hay que nombrarlo.
- Acepta como excelente cualquier respuesta que articule "el streaming no acelera la generación, mejora la latencia percibida" sin que se lo hayan pedido literalmente.
