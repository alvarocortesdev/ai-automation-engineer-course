"""Factor III — Config en el entorno (Primero-Sin-IA).

PUNTO DE PARTIDA con el ANTIPATRÓN: la config está hardcodeada en el código
(URL de base de datos, clave de API y puerto). Eso viola el Factor III de
12-factor: lo que varía entre deploys (y los secretos) NO puede vivir en el
código ni horneado en la imagen.

TU TAREA: refactoriza esto a una clase `Settings` de `pydantic-settings` que
lea del entorno con prefijo `APP_`, valide tipos y FALLE AL ARRANCAR si falta
un requerido. Implementa `get_settings()` para que devuelva una instancia
fresca (los tests manipulan el entorno y no deben chocar con una caché).

Necesitas el paquete pydantic-settings:
    uv add pydantic-settings        # o:  pip install pydantic-settings

Corre el test:
    uv run pytest        # o:  pytest

Anota en bitacora.md qué es config y qué no (con un ejemplo de cada uno de tu
propio proyecto) y por qué un .env commiteado rompe el Factor III.
"""

# ──────────────────────────────────────────────────────────────────────────
# ANTIPATRÓN (lo que vas a ELIMINAR al refactorizar). Déjalo como referencia
# mental de qué NO hacer; la solución no debe contener ninguna de estas líneas.
#
#   DATABASE_URL = "postgresql://admin:s3cr3t@localhost:5432/tienda"  # config + secreto en el código
#   API_KEY = "sk_live_51Hxxxx_CLAVE_REAL"                            # secreto horneado en la imagen
#   PORT = 8000                                                       # puerto fijo en el código
#   DEBUG = True
# ──────────────────────────────────────────────────────────────────────────

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Config leída del entorno (variables con prefijo APP_).

    Contrato que los tests esperan:
      - database_url: str  -> REQUERIDO (sin default). Si falta -> ValidationError.
      - api_key:      str  -> REQUERIDO (sin default). Si falta -> ValidationError.
      - debug:        bool -> opcional, default False (parsea "true"/"1"/"yes").
      - port:         int  -> opcional, default 8000.

    Variables de entorno: APP_DATABASE_URL, APP_API_KEY, APP_DEBUG, APP_PORT.
    PROHIBIDO darle un default (vacío o no) a database_url y api_key: un secreto
    con default convierte un fallo ruidoso y temprano en uno silencioso y tardío.
    """

    # TODO(1): configura model_config con env_prefix="APP_" (y env_file=".env"
    #          para la comodidad de dev local).
    # TODO(2): declara database_url y api_key como requeridos (sin '=').
    # TODO(3): declara debug y port como opcionales con sus defaults.
    #
    # (Esta clase aún no tiene campos: impleméntalos. Mientras tanto, get_settings()
    #  abajo lanza NotImplementedError y los tests fallan en rojo, como debe ser.)


def get_settings() -> "Settings":
    """Devuelve una instancia FRESCA de Settings (lee el entorno actual).

    Una instancia nueva por llamada hace los tests deterministas cuando ellos
    cambian las variables de entorno. En una app real podrías cachear con
    functools.lru_cache; aquí NO caches para no enmascarar cambios del entorno.
    """
    raise NotImplementedError("Devuelve Settings() leyendo el entorno actual.")


if __name__ == "__main__":
    # Prueba manual (Predict-Run): exporta las variables y corre este archivo.
    #   APP_DATABASE_URL=postgresql://localhost/db APP_API_KEY=k python settings.py
    # ¿Qué crees que pasa si NO exportas APP_API_KEY antes de correrlo?
    print(get_settings().model_dump())
