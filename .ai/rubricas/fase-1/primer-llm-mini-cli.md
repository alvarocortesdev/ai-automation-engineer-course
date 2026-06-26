---
ejercicio_id: fase-1/primer-llm-mini-cli
fase: fase-1
sub_unidad: "1.10"
version: 1
---

# Rúbrica — Tu primer LLM en una mini-CLI

> Rúbrica **analítica** atada a los `objetivos`. El corazón del ejercicio NO es "llamar a Claude"
> (eso son tres líneas), sino los hábitos que lo vuelven código de ingeniero: **secreto en el
> entorno**, **validar antes de gastar una llamada**, **mapear los fallos del SDK a errores de
> dominio**, y **dejar el llamado testeable** (el mismo seam de `fetch` de 1.5). Evaluar la
> comprensión de esos hábitos tanto como la corrección del llamado.

## Objetivos evaluados
- **O1** — Llamar al LLM con el SDK oficial y leer el texto (`content[0].text`), con `model` y `max_tokens`.
- **O2** — Leer la API key de una variable de entorno; no hardcodearla ni imprimirla.
- **O3** — Validar el input antes de la llamada y mapear los fallos del SDK a errores de dominio claros.
- **O4** — Hacer testeable el código inyectando el modelo, sin tocar la red ni gastar tokens.

## Criterios y niveles

### C1 — Manejo del secreto (API key) · mapea: O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | La key está hardcodeada en el código, se imprime/loguea, o se pasa como literal a `Anthropic(api_key="sk-...")`. |
| **en-progreso** | Lee la key del entorno pero sin gate claro: si falta, revienta con un stack trace en vez de un error útil. |
| **competente** | `leer_api_key` lee `ANTHROPIC_API_KEY`, lanza `FaltaApiKey` con mensaje claro si falta/está vacía, y nunca imprime el valor. |
| **excelente** | Además explica por qué un secreto en el código es irreversible (queda en el historial de Git) y menciona `.env` + `.gitignore` como el patrón de proyecto. |

### C2 — Corrección del llamado y lectura de la respuesta · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No construye el llamado, o trata `mensaje.content` como string, o omite `max_tokens`. |
| **en-progreso** | Llama bien pero lee la respuesta de forma frágil (asume estructura sin `content[0].text`), o importa `anthropic` a nivel de módulo (rompe los tests offline). |
| **competente** | `messages.create` con `model`, `max_tokens` y `messages`; lee `content[0].text`; importa `anthropic` **dentro** del adaptador. |
| **excelente** | Reconoce que `content` es una lista de bloques y por qué; usa el modelo barato (Haiku) a conciencia y/o reporta `usage` (costo). |

### C3 — Validación previa, mapeo de errores y seam testeable · mapea: O3, O4
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No valida el prompt (llama al modelo con input vacío), o no separa la lógica del adaptador (el SDK está acoplado al núcleo). |
| **en-progreso** | Valida pero después de llamar (gasta la petición), o atrapa los errores del SDK con `except Exception` genérico, o `responder` conoce el SDK. |
| **competente** | Valida **antes** del llamado; `responder` recibe el modelo inyectado y no sabe del SDK; `preguntar_a_claude` (adaptador) mapea `AuthenticationError → FaltaApiKey` y `APIError → ModeloInalcanzable`; `main` traduce a códigos 2/3/4; los tests usan un fake sin red. |
| **excelente** | Sabe explicar que el adaptador es una semilla de "ports & adapters" y que el seam es el mismo que el `fetch` de 1.5 y el que mockea un LLM en 2.11; su fake es mínimo y claro. |

## Errores típicos a marcar
- **Key hardcodeada o impresa**: el secreto en el código viaja a Git para siempre; imprimirlo lo filtra a logs.
- **`mensaje.content` tratado como string**: el texto está en `content[0].text` (lista de bloques), no en `content`.
- **Omitir `max_tokens`**: es obligatorio en este SDK; además es el freno de costo/longitud.
- **`import anthropic` a nivel de módulo**: rompe los tests offline (que no requieren el paquete). Debe ir dentro del adaptador.
- **Validar el prompt después de llamar**: gasta una petición (y plata) en input que ya se sabía inválido. El test `modelo_que_no_debe_correr` lo detecta.
- **`except Exception` genérico** en `responder`: atrapa también bugs propios. El mapeo de errores del SDK va en el adaptador, con tipos específicos (`anthropic.AuthenticationError`, `anthropic.APIError`).
- **Acoplar el SDK al núcleo**: si `responder` importa o conoce `anthropic`, deja de ser testeable sin el paquete y sin red.
- (transversal seguridad) tratar la salida del LLM como confiable: imprimir está bien hoy, pero el reflejo "no confíes en el output" (alucinación, prompt injection) debe estar presente en su write-up/explicación.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Manejo de excepciones de `httpx` o reintentos con backoff/`tenacity` (no pedidos, propios de F3): sofisticación impropia del nivel, señal de haber pegado un cliente genérico.
- Parámetros del SDK que no se enseñan aquí (`thinking`, `stream`, `tools`, `temperature`) apareciendo sin que el alumno pueda explicarlos.
- No puede explicar por qué los tests no necesitan red, key ni el paquete `anthropic`.
- **Verificación sugerida:** pedir que, sin ejecutar, prediga qué pasa si llama `responder("  ", fake)` y por qué el fake no se ejecuta; y que escriba el fake mínimo que simule un `ModeloInalcanzable`.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Hay dos cosas que el modelo nunca debería ver: un prompt vacío y una llamada que no hace falta. ¿En qué orden conviene validar el input respecto a llamar al modelo? ¿Y dónde vive el conocimiento del SDK —en `responder` o en el adaptador?"
- **Pregunta socrática (nivel 2):** "Si tu test inyecta un modelo falso, ¿necesita internet? ¿Necesita una API key? ¿Necesita el paquete `anthropic` instalado? Si alguna respuesta es 'sí', algo está acoplado donde no debería. ¿Dónde está el `import anthropic`?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Estructura: `leer_api_key` lee del entorno y lanza `FaltaApiKey`. `responder` valida `if not prompt or not prompt.strip()` **antes** de delegar. `preguntar_a_claude` importa `anthropic` adentro, envuelve `messages.create` en `try/except anthropic.AuthenticationError / anthropic.APIError`, y devuelve `content[0].text`. `main` ordena las guardas en códigos 2/3/4. Revisa la sección 4.6 y reintenta antes de mirar la referencia."

## Conexión con el proyecto / capstone
- El seam de inyección y el manejo de secretos por entorno son la base testeable del **Capstone F1**, y exactamente la mecánica que la Fase 6 toma para sumarle prompt engineering, salidas estructuradas, evals y seguridad de LLM. Un LLM es una API; se llama y se mockea como cualquier otra.
