# Ejercicio 5.1 — Compón el stack: app + Postgres + Redis con health gates

> **Modalidad: código (sin IA primero).** Vas a escribir un `compose.yaml` real que orquesta tres servicios. La gracia no es la sintaxis YAML: es entender las **redes**, el **orden de arranque** y el **manejo de secretos**. Si no puedes defender por qué cada bloque está ahí, todavía no lo aprendiste.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** [`5.1` Docker a fondo](/fase-5-devops/5-1-docker/)
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Componer un stack multi-servicio (app FastAPI + Postgres + Redis) con Docker Compose: red por defecto y descubrimiento por nombre de servicio, named volume para persistencia, variables de entorno para configuración y secretos, y orden de arranque con `depends_on: condition: service_healthy`.

## 📋 Contexto

Este `compose.yaml` es la otra mitad de la primera entrega del [Capstone F5](/fase-5-devops/proyecto/): junto con el `Dockerfile`, define el stack local reproducible que luego desplegarás ([`5.9`](/fase-5-devops/5-9-despliegue/)) e instrumentarás ([`5.10`](/fase-5-devops/5-10-observabilidad/)).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (40 min).
2. Solo entonces consulta la **documentación oficial** de Compose.
3. **Solo al final** usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe el compose.yaml de memoria**. Si no puedes, no lo aprendiste.

## 🛠️ Instrucciones

Te damos un `compose.yaml` esqueleto con TODOs y un `.env.example`. Complétalo para que levante tres servicios bien orquestados:

1. **Sin** campo `version:` arriba (es obsoleto; Compose lo ignora y advierte).
2. El servicio `api` se construye con `build: .`; `db` y `cache` usan imágenes **pinneadas** (no `latest`).
3. `db` y `cache` tienen **`healthcheck`** (Postgres con `pg_isready`, Redis con `redis-cli ping`).
4. La `api` usa **`depends_on` con `condition: service_healthy`** para esperar a que ambos estén sanos.
5. La `api` alcanza la DB y el cache **por nombre de servicio** (`db`, `cache`) en sus URLs de entorno, no por IP.
6. Postgres persiste sus datos en un **named volume** declarado a nivel raíz.
7. La contraseña de Postgres entra por **`${POSTGRES_PASSWORD}`** (de `.env`), nunca escrita en el archivo. Documenta la variable en `.env.example` (sin un valor real secreto).

Corre el linter:

```bash
uv run pytest test_compose.py        # o simplemente: pytest test_compose.py
```

El linter es **estático** (no necesita Docker): lee tu `compose.yaml` y tu `.env.example`. Pasarlo es el **piso**, no la meta.

> Si tienes Docker: `docker compose config` valida la sintaxis y `docker compose up --build` levanta el stack. No es obligatorio para "hecho".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest test_compose.py` pasa en **verde**.
- [ ] La contraseña **no aparece en texto plano** en `compose.yaml`; `.env` está pensado para ir al `.gitignore`.
- [ ] `notas.md` (5–8 líneas) responde: **¿por qué `depends_on: [db]` (forma corta) no basta?** y **¿cómo resuelve la `api` el hostname `db` sin que tú configures ninguna IP?** — con tus palabras.
- [ ] Puedes explicar **sin notas** la diferencia entre un named volume y un bind mount, y cuándo usar cada uno.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-5/compose-app-postgres-redis/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-5/compose-app-postgres-redis.md` — no la mires antes de intentarlo de verdad.
