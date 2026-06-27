---
ejercicio_id: fase-5/dockerizar-fastapi
fase: fase-5
sub_unidad: "5.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md`). Hay un **rango** de soluciones válidas; lo que importa es que las decisiones estén justificadas, no que el archivo sea idéntico a este.

# Solución de referencia — Dockeriza el backend FastAPI

## `Dockerfile` canónico

```dockerfile
# ---------- Etapa 1: builder ----------
FROM python:3.13-slim AS builder

# uv: instalador de paquetes rápido. Se queda en el builder, no en la imagen final.
RUN pip install --no-cache-dir uv

WORKDIR /app

# Manifiesto primero (cambia poco) -> la capa de instalación se cachea
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache -r requirements.txt

# ---------- Etapa 2: runtime ----------
FROM python:3.13-slim AS runtime

# Usuario sin privilegios (defensa en profundidad)
RUN groupadd --system app && useradd --system --gid app --no-create-home appuser

# Copia SOLO el venv ya construido: nada de uv, gcc ni headers llega al runtime
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
# El código (cambia mucho) va al final: su cambio no invalida la instalación
COPY ./app ./app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').getcode()==200 else 1)"

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
```

## `.dockerignore` canónico

```text
.git
.gitignore
.venv
__pycache__/
*.pyc
.env
.env.*
tests/
*.md
.pytest_cache/
```

## Por qué cada decisión (lo que el `notas.md` debería capturar)

1. **Multi-stage reduce tamaño Y seguridad a la vez.** El builder trae `uv` y, al instalar, puede tirar de compiladores/headers. El runtime parte de una base slim limpia y solo recibe el venv (`COPY --from=builder /opt/venv`). Resultado: imagen más pequeña (menos costo de transferencia/CI, arranque más rápido) **y** menos software instalado = menos superficie de ataque / menos CVEs que escanear. Un solo patrón ataca ambos frentes.
2. **Orden de capas = caché.** Cada instrucción es una capa (un diff apilado). Docker reusa una capa si ella y todo lo de arriba no cambió. Al copiar `requirements.txt` e instalar **antes** de `COPY ./app ./app`: si cambias `app/main.py`, se invalida la capa `COPY ./app ./app` y las de abajo, pero **NO** la capa `RUN uv pip install` (porque `requirements.txt` no cambió). La instalación de dependencias —lo lento— se reutiliza.
   - Capa que se invalida al tocar `app/main.py`: la del `COPY ./app ./app` (y el `CMD`, que es trivial).
   - Capa que NO se invalida: la del `RUN uv pip install -r requirements.txt`.
3. **`python:3.13-slim` pinneado, no `latest`.** Reproducibilidad: dos builds del mismo Dockerfile deben dar el mismo entorno. `latest` rompe eso.
4. **No-root.** Si la app es comprometida, no ser root dentro del contenedor frena el escalamiento hacia el host.
5. **HEALTHCHECK con `python -c` + urllib.** La base slim no trae `curl`; instalarlo solo para esto sumaría peso y superficie. Python ya está, así que golpeamos `/health` con la stdlib.
6. **`.dockerignore`.** Sin él, `COPY` arrastra `.git`, `.venv`, `__pycache__` y —lo grave— `.env` con secretos, que quedarían en una capa permanente (visible con `docker history`).
7. **`CMD` en *exec form*** (lista JSON): el proceso recibe señales (SIGTERM) directamente, para un apagado limpio. La *shell form* lo envolvería en `/bin/sh -c` y rompería el manejo de señales.

## Rango de soluciones aceptables
- **`pip` en vez de `uv`** en el builder es válido (`RUN pip install --no-cache-dir -r requirements.txt`), solo más lento; el patrón de capas es lo evaluado.
- **Otra forma de aislar lo instalado** (p. ej. `uv pip install --target /install` + `ENV PYTHONPATH`, o copiar `site-packages`) cuenta como `competente` si el runtime no carga el toolchain de build.
- **`distroless`** como runtime es válido y más estricto (`excelente`), aunque obliga a otro enfoque para el healthcheck.
- **`python:3.12-slim`** u otra menor reciente es aceptable; lo que no se acepta es `latest` ni la imagen completa (no-slim) sin justificación.
- El healthcheck puede usar `wget` si lo instala explícitamente, o un script propio; lo que se marca mal es `curl` sobre slim sin instalarlo.
- Para los objetivos del ejercicio, lo esencial es: multi-stage real, orden de capas correcto, no-root, base pinneada/slim, healthcheck funcional, `.dockerignore` que excluye `.env`. Cómo se llega a eso admite variantes.
