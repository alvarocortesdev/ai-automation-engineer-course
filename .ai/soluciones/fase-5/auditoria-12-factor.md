---
ejercicio_id: fase-5/auditoria-12-factor
fase: fase-5
sub_unidad: "5.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es un ejercicio de **diagnóstico**: úsala para evaluar la auditoría de `auditoria.md`, no como "la única respuesta" (la redacción del arreglo admite variantes).

# Solución de referencia — Auditoría 12-factor de un backend

## Tabla de violaciones (referencia completa)

| # | Dónde | Factor | Síntoma observable en producción | Arreglo |
|---|---|---|---|---|
| V1 | `app.py`: `DATABASE_URL`, `STRIPE_API_KEY`, `PORT` literales | **III — Config** | La misma imagen no se puede apuntar a otra base/clave sin reconstruir; prod usa la base/clave de dev. | Leer de variables de entorno (`pydantic-settings`, `env_prefix="APP_"`). |
| V2 | `Dockerfile`: `ENV STRIPE_API_KEY=sk_live_...` | **III + seguridad** | El secreto **queda en una capa** de la imagen; cualquiera con la imagen lo extrae (`docker history`). Filtración irreversible. | Quitar el `ENV`; inyectar en runtime (`-e`/`environment:`/secret del runner). Rotar la clave filtrada. |
| V3 | `app.py`: `SESSIONS`, `CARRITOS` en memoria | **VI — Processes (stateless)** | Al **reiniciar/redeploy** el contenedor, todos los usuarios se desloguean y pierden su carrito; con **dos réplicas**, el login en la réplica 1 da 401 intermitente en la 2. | Mover el estado a un backing service compartido (Redis para sesión, DB para carrito). |
| V4 | `app.py`: `logging.basicConfig(filename="/var/log/...")` | **XI — Logs** | El archivo muere con el contenedor; con N réplicas hay N archivos huérfanos; puede llenar el disco. Nadie agrega los logs. | Escribir a **stdout** (`stream=sys.stdout`); el entorno los rutea/agrega (alimenta `5.10`). |
| V5 | `app.py`: `uvicorn.run(..., port=PORT)` con `PORT` fijo | **VII — Port binding** | El entorno no puede decidir en qué puerto exponer la app; choca al mapear o al correr varias. | Leer el puerto de config (`--port $APP_PORT`) y dejar que el entorno mapee. |
| V6 | comentarios de `app.py`/`compose.yaml`: SQLite en dev, Postgres en prod | **X — Dev/prod parity** | SQL que SQLite tolera revienta en Postgres en prod; "pasó en mi máquina" no predice prod. | Usar Postgres también en dev (Compose levanta el mismo Postgres). |
| V7 | `Dockerfile`: `pip install fastapi uvicorn psycopg2 stripe` | **II — Dependencies** (bonus) | Sin versiones pinneadas ni lockfile, dos builds traen versiones distintas → "funcionaba ayer". | Pinear con lockfile (`uv.lock`/`requirements.txt` con hashes); `uv sync`/`pip install -r`. |
| V8 | (matiz) la URL de la base atada al código | **IV — Backing services** (se solapa con III) | La base no es un recurso adjunto intercambiable: cambiar de Postgres local a gestionado exige tocar código. | La URL viene de config; cambiar de base = cambiar una variable, cero código. |

> Mínimo para **competente**: V1, V2, V3, V4, V5, V6 con el factor correcto. V7 y el matiz IV (V8) elevan a **excelente**.

## ADR de referencia (prioridad)

**Primero el secreto horneado (V2), luego el del código (V1).** Criterio: el riesgo de seguridad de una clave de pago filtrada es **irreversible** (alguien puede haberla copiado ya; hay que **rotarla**, no solo moverla) y de impacto directo en plata. Los demás (estado en memoria, logs, puerto) son riesgos **operativos recuperables**: duelen, pero no filtran credenciales. Orden sugerido: V2/V1 (seguridad) → V3 (estado, bloquea el escalado y el redeploy) → V4 (logs, habilita operar) → V6/V5/V7 (paridad, puerto, deps).

## Defensa de referencia
- **Secreto en imagen vs variable de entorno:** la imagen es un artefacto **distribuible e inmutable**; el secreto queda en una capa visible para cualquiera que tenga la imagen (`docker history`, registries). Una variable de entorno se inyecta en runtime, no se distribuye con el artefacto y se puede rotar sin reconstruir.
- **Qué factor habilita el escalado:** el **VI (procesos sin estado)**. Solo si nada importante vive en la memoria de un proceso puedes lanzar N réplicas idénticas (Factor VIII) detrás de un balanceador. Este backend NO escala hoy porque la sesión y el carrito viven en `dict` del proceso: dos réplicas verían usuarios distintos.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Síntomas genéricos** ("es inseguro") en vez de observables ("queda en `docker history`").
2. **Olvidar V2** (secreto en la imagen) cazando solo V1 (secreto en el código): son dos violaciones, V2 es igual de grave.
3. **Confundir III/IV** o **VI/VIII** (ver rúbrica).
4. **Olvidar la paridad (V6):** la pista está en los comentarios; premia a quien los leyó.
5. **ADR sin postura:** "depende" no es priorizar; debe comprometer un orden y justificarlo por riesgo.

## Rango de soluciones aceptables
- Numerar/agrupar distinto (p. ej. fusionar V1+V8 bajo "config y backing services") — válido si nombra ambos factores.
- Proponer un **gestor de secretos** (Vault, secrets de la nube) en vez de variables de entorno planas para V2 — es una mejora, márcalo excelente.
- Priorizar V3 antes que V1 argumentando que el repo aún no es público — defendible si lo justifica; la referencia prioriza seguridad, pero un trade-off bien razonado es aceptable.
- ❌ **No aceptable como competente:** menos de 6 violaciones; factores mal asignados; arreglos del tipo "migrar a Kubernetes"; ADR sin criterio.
