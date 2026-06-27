---
ejercicio_id: fase-6/validacion-tool-args
fase: fase-6
sub_unidad: "6.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**: el alumno debe corregir su trabajo, no recibir este código. Úsala para
> detectar el error y graduar las pistas.

# Solución de referencia — Gate de validación de argumentos de una tool

## Respuesta canónica (implementación)

```python
from __future__ import annotations
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

TECHO_REEMBOLSO_CLP = 200_000
ALLOWLIST = {"buscar_pedido", "reembolsar"}


@dataclass
class Decision:
    accion: str
    motivo: str


class ArgsBuscarPedido(BaseModel):
    model_config = ConfigDict(extra="forbid")   # rechaza args no pedidos (nivel excelente)
    pedido_id: int

    @field_validator("pedido_id")
    @classmethod
    def _pid_positivo(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("pedido_id debe ser positivo")
        return v


class ArgsReembolsar(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pedido_id: int
    monto_clp: int

    @field_validator("pedido_id")
    @classmethod
    def _pid_positivo(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("pedido_id debe ser positivo")
        return v

    @field_validator("monto_clp")
    @classmethod
    def _monto_positivo(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("monto_clp debe ser positivo")
        return v


MODELOS = {"buscar_pedido": ArgsBuscarPedido, "reembolsar": ArgsReembolsar}


def decidir(nombre: str, argumentos: dict) -> Decision:
    # Capa 1 — permiso: si no está permitida, ni miramos los argumentos.
    if nombre not in ALLOWLIST:
        return Decision("RECHAZAR", f"tool no permitida: {nombre}")

    # Capa 2 — forma: pydantic valida tipos, requeridos y positivos.
    try:
        args = MODELOS[nombre].model_validate(argumentos)
    except ValidationError as e:
        return Decision("RECHAZAR", f"argumentos inválidos: {e.errors()[0]['msg']}")

    # Capa 3 — semántica/negocio: la acción irreversible cara necesita un humano.
    if nombre == "reembolsar" and args.monto_clp > TECHO_REEMBOLSO_CLP:
        return Decision("CONFIRMAR", "reembolso sobre el techo: requiere humano")

    return Decision("EJECUTAR", "ok")
```

Verificado contra `test_gate.py`: **11 passed** (pydantic 2.x).

## Razonamiento paso a paso

El gate son **tres murallas en orden estricto**, y el orden es por seguridad:

1. **Permiso primero.** Si la tool no está en la allowlist, se rechaza **sin tocar
   sus argumentos**. No quieres correr validación —ni nada— sobre una llamada que no
   deberías considerar. Es least privilege puro: el universo de acciones posibles es
   un conjunto cerrado y pequeño.
2. **Forma después.** Recién cuando la tool es legítima, pydantic valida sus
   argumentos: tipos correctos, campos requeridos presentes, valores positivos. Un
   `pedido_id` de `"abc"` o un `monto_clp` ausente caen aquí. Se atrapa
   `ValidationError` (no `Exception` genérica).
3. **Semántica al final.** La forma válida no autoriza a ejecutar. La regla de
   negocio —techo de 200 000— decide entre `EJECUTAR` (auto) y `CONFIRMAR` (HITL). El
   modelo no conoce ni le importa esa política; la pones tú.

El punto pedagógico que el corrector debe verificar que el alumno **entiende**: el
modelo solo **pidió** la llamada. Entre "pidió" y "ejecuté" está este gate, que es el
único lugar donde tu sistema decide. `strict`/pydantic dan la **forma**; el gate da la
**decisión**.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Orden de las capas.** El error #1 es validar la forma antes de chequear la
   allowlist. Si el `decidir` empieza con `model_validate`, falla en seguridad aunque
   los tests "verde" por casualidad (los tests de allowlist usan tools sin modelo, así
   que un `MODELOS[nombre]` antes del chequeo lanzaría `KeyError`, no `RECHAZAR`).
2. **Frontera del techo.** `> TECHO` (no `>=`): 200 000 exacto debe `EJECUTAR`. El
   test `test_reembolso_justo_en_el_techo_ejecuta` lo fija.
3. **`except` demasiado amplio.** `except Exception` enmascara bugs reales del gate
   como "argumentos inválidos". Debe ser `except ValidationError`.
4. **Coerción de pydantic.** Por defecto pydantic v2 coacciona strings numéricos
   (`"8842"` → `8842`); no es un error, pero el alumno debe saber que `"abc"` sí
   levanta. (Un nivel excelente podría usar `Strict` o `model_config` para no
   coaccionar, pero no se exige.)

## Rango de soluciones aceptables
- **`Decision` como dataclass, namedtuple, dict o `str`+`reason` separados**: todas
  cuentan como `competente` mientras los tests accedan a `.accion` y la rama correcta
  salga. (El starter da el dataclass `Decision`; respetarlo es lo limpio.)
- **Un solo modelo pydantic con campos opcionales** en vez de uno por tool: aceptable
  si la validación por tool sigue siendo correcta, aunque el mapa `{nombre: Modelo}`
  es más limpio y escala mejor (nivel excelente).
- **Validar los positivos con `Field(gt=0)`** en vez de `field_validator` es
  equivalente y igual de válido (incluso más conciso).
- **Mensajes de `motivo`** libres: no se evalúa el texto exacto, solo que `accion` sea
  correcta y que el motivo sea útil para logging.
- Para O4, cualquier `verificacion.md` que nombre con precisión "forma vs. semántica"
  y lo ligue a least privilege / Excessive Agency (LLM06) es válido; no se exige una
  redacción concreta.
