# Ejercicio 5.1 — Dockeriza el backend FastAPI (multi-stage, seguro y mínimo)

> **Modalidad: código (sin IA primero).** Vas a escribir un `Dockerfile` de **producción** real para una app FastAPI. No copies a ciegas el de la lección: reconstrúyelo razonando cada decisión. Si no puedes defender por qué pusiste una línea, todavía no la aprendiste.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** [`5.1` Docker a fondo](/fase-5-devops/5-1-docker/)
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Implementar un `Dockerfile` **multi-stage** y un `.dockerignore` para un backend FastAPI, con caché de capas correcta, imagen base mínima y pinneada, usuario no-root y `HEALTHCHECK` — defendiendo cada decisión.

## 📋 Contexto

Esta imagen es la **primera entrega del [Capstone F5](/fase-5-devops/proyecto/)**: la pieza que el CI/CD ([`5.3`](/fase-5-devops/5-3-cicd-github-actions/)) construirá y los gates de seguridad ([`5.4`](/fase-5-devops/5-4-seguridad-supply-chain-ci/)) escanearán. Una imagen mínima y reproducible ahorra costo y reduce riesgo aguas abajo.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (40 min). Está bien que sea lento.
2. Solo entonces consulta **documentación oficial** (Docker, FastAPI).
3. **Solo al final** usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe el Dockerfile de memoria**. Si no puedes, no lo aprendiste.

## 🛠️ Instrucciones

Te damos: `app/main.py` (FastAPI con `/health`), `requirements.txt`, un `Dockerfile` vacío y un `.dockerignore` vacío.

Escribe un `Dockerfile` que:

1. Sea **multi-stage**: una etapa `builder` que instala dependencias y una `runtime` mínima que solo copia lo necesario.
2. Use una base **pinneada y slim** (nada de `latest`; por ejemplo `python:3.13-slim`).
3. Ordene las instrucciones para **aprovechar la caché de capas**: el manifiesto de dependencias (`requirements.txt`) se copia e instala **antes** de copiar el código de `app/`.
4. Corra como **usuario no-root** (crea un usuario de sistema y usa `USER`).
5. Incluya un **`HEALTHCHECK`** que golpee `/health` **sin depender de `curl`** (la imagen slim no lo trae).
6. `EXPOSE` el puerto 8000 y defina un `CMD` que arranque la app (`fastapi run app/main.py --port 8000`).

Escribe un `.dockerignore` que excluya, como mínimo: `.git`, `.env` y `.env.*`, `__pycache__`, `*.pyc`, `.venv` y `tests/`.

Corre el linter:

```bash
uv run pytest test_dockerfile.py        # o simplemente: pytest test_dockerfile.py
```

El linter es **estático** (no necesita Docker instalado): lee tu `Dockerfile` y tu `.dockerignore` y verifica las buenas prácticas. Pasarlo es el **piso**, no la meta: un linter no entiende si tu razonamiento es correcto.

> Si tienes Docker instalado y quieres ir más allá: `docker build -t miapp .` y luego `docker images` para ver el tamaño. Anótalo en `notas.md`. No es obligatorio para "hecho".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest test_dockerfile.py` pasa en **verde**.
- [ ] El `Dockerfile` no hornea **ningún secreto** (ningún `ENV` con contraseña/clave literal).
- [ ] `notas.md` (5–8 líneas) responde: **¿por qué multi-stage reduce tamaño Y mejora seguridad a la vez?** y **¿qué capa se invalida si cambias `app/main.py`, y cuál NO?** — con tus palabras.
- [ ] Puedes explicar **sin notas** la diferencia entre imagen y contenedor, y por qué `EXPOSE` no publica el puerto.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-5/dockerizar-fastapi/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-5/dockerizar-fastapi.md` — no la mires antes de intentarlo de verdad.
