---
ejercicio_id: fase-5/compose-app-postgres-redis
fase: fase-5
sub_unidad: "5.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md`). Hay un **rango** de soluciones válidas; lo importante es que el orquestado y los secretos estén bien razonados, no que el YAML sea idéntico.

# Solución de referencia — Stack app + Postgres + Redis

## `compose.yaml` canónico

```yaml
name: miapp

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: "postgresql://app:${POSTGRES_PASSWORD}@db:5432/appdb"
      REDIS_URL: "redis://cache:6379/0"
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:17
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  cache:
    image: redis:7
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
```

## `.env.example` canónico

```text
# Copiar a .env (que va al .gitignore) y poner un valor fuerte.
POSTGRES_PASSWORD=cambia-esto-en-tu-.env
```

## Por qué cada decisión (lo que el `notas.md` debería capturar)

1. **Sin `version:`.** En Compose moderno el campo es obsoleto; ponerlo genera una advertencia. El archivo arranca en `services`.
2. **`depends_on: [db]` corto NO basta.** La forma corta solo espera a que el *contenedor* de Postgres arranque (proceso creado), no a que Postgres esté *listo para aceptar conexiones* —que tarda un par de segundos extra de inicialización. Sin el health gate, la api arranca antes, intenta `connect()`, falla y muere: una **race condition** que a veces gana y a veces no. La forma larga con `condition: service_healthy` + un `healthcheck` que use `pg_isready` hace que la api espere a que la dependencia esté **sana**.
3. **DNS interno por nombre de servicio.** Compose crea una red por defecto y conecta los tres servicios. Dentro de esa red, el **nombre del servicio es el hostname**: `db` resuelve a la IP del contenedor de Postgres, `cache` a la de Redis. Por eso la `DATABASE_URL` dice `@db:5432` y no una IP. Nadie configura IPs: lo hace el DNS embebido de Docker. Nota: los puertos internos (5432, 6379) no necesitan publicarse al host para que los servicios se hablen; solo se publica (`ports`) lo que el exterior consume (la api en 8000).
4. **Named volume para Postgres.** `pgdata:/var/lib/postgresql/data` persiste los datos fuera del ciclo de vida del contenedor; sin él, recrear el contenedor borra la base. Declarado a nivel raíz en `volumes:`.
5. **Secreto por `${POSTGRES_PASSWORD}`.** Compose lee la variable de `.env` (o del entorno). La contraseña **no** está escrita en `compose.yaml`, que sí va al repo. `.env` va al `.gitignore`; `.env.example` documenta qué variables hace falta, sin el valor real.
6. **Imágenes pinneadas** (`postgres:17`, `redis:7`): reproducibilidad. `latest` rompería el "corre igual en cualquier máquina".

## Rango de soluciones aceptables
- **`valkey/valkey:8`** en vez de `redis:7` es válido (y más correcto en producción por la licencia); el healthcheck sigue siendo `redis-cli ping` (Valkey lo provee).
- **`env_file:` o el bloque `secrets:`** de Compose en vez de `environment` para el secreto cuenta como `excelente`.
- Intervalos/`retries`/`start_period` distintos son aceptables si son razonables (no `interval: 1s` agresivo, no healthcheck trivial `["CMD","true"]`).
- Versiones mayores distintas pero pinneadas (`postgres:16`, `redis:7.4`) son válidas; lo que no se acepta es `latest`.
- Un `networks:` explícito y nombrado es válido (más control), aunque la red por defecto basta para este ejercicio.
- Lo esencial evaluado: sin `version`, healthchecks reales en db y cache, `service_healthy`, hostnames por nombre de servicio, named volume para la DB, contraseña por variable de entorno. Las variantes alrededor de eso son aceptables.
