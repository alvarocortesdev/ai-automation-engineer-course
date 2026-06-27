---
ejercicio_id: fase-5/config-en-entorno
fase: fase-5
sub_unidad: "5.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Config en el entorno (Factor III)

## Implementación canónica (`settings.py`)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")

    database_url: str          # requerido: sin default
    api_key: str               # requerido: sin default
    debug: bool = False        # opcional, default seguro
    port: int = 8000           # opcional


def get_settings() -> Settings:
    return Settings()          # instancia fresca: lee el entorno actual cada vez
```

Verificado contra `test_settings.py`: pasa los seis casos (lee requeridos; `port` default e desde entorno como `int`; `debug` parsea `"true"/"1"/"false"/"0"`; falta de un requerido lanza `ValidationError`; entorno vacío también lanza).

## Por qué funciona

- **`env_prefix="APP_"`** hace que `database_url` se lea de `APP_DATABASE_URL`, etc. Sin el prefijo, leería `DATABASE_URL` y los tests (que definen `APP_*`) fallarían.
- **Campo sin `=` (sin default) = requerido.** `Settings()` lee del entorno al instanciar; si un requerido falta, `pydantic` lanza `ValidationError` **al arrancar** (fail-fast). Es lo que verifican los dos tests de "falta requerido" y "entorno vacío".
- **`debug: bool` y `port: int`** aprovechan la coerción de tipos de pydantic: `"true"/"1"` → `True`, `"9000"` → `9000` (int). El alumno no parsea a mano.
- **`get_settings()` devuelve una instancia nueva** en cada llamada. Si cacheara (`lru_cache`), los tests que cambian el entorno entre llamadas verían el valor viejo. En una app real se cachea; en este ejercicio NO, y el alumno debería notarlo.
- **`env_file=".env"`** es la comodidad de dev; en prod no se envía `.env` y las variables reales tienen prioridad sobre él.

## El recorrido de razonamiento esperado (bitácora)
1. **Config** es lo que varía entre deploys (URL de base, clave de API) + secretos; **no-config** es lo invariable (nombre de la app, rutas de routing, mapeo de errores).
2. Un `.env` **commiteado** mete secretos en el repo: cualquiera que clone los obtiene. El `.env` va en `.gitignore`; se commitea un `.env.example` con las llaves sin valores.
3. Un requerido-sin-default falla **ruidoso y temprano** (en el deploy, con error claro); un default vacío falla **silencioso y tarde** (bajo carga, cuando alguien pega el endpoint).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Default inseguro** a un secreto: descalifica C2 como competente; el test del entorno vacío debería cazarlo (no lanzaría).
2. **`os.environ` a mano** sin pydantic: pierde tipos y fail-fast; aceptable solo si replica ambos (improbable y feo).
3. **`lru_cache` en `get_settings()`**: rompe los tests de `port`/`debug` desde entorno.
4. **`env_prefix` ausente o equivocado**: lee variables sin el `APP_`.
5. **Tipos como string**: `port` quedando `"8000"` en vez de `8000`.

## Rango de soluciones aceptables
- **`Field(...)` explícito** para los requeridos (`database_url: str = Field(...)`) — equivalente a no poner default.
- **`validation_alias`/`AliasChoices`** para nombres de variable alternativos — válido si los tests siguen pasando (definen `APP_*`).
- **`get_settings()` con `lru_cache` PERO los tests limpiando la caché** — válido solo si el alumno ajustó los tests y lo justificó; con los tests dados tal cual, debe ser instancia fresca.
- ❌ **No aceptable como competente:** secreto/Default en el código; leer sin `pydantic-settings` perdiendo el fail-fast; `port`/`debug` sin coerción de tipo.
