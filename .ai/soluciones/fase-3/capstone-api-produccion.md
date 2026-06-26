---
ejercicio_id: fase-3/capstone-api-produccion
fase: fase-3
sub_unidad: "3.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Capstone Fase 3: API de producción

## Aviso de uso para el corrector

Este capstone **no tiene una única respuesta correcta**: el alumno elige su dominio, su modelo y su
estructura. Lo de abajo es **un** proyecto ejemplar que alcanza el nivel `excelente` —una **vara de
medir**, no la solución a copiar—. **No exijas que el alumno haya hecho *este* dominio ni *estos*
nombres.** Evalúa su entrega contra la rúbrica (`.ai/rubricas/fase-3/capstone-api-produccion.md`) usando
este ejemplo solo para calibrar qué se ve como "producción".

> Lo esencial a verificar no es el dominio elegido, sino: **¿la spec y el ADR llegaron antes del código?
> ¿el dominio está desacoplado de FastAPI/SQLAlchemy? ¿el IDOR está cerrado en la query (con test)? ¿la
> idempotencia usa una clave persistida con índice único? ¿la guardia SSRF resuelve DNS y bloquea rangos
> internos? ¿los tests se miden con mutation score? ¿los secretos están fuera del repo y del historial?
> ¿puede defender cada decisión sin notas?** Un proyecto distinto que cumpla todo eso es igual de `excelente`.

---

## Proyecto ejemplar: `docubase` (base de conocimiento de documentos)

Usuarios con `colecciones` y `documentos`; import de documento desde una URL (superficie SSRF); encolado
de procesamiento (superficie idempotencia). Diseñado para que la Fase 6 lo vuelva un RAG añadiendo un
adapter `Indexador` sin tocar el dominio.

### 1. `SPEC.md` (antes del código)

Recursos, tabla de endpoints (verbo/auth/status/errores), contrato RFC 9457 y los casos de seguridad
(IDOR → 404 por dueño; URL interna → 400; reintento con misma `Idempotency-Key` → efecto una vez).
Equivalente a `plantillas/SPEC.md` completada. La spec se lee como la lista de tests.

### 2. ADR-0001 — ports & adapters

Decisión: dominio sin imports de frameworks; puertos `RepositorioDocumentos`, `ClienteHTTP`. Alternativa
descartada: CRUD acoplado (se paga en F6). Consecuencia clave: el RAG entra como adapter; el dominio se
testea con un repo en memoria. (Equivalente a `plantillas/ADR-0001-arquitectura-hexagonal.md`.)

### 3. Estructura

```text
src/
├── dominio/         # entidades + puertos (Protocol). CERO fastapi/sqlalchemy aquí.
├── casos_uso/       # importar_documento, listar_documentos, encolar_proceso
├── adapters/
│   ├── http/        # routers, deps (auth, sesión, paginación), errores RFC 9457
│   └── db/          # modelos SQLAlchemy 2.0 + repos que implementan los puertos
└── main.py          # app, lifespan, limiter, exception handlers, logging
```

### 4. Auth — hashing y JWT (APIs vigentes 2026, verificadas contra docs FastAPI)

```python
# adapters/http/seguridad.py
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from .config import settings  # pydantic-settings: lee SECRET_KEY, JWT_ALGORITHM, etc. de env

hasher = PasswordHash.recommended()  # argon2 por defecto

def hash_password(plano: str) -> str:
    return hasher.hash(plano)

def verificar_password(plano: str, hashed: str) -> bool:
    return hasher.verify(plano, hashed)   # NUNCA  plano == hashed

def crear_access_token(sub: str, scopes: list[str]) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": sub, "scopes": scopes, "exp": expira}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except InvalidTokenError as e:
        raise CredencialesInvalidas() from e   # excepción de dominio → handler la vuelve 401 RFC 9457
```

```python
# adapters/http/deps.py
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")

async def usuario_actual(token: Annotated[str, Depends(oauth2)]) -> Usuario:
    datos = decodificar_token(token)
    username = datos.get("sub")
    if username is None:
        raise CredencialesInvalidas()
    usuario = await repo_usuarios.por_username(username)
    if usuario is None:
        raise CredencialesInvalidas()
    return usuario

UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]
```

```python
# adapters/http/routers/auth.py
from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
@limiter.limit(settings.rate_limit_auth)   # slowapi: requiere el param `request: Request`
async def login(request: Request, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = await repo_usuarios.por_username(form.username)
    if usuario is None or not verificar_password(form.password, usuario.hashed_password):
        raise CredencialesInvalidas()   # → 401 RFC 9457 (no revela si el user existe)
    token = crear_access_token(usuario.username, scopes=form.scopes)
    return {"access_token": token, "token_type": "bearer"}
```

### 5. El IDOR cerrado en la query (la pieza que más se evalúa)

```python
# adapters/db/repo_documentos.py  (implementa el puerto RepositorioDocumentos)
from sqlalchemy import select
from sqlalchemy.orm import Session

class RepoDocumentosSQL:
    def __init__(self, sesion: Session) -> None:
        self._s = sesion

    def por_id_para_dueno(self, doc_id: int, owner_id: int) -> Documento | None:
        # El filtro por dueño va EN la query: el documento ajeno no existe para este usuario.
        stmt = select(DocumentoModel).where(
            DocumentoModel.id == doc_id,
            DocumentoModel.owner_id == owner_id,   # <- la defensa, no un if posterior
        )
        fila = self._s.scalars(stmt).first()
        return fila.a_entidad() if fila else None
```

```python
# adapters/http/routers/documentos.py
@router.get("/documentos/{doc_id}", response_model=DocumentoPublico)
async def obtener(doc_id: int, usuario: UsuarioActual, repo: RepoDep):
    doc = repo.por_id_para_dueno(doc_id, usuario.id)
    if doc is None:
        raise RecursoNoEncontrado("documento")   # 404 también para el ajeno (no filtra existencia)
    return doc
```

### 6. Guardia SSRF (reusa el ejercicio `blindar-fetch-ssrf`)

```python
# adapters/http/ssrf.py
import ipaddress, socket
from urllib.parse import urlparse

ESQUEMAS_OK = {"http", "https"}

def url_es_segura(url: str) -> bool:
    p = urlparse(url)
    if p.scheme not in ESQUEMAS_OK or not p.hostname:
        return False
    try:
        infos = socket.getaddrinfo(p.hostname, p.port or 80, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return False
    for *_, sockaddr in infos:           # revisa TODAS las IPs resueltas (anti DNS rebinding)
        ip = ipaddress.ip_address(sockaddr[0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False                 # bloquea 10/8, 127/8, 169.254/16 (metadata cloud), etc.
    return True
```

El cliente httpx hace el fetch con `follow_redirects=False` (o revalidando cada salto) y un `timeout`
explícito; el caso de uso llama a `url_es_segura` **antes** de tocar la red y lanza `UrlNoPermitida` → 400.

### 7. Idempotencia (reusa `disenar-pago-idempotente`)

```python
# tabla idempotency_keys: UNIQUE(key) — la unicidad la garantiza el índice, no un "consultar y luego insertar"
async def encolar_proceso(doc_id: int, usuario: Usuario, idem_key: str, repo, cola) -> Resultado:
    previo = repo.resultado_por_clave(idem_key, usuario.id)
    if previo is not None:
        return previo                    # reintento: devuelve el resultado guardado, NO reencola
    try:
        repo.reservar_clave(idem_key, usuario.id)   # INSERT; si choca con el índice único -> conflicto
    except ClaveDuplicada:               # carrera: otro request idéntico ganó
        return repo.resultado_por_clave(idem_key, usuario.id)
    resultado = cola.encolar(doc_id)     # el efecto ocurre UNA vez
    repo.guardar_resultado(idem_key, resultado)
    return resultado
```

### 8. Errores RFC 9457 (un handler por excepción de dominio)

```python
# main.py
from fastapi.responses import JSONResponse

def problema(status: int, title: str, detail: str, instance: str, tipo: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={"type": tipo, "title": title, "status": status, "detail": detail, "instance": instance},
    )

@app.exception_handler(RecursoNoEncontrado)
async def _no_encontrado(request, exc):
    return problema(404, "Recurso no encontrado", str(exc), request.url.path,
                    "https://docubase.example/errors/no-encontrado")

@app.exception_handler(CredencialesInvalidas)
async def _credenciales(request, exc):
    resp = problema(401, "Credenciales inválidas", "Token ausente o inválido", request.url.path,
                    "https://docubase.example/errors/credenciales")
    resp.headers["WWW-Authenticate"] = "Bearer"
    return resp
```

El `excelente` también mapea el 429 de slowapi a `application/problem+json` con un handler propio de
`RateLimitExceeded` (en vez del `_rate_limit_exceeded_handler` por defecto), para que el contrato de error
sea uniforme.

### 9. Observabilidad (logs + correlation ID)

Middleware que genera/propaga un `X-Request-ID`, lo mete en un `contextvar` y lo incluye en cada log JSON
(logging estructurado). En la demo se ve el mismo id en las líneas de un request que falla.

### 10. Migraciones, CI y secretos

- **Alembic:** `alembic revision --autogenerate -m "..."` revisado a mano (no a ciegas) y `alembic upgrade head`. El esquema vive en migraciones; nada de `create_all` en prod.
- **CI (`.github/workflows/ci.yml`):** `ruff check` → `pytest` → `mutmut run` (reporta score) → `gitleaks` → `pip-audit`. Falla el job si gitleaks encuentra un secreto.
- **Secretos:** `pydantic-settings` lee de env/`.env`; `.env` en `.gitignore`; `git log -p` limpio.

### 11. Tests medidos por mutation score

Contrato (`TestClient`): 422 de validación, 401 sin token, 404-RFC9457, **IDOR (A crea, B recibe 404)**,
409/200 de idempotencia en reintento, 400 de SSRF con `169.254.169.254`, 429 de rate limit. Dominio puro:
`encolar_proceso` con un repo en memoria que implementa el puerto (sin Postgres). `mutmut run` reporta un
score alto; los mutantes sobrevivientes se discuten en el write-up.

### 12. README (en inglés) + write-up de trade-offs

`docker compose up` → demo pegada (registro → token → crear colección → importar → 404 al doc ajeno → 429).
Write-up: *"Chose ports & adapters over a flat CRUD because Phase 6 will plug a RAG indexer as an adapter
without touching the domain. The hardest part was idempotency under concurrency: a 'check-then-insert'
had a race, so I rely on the UNIQUE index and handle the conflict. I left soft-deletes out on purpose."*

---

## Mapeo al Definition of Done (lo que el corrector verifica)

| Punto del DoD (§B) | Evidencia en el ejemplar | Aplica en F3 |
|---|---|---|
| **1. Spec + ADRs** | `SPEC.md` antes del 1er endpoint + ADR-0001 ports & adapters | ✅ Obligatorio |
| **2. Tests + lint en CI, mutation score** | contrato + dominio; `mutmut` reporta score; `ruff` en CI | ✅ Obligatorio |
| **3. Seguridad + SCA/secret-scan** | IDOR/Injection/SSRF con test; `gitleaks` + `pip-audit` en CI | ✅ Obligatorio |
| **4. Observabilidad** | logs JSON + correlation ID por request (OTel = stretch) | ✅ (logs+IDs) |
| **8. Demo + README inglés + write-up** | `docker compose up` + sesión pegada + trade-offs | ✅ Obligatorio |
| **9. Conventional Commits** | historial spec→ADR→migración→features→fix→docs | ✅ Obligatorio |
| 5. Eval harness (IA) | — no hay IA todavía | 🌱 semilla → F6 |
| 6. Validación/least-privilege de agente | — no hay agente | 🌱 semilla → F6/F7 |
| 7. a11y (WCAG) | — no hay UI; la API solo expone JSON | 🌱 semilla → F4 |

## Rango de soluciones aceptables (para no penalizar lo correcto)
- **Cualquier dominio** sirve si tiene las tres superficies (recurso con dueño, acción sensible, fetch saliente): gastos compartidos, reservas, acortador con cuotas, etc. No exigir `docubase`.
- **El hashing** puede ser `pwdlib` (recomendado hoy) o `bcrypt` directo; **el JWT**, `PyJWT` (estándar actual). Aceptar ambos si son correctos; marcar solo el texto plano o `==` sobre el hash.
- **Async o sync** es válido mientras sea coherente (no `async def` con cliente bloqueante dentro). Un backend totalmente síncrono bien hecho es aceptable en F3.
- **La idempotencia** puede vivir en una tabla propia o como columna; lo que importa es la **clave persistida con índice único** y el reintento que no repite el efecto. Un check sin índice (con carrera) es `en-progreso`, no `competente`.
- **El rate limiting** puede ser `slowapi`, un middleware propio o el del reverse proxy si está documentado. Lo que no se acepta es "no hay".
- **Otro stack** (Node/NestJS) es válido si cumple el mismo DoD: spec, ADR, migraciones, OAuth2/JWT, IDOR/Injection/SSRF cerrados, idempotencia, RFC 9457, tests medidos, secretos fuera, Conventional Commits. La Fase 3 marca FastAPI como troncal, pero el capstone evalúa el DoD, no el framework.
- Para el gate Primero-Sin-IA: lo decisivo es que **defienda su arquitectura y sus mitigaciones sin notas**. Un backend más simple pero entendido y honesto supera a uno sofisticado que no puede explicar.
