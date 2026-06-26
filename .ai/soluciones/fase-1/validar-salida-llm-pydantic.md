---
ejercicio_id: fase-1/validar-salida-llm-pydantic
fase: fase-1
sub_unidad: "1.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Validar la salida de un LLM con pydantic

## Respuesta canónica

```python
from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Compra(BaseModel):
    model_config = ConfigDict(extra="forbid")   # campo alucinado => ValidationError

    comercio: str = Field(min_length=1)
    monto: int = Field(gt=0)                      # CLP, entero positivo
    categoria: str = Field(min_length=1)
    fecha: date                                   # pydantic parsea la cadena ISO "YYYY-MM-DD"
    items: list[str] = Field(min_length=1)        # al menos un item

    @field_validator("comercio", "categoria")
    @classmethod
    def sin_espacios_sobrantes(cls, v: str) -> str:
        limpio = v.strip()
        if not limpio:                            # "   " pasa min_length pero está vacío
            raise ValueError("no puede ser vacío ni de solo espacios")
        return limpio                             # devuelve el valor ya normalizado


def parsear_compra(raw_json: str) -> Compra:
    return Compra.model_validate_json(raw_json)   # parsea JSON Y valida en un paso
```

Con esto pasan los 9 tests.

## Razonamiento paso a paso

1. **Tipos + constraints declarativas.** `monto: int = Field(gt=0)`, `items: list[str] = Field(min_length=1)`, `comercio`/`categoria` con `Field(min_length=1)`. En modo lax (el default), pydantic **coacciona** `"12990"` → `12990` y la cadena ISO → `date`. Eso cubre la coacción y casi todos los rechazos (monto ≤ 0, lista vacía, fecha inválida, string de largo 0).
2. **Lo que las constraints NO cubren.** `min_length=1` cuenta caracteres, no contenido útil: `"   "` (tres espacios) tiene largo 3 y pasa. Un LLM perfectamente devuelve eso. El `@field_validator("comercio", "categoria")` —`mode="after"` por defecto, corre tras la coacción de tipo— hace `strip`, lanza `ValueError` si queda vacío (pydantic lo envuelve como `ValidationError`) y **devuelve el valor normalizado** para que el objeto quede limpio.
3. **Cerrar la puerta a lo alucinado.** Por defecto pydantic **ignora** los campos extra. Para datos no confiables eso es peligroso: el LLM inventa `"confianza": 0.99` y se cuela en silencio. `model_config = ConfigDict(extra="forbid")` convierte ese campo extra en un `ValidationError`. Es el principio de "fallar ruidoso" en la frontera.
4. **Un solo paso.** `model_validate_json` parsea el string JSON **y** valida; evita el `json.loads` separado (dos pasos = doble superficie de error y un dict intermedio sin tipar).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Falta `extra="forbid"`** → `test_campo_alucinado` falla. Es el corazón del hilo de seguridad de IA (LLM05 Improper Output Handling): confiar en la salida del modelo.
2. **Creer que `min_length` cubre los espacios** → `test_comercio_solo_espacios` falla. Necesita el validador con `strip`.
3. **Sintaxis v1**: `@validator`, `.parse_raw()`, `.dict()`, `class Config: extra = "forbid"`. Funciona a medias o lanza deprecation/errores. La v2 es la de arriba.
4. **`@field_validator` sin `@classmethod`** o con los decoradores invertidos → `PydanticUserError` de configuración.
5. **Validador que no hace `return`** → el campo queda `None` y rompe el caso válido.
6. **Parsear y validar por separado** (`Compra(**json.loads(raw))`) cuando `model_validate_json` lo hace en uno.

## Rango de soluciones aceptables
- **Validador de espacios**: aceptar dos validadores separados (uno por campo) en vez de uno compartido; o resolverlo con `Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]` (pydantic v2) — equivalente y `excelente` si el alumno lo justifica. Lo esencial es que `"   "` sea rechazado y que el valor quede normalizado.
- **`monto`**: usar `PositiveInt` en lugar de `int = Field(gt=0)` es equivalente y válido.
- **`categoria`**: si el alumno la modela como `Literal[...]` o un `Enum` de categorías conocidas, es **más** estricto y cuenta como `excelente` (siempre que los tests sigan pasando con "supermercado").
- **Rechazo de extra**: `model_config = ConfigDict(extra="forbid")` o, equivalente, `@field_validator` no aplica aquí; debe ser config del modelo. Aceptar también `extra="forbid"` vía `class-level` config dict.
- **Test propio**: cualquiera de monto float `"12990.5"` (en modo lax pydantic lo rechaza para `int` salvo que sea entero exacto), item vacío en la lista, o campo faltante, cuenta para `excelente`.
- **`parsear_compra`**: aceptable también `Compra.model_validate(json.loads(raw_json))`, pero señalar que `model_validate_json` es preferible (un paso). No aceptable: construir el modelo sin validar o capturar y silenciar el `ValidationError`.
