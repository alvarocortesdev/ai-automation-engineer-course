# Capstone Fase 3 — API de producción

> **Modalidad: capstone (mixto — código + spec/ADR/README + infra).** Es el proyecto final de la Fase 3:
> una **API REST de producción** con FastAPI, PostgreSQL y todo lo que separa un CRUD de juguete de un
> backend que un equipo desplegaría. No es un ejercicio con tests que ya están escritos: aquí decides el
> dominio, la arquitectura y cada línea, y luego defiendes por qué. Es la base reutilizable que la Fase 4
> (frontend) consume y la Fase 6 (IA) extiende.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.P` Capstone — API de producción
**Ruta:** crítica · **Timebox:** proyecto · 15–25 h repartidas en 1–2 semanas

## 🎯 Objetivo

Construir una API REST que cumpla el **Definition of Done** del curso: spec primero, arquitectura ports &
adapters, persistencia en PostgreSQL con migraciones Alembic, OAuth2/JWT con autorización real, OWASP
aplicado (Broken Access Control, Injection, SSRF), idempotencia y rate limiting, errores RFC 9457,
observabilidad mínima, secretos fuera del repo, una suite de tests medida por **mutation score** y un README
en inglés con demo que corre. Al terminar puedes explicar y defender cada decisión sin notas.

## 📋 Contexto

Las dieciséis sub-unidades de la Fase 3 fueron piezas: modelado, queries, transacciones, FastAPI, hexagonal,
OAuth2, OWASP, idempotencia. Este capstone las ensambla en **un** sistema coherente. El backend es donde vive
la lógica de las apps de IA que vas a construir: en la Fase 6 servir un modelo o un pipeline RAG es exponer
*este mismo backend* con un endpoint más. Hacerlo bien una vez te ahorra reescribirlo tres fases después —y
es la pieza de portafolio que un recruiter abre primero (README, commits, tests, secretos).

## 📏 Primero-Sin-IA (el corazón de este capstone)

Este capstone es **repaso integrador**: ya conoces cada concepto, ahora los combinas. Por eso el Primero-Sin-IA
es de entrada (no hay worked example nuevo que copiar), con andamiaje en el *proceso*, no en el código.

1. **Piensa tú el diseño.** La spec, el modelo de datos, los puertos/adapters y las mitigaciones de seguridad
   los razonas a mano, sin IA. La arquitectura es la parte que más se aprende pensándola.
2. Consulta **documentación oficial** (FastAPI, SQLAlchemy 2.0, Alembic, RFC 9457, OWASP) cuando lo necesites.
3. **Solo al final**, si quieres, usa IA para *revisar y explicar* lo que ya construiste —nunca para *generar
   la arquitectura ni las mitigaciones*. Pegar un backend completo de un chat es saltarse el capstone entero.
4. **Mañana**, reescribe tu `SPEC.md` de memoria. Si no puedes, no internalizaste tu propio diseño.

> "Sin IA para razonar" = no le delegas el diseño, la arquitectura ni la lógica de seguridad. Usar docs
> oficiales, `man` y autocompletado básico está bien. Si quitarte el chat te deja sin saber por dónde empezar,
> ese vacío es justo lo que el capstone vino a llenar.

## 🛠️ El brief

Construye una API REST de **producción** sobre el dominio que elijas. Recomendado (y pensado para que la Fase 6
lo convierta en RAG sin reescribir): una **base de conocimiento de documentos**.

### El dominio debe tener estas tres superficies (sí o sí)

Elige cualquier dominio, pero **debe** incluir:

1. **Recursos que pertenecen a un usuario** → superficie de control de acceso (IDOR). Ej.: `colecciones` y
   `documentos` con `owner_id`.
2. **Una acción sensible que no debe ejecutarse dos veces** → superficie de idempotencia. Ej.: "encolar
   procesamiento de un documento", "registrar un cobro".
3. **Un endpoint que hace una petición de red saliente** → superficie de SSRF. Ej.: "importar documento desde
   una URL".

Dominios que califican: gestor de gastos compartidos, API de reservas, acortador de URLs con cuotas, gestor de
documentos. **No** califica un to-do list sin dueños ni acciones sensibles (te quedas sin la mitad de los
requisitos).

### Requisitos mínimos (lo que se evalúa)

- **Persistencia:** PostgreSQL + SQLAlchemy (estilo 2.0). **Todo cambio de esquema es una migración Alembic.**
  Prohibido `Base.metadata.create_all` como mecanismo de esquema en producción.
- **Arquitectura:** ports & adapters *light*. El paquete de dominio **no importa** `fastapi` ni `sqlalchemy`.
  Define puertos (interfaces) y adapters (router HTTP, repo SQLAlchemy, cliente httpx).
- **Auth (autenticación):** OAuth2 password flow + JWT. Hashing con `pwdlib` (argon2), firma con `PyJWT`.
- **Authz (autorización):** cada recurso se filtra por dueño y/o scope. Un usuario **no** puede leer/editar el
  recurso de otro (ni cambiando el id en la URL).
- **OWASP aplicado (hands-on, no nociones):**
  - **Broken Access Control / IDOR:** la query filtra por `owner_id` siempre (la defensa vive en la query, no
    en un `if` posterior).
  - **Injection:** queries parametrizadas / ORM; nada de f-strings con SQL.
  - **SSRF:** guardia en el import por URL —resuelve el DNS, rechaza IPs privadas/loopback/link-local y el
    endpoint de metadata del cloud (`169.254.169.254`), valida el esquema (`http/https`) y controla redirecciones.
- **Confiabilidad:** **idempotencia** (`Idempotency-Key`) en el endpoint sensible (clave persistida con índice
  único; el reintento devuelve el resultado guardado, no repite el efecto). **Rate limiting** en auth e import.
- **Contrato:** OpenAPI automático en `/docs`. Errores en formato **RFC 9457** (`application/problem+json`, con
  `type`/`title`/`status`/`detail`/`instance`).
- **Calidad:** suite de tests (contrato con `TestClient` + dominio puro) **medida por mutation score** (mutmut).
  Lint (ruff) en CI.
- **Observabilidad:** logs estructurados (JSON) con un **correlation ID** por request. (Trazas OpenTelemetry =
  stretch, no obligatorio en F3.)
- **Secretos:** en `.env` (gitignored) + `gitleaks` en CI. Cero secretos en el código o en el historial.
- **Comunicación:** README **en inglés** con `docker compose up` y una **sesión real pegada** (la demo que
  corre); write-up de trade-offs; historial 100% **Conventional Commits**.

## ✅ Criterios de "hecho" (Definition of Done — Fase 3)

Este capstone se mide contra el **Definition of Done único** del curso. En la Fase 3 aplican estos puntos (el 5
—eval de IA—, el 6 —agente— y el 7 —a11y de UI— se siembran y se exigen en F4 y F6):

- [ ] **(DoD 1)** `SPEC.md` existe y se escribió **antes** que el código (su commit precede al primer endpoint),
  más al menos un **ADR** que justifica la decisión de arquitectura (ports & adapters vs CRUD acoplado).
- [ ] **(DoD 2)** Tests verdes + lint en CI; calidad demostrada con **mutation score** (mutmut), no con % de
  coverage. Hay tests de contrato (401/404-RFC9457/409-idempotencia/422/429) y de dominio.
- [ ] **(DoD 3)** Seguridad aplicada y demostrable: IDOR cerrado (test que prueba 403/404 al recurso ajeno),
  Injection imposible (queries parametrizadas), SSRF bloqueado (test con IP privada/metadata). `gitleaks` y un
  dependency-scan (`pip-audit` o equivalente) corren en CI.
- [ ] **(DoD 4)** Observabilidad: logs estructurados con correlation ID por request (se ve en la demo).
- [ ] **(DoD 8)** La API **corre** (`docker compose up`) y hace lo que el README promete (**demo pegada**);
  README **en inglés**; write-up de trade-offs (qué dejaste fuera y por qué, qué fue lo más difícil).
- [ ] **(DoD 9)** Todo el historial usa **Conventional Commits**.
- [ ] **(Gate Primero-Sin-IA)** Diseñaste la arquitectura y las mitigaciones sin delegar el pensamiento a una
  IA; puedes explicar **cada decisión y cada mitigación sin notas**.

## 📂 Estructura sugerida del entregable

```text
mi-api/
├── SPEC.md                  ← copia plantillas/SPEC.md; escríbela PRIMERO
├── README.md                ← en inglés: qué es, docker compose up, demo que corre, trade-offs
├── pyproject.toml           ← copia plantillas/pyproject.toml (deps con uv)
├── .env.example             ← copia plantillas/.env.example; el .env real va gitignored
├── docker-compose.yml       ← tu app + postgres
├── alembic.ini
├── migrations/              ← versiones Alembic
├── docs/
│   └── ADR-0001-*.md        ← copia plantillas/ADR-0001-arquitectura-hexagonal.md
├── src/
│   ├── dominio/             ← entidades + puertos (CERO imports de fastapi/sqlalchemy)
│   ├── casos_uso/           ← la lógica de negocio
│   ├── adapters/
│   │   ├── http/            ← routers FastAPI, dependencias, exception handlers RFC 9457
│   │   └── db/              ← modelos SQLAlchemy + repos que implementan los puertos
│   └── main.py              ← arma la app, lifespan, limiter, handlers, logging
├── tests/                   ← contrato (TestClient) + dominio (puro). Ver tests/ aquí como guía.
└── .github/workflows/ci.yml ← lint + test + mutmut + gitleaks + dependency-scan
```

## 🧭 Orden recomendado de construcción (la disciplina ES el orden)

1. **Elige el dominio** (con las tres superficies). 2. **Escribe `SPEC.md`** (antes del código). 3. **Escribe el
ADR** de arquitectura. 4. **Primera migración Alembic** (esquema base). 5. **Construye por capas verticales:**
auth completa y verde → recurso con dueño y su test de acceso → import con guardia SSRF → idempotencia → pulido
(RFC 9457, rate limiting, logs, mutmut). Una feature verde antes de la siguiente; nunca 2000 líneas que
"deberían funcionar".

> El error #1 es empezar por el código (paso 5) y dejar spec/ADR/seguridad "para después". El error #2 es
> construir todos los modelos, luego todos los endpoints (capas horizontales): te quedas sin nada que corra hasta
> el final. Verticaliza.

## 💡 Pista (ábrela solo si te trabas con el arranque)

<details>
<summary>Mostrar pista</summary>

Si te paralizas, casi siempre saltaste la spec o intentas todo a la vez. Vuelve a lo mínimo que corre: un
`POST /auth/registro` que persista un usuario con la contraseña **hasheada** y un `POST /auth/token` que devuelva
un JWT. Pruébalo con `/docs`. Esa sola feature, verde y con su test, te da el esqueleto (app + router +
dependencia de sesión + un exception handler). A partir de ahí, cada recurso es el mismo patrón: caso de uso en
el dominio, puerto, adapter de repo, router. Para el control de acceso, el truco mental es "el recurso de otro
no existe para mí": la query SIEMPRE lleva `WHERE owner_id = <usuario actual>`. Esto es una pista del *proceso*;
la arquitectura y las mitigaciones las diseñas tú.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA tu proyecto completo (este directorio o tu repo), la **rúbrica**
(`.ai/rubricas/fase-3/capstone-api-produccion.md`) y `.ai/INSTRUCCIONES-CORRECTOR.md`. Pídele:

> "Corrige mi capstone `ejercicios/fase-3/capstone-api-produccion/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md` al pie de la letra."

La **solución de referencia** (un proyecto ejemplar) vive en `.ai/soluciones/fase-3/capstone-api-produccion.md`
— es material del corrector; no la mires antes de cerrar tu intento. En un capstone de diseño **no hay una única
respuesta correcta**: el corrector evalúa tu spec, tu arquitectura, tus mitigaciones y si puedes defender tus
decisiones, no si elegiste "el" dominio.
