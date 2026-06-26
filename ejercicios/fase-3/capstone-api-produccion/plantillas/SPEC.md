# SPEC — <nombre de tu API>

> Escribe esto ANTES del código. La spec es tu lista de tests futura. Si no puedes describir un
> endpoint en una línea, todavía no lo entiendes. Borra los comentarios `<...>` al completar.

## Propósito

<Una frase: qué resuelve esta API y para quién.>

## Recursos y dueños

<Lista los recursos y quién es su dueño. Deja explícitas las claves foráneas.>

- `users` (id, email único, hashed_password, created_at)
- `<recurso>` (id, owner_id → users.id, ...)
- `idempotency_keys` (key único, user_id, endpoint, status, response_body, created_at)

## Endpoints (verbo · ruta · auth · status de éxito · errores)

> Marca cuáles exigen autenticación y cuáles validan dueño/scope.

| Verbo | Ruta | Auth | Éxito | Errores posibles |
|---|---|---|---|---|
| POST | /auth/registro | no | 201 | 409 email duplicado, 422 inválido, 429 |
| POST | /auth/token | no | 200 | 401 credenciales, 422, 429 |
| POST | /<recurso> | sí | 201 | 401, 422 |
| GET | /<recurso>/{id} | sí (dueño) | 200 | 401, 404 (incluye "no es tuyo") |
| GET | /<recurso> | sí | 200 | 401 (paginado: ?saltar&limite) |
| POST | /<recurso>/importar | sí | 202 | 400 URL inválida/SSRF, 401, 422 |
| POST | /<recurso>/procesar | sí (Idempotency-Key) | 202 | 401, 409/200 si repetido |

## Contrato de error (RFC 9457)

Todos los errores devuelven `application/problem+json` con: `type`, `title`, `status`, `detail`, `instance`.

## Casos borde y decisiones de seguridad

- **Acceso a recurso ajeno** → la query filtra por `owner_id`; el recurso ajeno no existe para mí (404, no 403, para no filtrar existencia).
- **Import con URL interna** (`http://169.254.169.254/`, `http://localhost:...`, IP privada) → 400, la guardia SSRF la rechaza.
- **Reintento con mismo `Idempotency-Key`** → no repite el efecto; devuelve el resultado del primer intento.
- **Body inválido** (campo faltante/tipo erróneo) → 422 de pydantic, antes de tocar la lógica.
- **Demasiados requests a /auth/token** → 429 (rate limit).
- **Secretos** → `SECRET_KEY`, `DATABASE_URL` salen de env vars; nunca del código.

## Fuera de alcance (a propósito)

<Qué NO vas a hacer y por qué. Acotar es diseño.>
