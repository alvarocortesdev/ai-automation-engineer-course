---
ejercicio_id: fase-1/bitacora-json
fase: fase-1
sub_unidad: "1.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Bitácora en JSON (round-trip robusto)

## Respuesta canónica

```python
from __future__ import annotations

import json
from pathlib import Path


class BitacoraCorrupta(Exception):
    """El archivo existe pero su contenido no es JSON válido."""


def cargar(ruta: str | Path) -> list:
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise BitacoraCorrupta(f"la bitácora en {ruta} no es JSON válido: {e}") from e


def agregar(ruta: str | Path, mensaje: str) -> None:
    registros = cargar(ruta)
    registros.append({"mensaje": mensaje})
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)


def resumen(registros: list) -> dict:
    return {"total": len(registros)}
```

## Razonamiento paso a paso

1. **`cargar` reúsa el patrón "leer con `with` + `json.load`".** El `with open(..., encoding="utf-8")`
   garantiza el cierre y la codificación correcta. `json.load` (sin `s`) lee directo del archivo.
2. **Dos `except` específicos, dos decisiones distintas.**
   - `FileNotFoundError` → `return []`: la primera vez no hay archivo; eso es esperable, no un error.
   - `json.JSONDecodeError` → `raise BitacoraCorrupta(...) from e`: el archivo existe pero está roto;
     eso es un bug que el llamador debe conocer. `JSONDecodeError` es subclase de `ValueError`.
     El `from e` **encadena la causa** (preserva el traceback original para depurar).
3. **`agregar` se apoya en `cargar`** (no duplica la lectura), hace `.append({"mensaje": mensaje})`
   y guarda con `json.dump(..., ensure_ascii=False, indent=2)`:
   - `ensure_ascii=False` → la `ñ` y los acentos quedan legibles en disco, no como `\uXXXX`.
   - `indent=2` → archivo legible por humanos.
   - `encoding="utf-8"` al escribir → consistente con la lectura; sin esto, Windows corrompería acentos.
4. **`resumen` es trivial:** `{"total": len(registros)}`. Está separada a propósito (función pura,
   fácil de testear sin tocar disco).

## Puntos resbalosos (donde el corrector debe mirar)
1. **`dump` vs `dumps`.** La solución usa `json.dump` (sin `s`, escribe al archivo). Un error común
   es `json.dumps(registros, f)` → `TypeError`, o `f.write(json.dumps(registros))` (funciona pero es
   menos idiomático; aceptable si el encoding es correcto).
2. **`ensure_ascii`.** Si el alumno omite `ensure_ascii=False`, el round-trip a nivel de objeto
   Python **sigue siendo correcto** (`json.load` decodifica los `\uXXXX`), así que `cargar` devuelve
   los datos bien. Lo que falla es el test que inspecciona el **archivo crudo** (`"ñandú" in crudo`).
   Distinguir: el dato no se corrompe, pero el archivo queda ilegible y contra el contrato.
3. **`encoding="utf-8"`.** En macOS/Linux suele ser el default, así que el alumno puede "tener suerte"
   y pasar los tests sin ponerlo. Marcarlo igual: es un bug latente que explota en otra máquina.
4. **`except` genérico.** Un `except Exception`/`except:` que devuelve `[]` para todo haría pasar el
   test del inexistente pero **esconde** el JSON corrupto (el test de `BitacoraCorrupta` fallaría, o
   peor, pasaría por la razón equivocada). Es el anti-patrón clave a cazar.

## Rango de soluciones aceptables
- Usar `pathlib` en vez de `open()` es **igual de válido** (incluso preferible):
  ```python
  def cargar(ruta):
      p = Path(ruta)
      if not p.exists():
          return []
      try:
          return json.loads(p.read_text(encoding="utf-8"))
      except json.JSONDecodeError as e:
          raise BitacoraCorrupta(...) from e
  ```
  Nota: la variante con `if not p.exists()` tiene una carrera teórica (TOCTOU) frente a la de
  `try/except FileNotFoundError`; a este nivel **no se penaliza**, pero un `excelente` podría
  preferir el `try/except` por robustez.
- No usar `from e` baja de `excelente` a `competente`, no a `en-progreso` (la causa se pierde pero
  el comportamiento observable es correcto).
- Omitir `indent=2` es cosmético: no rompe el round-trip; mencionar pero no penalizar fuerte.
- Cualquier nombre de variable interno es libre; lo que se evalúa son las firmas públicas del contrato.
