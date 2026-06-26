# Ejercicio 3.12b — Diseña los flujos de auth de tres clientes (y dónde guardar el token)

> **Modalidad: a mano (razonamiento y diseño, sin IA, sin código que correr).** Entrena el criterio que se
> mide en entrevistas: elegir el flujo OAuth2 correcto según el tipo de cliente, decidir dónde vive el token
> en el navegador razonando XSS vs CSRF, y diseñar refresh + scopes. No hay test que pase; hay decisiones
> que defender.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.12` Autenticación y OAuth2 a fondo
**Ruta:** crítica · **Timebox:** 35–40 min

## 🎯 Objetivo

Demostrar, por escrito y con un diagrama, que sabes (1) elegir entre `authorization code + PKCE` y
`client credentials` según **cliente público vs confidencial** y **con/sin usuario**, (2) explicar qué ataque
evita PKCE, (3) decidir el almacenamiento de tokens en el navegador razonando el trade-off **XSS vs CSRF**, y
(4) diseñar rotación de refresh tokens con scopes de mínimo privilegio. Sin este criterio, "sé OAuth2" se
convierte en copiar el flujo equivocado de un tutorial desactualizado.

## 📋 Contexto

En el capstone tu API tendrá clientes distintos: un frontend, quizá un servicio que la consume sin usuario.
Cada uno se autentica distinto, y elegir mal el flujo (o guardar el token en el lugar equivocado) es una
vulnerabilidad real, no un detalle. Este ejercicio es puro criterio defendible.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Razona antes de escribir.
2. Solo entonces, consulta la **documentación oficial** (OAuth 2.0 Simplified de Aaron Parecki; RFC 7636 PKCE;
   MDN sobre `Set-Cookie` `HttpOnly`/`SameSite`) y la lección (secciones 4.6–4.10) para validar.
3. **Solo al final**, usa IA para *revisar* tu diseño — no para generarlo.
4. Mañana, redibuja el flujo de C1 de memoria y explícalo en voz alta a alguien.

## Los tres clientes a diseñar

Tu API (resource server) necesita ser consumida por tres clientes distintos:

> - **C1 — SPA en React** que corre en el navegador, con **usuarios humanos** que inician sesión.
> - **C2 — Cron job nocturno** (un script en un servidor) que llama a tu API para generar reportes. **No hay
>   usuario presente**; corre solo.
> - **C3 — App móvil nativa** (iOS/Android) con **login de usuario**.

## 🛠️ Qué entregar (deja estos archivos en esta carpeta)

### `decisiones.md`

1. **Flujo por cliente**: para **C1, C2 y C3**, indica el flujo OAuth2 (`authorization code + PKCE` o
   `client credentials`) y justifica en 2–3 líneas usando **dos** ejes: ¿cliente **público** (no puede
   esconder un secreto) o **confidencial**? ¿Hay un **usuario humano** que dé consentimiento?
2. **PKCE**: explica en 3–4 líneas **qué ataque evita** PKCE (pista: intercepción del authorization code) y
   por qué C1 y C3 lo necesitan pero C2 no.
3. **Almacenamiento del token en C1**: decide dónde guardar el **refresh token** del navegador
   (cookie `httpOnly` vs `localStorage`) y justifica con el trade-off **XSS vs CSRF**. Menciona el patrón
   **BFF** como alternativa y qué problema resuelve.
4. **Refresh + scopes**: describe la **rotación con detección de reuso** de refresh tokens (qué pasa cuando un
   refresh token ya usado reaparece) y propón **2 scopes** concretos de mínimo privilegio para tu API
   (ej. `reportes:leer`).
5. **La trampa (obligatoria)**: nombra **un** flujo que sería **incorrecto** para C1 y por qué (hay al menos
   dos respuestas válidas: `client credentials` y el viejo `implicit flow`).
6. **JWT (1 línea)**: explica por qué, aunque el access token vaya firmado, **no** pondrías el rol de
   facturación ni datos sensibles del usuario dentro del payload (conecta con el ejercicio `verificar-jwt-a-mano`).

### `diagrama.md`

Un diagrama **Mermaid** (`sequenceDiagram`) del flujo de **C1** (`authorization code + PKCE`) que muestre, en
orden: la generación del `code_verifier` y el `code_challenge`, el login/consentimiento del usuario en el
authorization server, el retorno del authorization code, el canje del code + `code_verifier` por tokens, y el
uso del access token contra tu API.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] C1 → `authorization code + PKCE`, C2 → `client credentials`, C3 → `authorization code + PKCE`, cada uno
      justificado con público/confidencial y con/sin usuario.
- [ ] Explicaste qué ataque evita PKCE y por qué C2 no lo necesita.
- [ ] Decidiste el almacenamiento del refresh token de C1 con el trade-off XSS vs CSRF, y mencionaste BFF.
- [ ] Describiste la rotación con detección de reuso y propusiste 2 scopes de mínimo privilegio.
- [ ] Nombraste un flujo incorrecto para C1 y por qué (client credentials o implicit).
- [ ] El `sequenceDiagram` de C1 incluye `code_verifier`/`code_challenge` y el canje del code por tokens.
- [ ] Puedes defender **sin notas** por qué una SPA no usa client credentials.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **C1 y C3** tienen un **usuario humano** y son **clientes públicos** (el código de una SPA está a la vista
  en el navegador; una app móvil se puede descompilar) → no pueden esconder un `client_secret` →
  `authorization code + PKCE`. PKCE reemplaza al secreto que no pueden guardar.
- **C2** no tiene usuario y corre en un servidor (cliente **confidencial**, sí puede guardar un secreto) →
  `client credentials`. No hay a quién mostrarle una pantalla de consentimiento.
- **PKCE** evita que un atacante que **intercepte el authorization code** (en el redirect) lo canjee: sin el
  `code_verifier` original, el authorization server rechaza el canje.
- **Almacenamiento C1:** `localStorage` es robable por cualquier **XSS** (un script inyectado lo lee). Cookie
  `httpOnly`+`Secure`+`SameSite` no es legible por JS (mitiga XSS) pero el navegador la manda sola → expones
  a **CSRF**, que mitigas con `SameSite` y/o un token anti-CSRF. El refresh token va en cookie httpOnly, no en
  localStorage. **BFF** mueve los tokens al servidor y le da al navegador solo una cookie de sesión.
- **La trampa:** `client credentials` para C1 es incorrecto (no hay secreto que esconder + es para máquina a
  máquina); el **implicit flow** está deprecado por OAuth 2.1.

Repasa las secciones 4.6–4.10 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `decisiones.md` + `diagrama.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/disenar-flujo-oauth2.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/disenar-flujo-oauth2.md` — no la mires antes de
intentarlo.
