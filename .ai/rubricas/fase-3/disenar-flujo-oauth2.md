---
ejercicio_id: fase-3/disenar-flujo-oauth2
fase: fase-3
sub_unidad: "3.12"
version: 1
---

# Rúbrica — Diseña los flujos de auth de tres clientes

> Rúbrica analítica para un ejercicio **a-mano** de diseño/criterio. Lo que se evalúa es la **justificación**,
> no solo la respuesta. Acertar "C1 → PKCE" sin poder explicar *por qué* (cliente público + usuario) es media
> respuesta; un trade-off bien defendido vale más que la etiqueta correcta. El corrector mide razonamiento.

## Objetivos evaluados
- **O1** — Elegir el flujo correcto por cliente, justificando con público/confidencial y con/sin usuario.
- **O2** — Explicar qué ataque evita PKCE y por qué un cliente público lo necesita.
- **O3** — Decidir almacenamiento de tokens (XSS vs CSRF) y diseñar rotación de refresh + scopes.

> Respuestas esperadas: **C1** authorization code + PKCE · **C2** client credentials · **C3** authorization code + PKCE. El corrector las conoce; **no las adelanta** al alumno: evalúa la justificación.

## Criterios y niveles

### C1 — Elección de flujo + justificación · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Asigna flujos al azar o todos iguales; sin justificar, o justificación equivocada. |
| **en-progreso** | Acierta 2 de 3 flujos, o los 3 pero justificando con un solo eje ("es el más seguro") sin distinguir público/confidencial ni con/sin usuario. |
| **competente** | Los 3 flujos correctos, cada uno justificado con **ambos** ejes (público vs confidencial, con/sin usuario). |
| **excelente** | Lo anterior + nombra que C1/C3 son públicos por razones distintas (código a la vista vs descompilable) y que C2 representa a sí mismo, no a un usuario. |

### C2 — PKCE y la trampa · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No explica PKCE, o lo confunde con "encriptar el token". No identifica la trampa. |
| **en-progreso** | Dice que PKCE "es más seguro" sin nombrar la intercepción del authorization code; o identifica solo una opción de la trampa. |
| **competente** | Explica que PKCE evita el canje de un **authorization code interceptado** (sin `code_verifier` no se canjea) y nombra un flujo incorrecto para C1 con razón. |
| **excelente** | Además explica por qué C2 no necesita PKCE (no hay redirect ni code que interceptar) y menciona que implicit está deprecado por OAuth 2.1. |

### C3 — Almacenamiento + refresh + scopes · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Recomienda `localStorage` sin matiz, o no decide; sin scopes ni rotación. |
| **en-progreso** | Elige cookie httpOnly pero sin nombrar el trade-off (no menciona CSRF), o da scopes pero no rotación (o viceversa). |
| **competente** | Refresh token en cookie httpOnly+Secure+SameSite con el trade-off XSS↔CSRF explícito; describe rotación con detección de reuso; 2 scopes de mínimo privilegio. |
| **excelente** | Lo anterior + menciona BFF y qué resuelve, y conecta el "no meter datos sensibles en el JWT" con que el payload es legible (base64, no cifrado). |

### C4 — Diagrama (sequenceDiagram de C1) · mapea: O1, O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay diagrama, o no es un flujo de OAuth2. |
| **en-progreso** | Diagrama incompleto: falta el `code_verifier`/`code_challenge` o el canje del code por tokens. |
| **competente** | `sequenceDiagram` con generación de verifier/challenge, login/consentimiento, retorno del code, canje code+verifier por tokens, y uso del access token. |
| **excelente** | Además muestra la verificación `SHA256(code_verifier) == code_challenge` en el authorization server y el refresh token. |

## Errores típicos a marcar
- **`client credentials` para C1 o C3**: el error estrella. Una SPA/móvil no puede esconder un `client_secret`, y client credentials no representa a un usuario.
- **Recomendar el implicit flow** "porque es para SPAs": desactualizado; deprecado por OAuth 2.1.
- **Creer que PKCE cifra algo** o que reemplaza a la firma del token: PKCE protege el *canje del code*, no el contenido del token.
- **`localStorage` para el refresh token** sin nombrar el riesgo XSS, o cookie sin mencionar CSRF: el ejercicio exige el **trade-off**, no una de las dos mitades.
- **Scopes vagos** (`admin`, `todo`) en vez de mínimo privilegio (`reportes:leer`).
- **Confundir autenticación con OAuth2/OIDC**: "OAuth2 es para login" sin notar que el login con identidad es OIDC encima de OAuth2.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Texto extenso y pulido que enumera flujos de memoria pero no aterriza en los **tres clientes concretos** del enunciado (respuesta genérica copiada).
- Menciona flujos avanzados (device code, JARM) sin que apliquen, como relleno, sin poder defender por qué C1 no los usa.
- Recomendación de almacenamiento sin trade-off (solo "usa httpOnly") — síntoma de regla memorizada sin el porqué.
- **Verificación sugerida:** pídele que defienda, en voz alta, por qué C2 no necesita PKCE pero C3 sí, en una frase. Si entendió, distingue "hay redirect + code que interceptar" de "no hay".

## Feedback sugerido (graduado)
> Nunca dar la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para cada cliente, pregúntate dos cosas antes de elegir flujo: ¿puede este cliente **guardar un secreto** sin que alguien lo extraiga? ¿Hay un **humano** que apruebe el acceso? Tus respuestas ya casi eligen el flujo."
- **Pregunta socrática (nivel 2):** "El código de tu SPA viaja al navegador de cada usuario. Si pusieras ahí un `client_secret`, ¿cuántas personas podrían leerlo abriendo las DevTools? ¿Sigue siendo un secreto?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "C1 y C3 son clientes **públicos** con usuario → authorization code + PKCE (PKCE sustituye el secreto que no pueden guardar). C2 es **confidencial** sin usuario → client credentials. Reescribe tus justificaciones nombrando esos dos ejes explícitamente."

## Conexión con el proyecto / capstone
- En el [capstone](/fase-3-backend/proyecto/) defines cómo se autentican los clientes de tu API; este ejercicio es el ADR de esa decisión (flujo elegido + almacenamiento de tokens + scopes), justo el "write-up de trade-offs" que pide el Definition of Done.
