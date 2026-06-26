---
ejercicio_id: fase-3/problem-details-rfc9457
fase: fase-3
sub_unidad: "3.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Construye errores problem+json (RFC 9457)

## Implementación

```python
PROBLEM_CONTENT_TYPE = "application/problem+json"


def build_problem_detail(status, title, *, type_=None, detail=None, instance=None, **extensions):
    problema = {
        "type": type_ if type_ is not None else "about:blank",
        "title": title,
        "status": status,
    }
    if detail is not None:
        problema["detail"] = detail
    if instance is not None:
        problema["instance"] = instance
    problema.update(extensions)   # extension members (RFC 9457 §3.2)
    return problema


_STATUS = {
    "ok": 200,
    "created": 201,
    "no_content": 204,
    "malformed_body": 400,
    "missing_auth": 401,
    "forbidden": 403,
    "not_found": 404,
    "state_conflict": 409,
    "validation_failed": 422,
    "server_error": 500,
}


def choose_status(situation):
    code = _STATUS.get(situation)
    if code is None:
        raise ValueError(f"Situación desconocida: {situation!r}")
    return code
```

## Por qué cada decisión

- **`type` por defecto `about:blank`.** RFC 9457 dice que cuando el miembro `type` está ausente, su
  valor se asume `"about:blank"`. Ponerlo explícito hace el objeto autocontenido y testeable.
- **No incluir claves con `None`.** Un `{"detail": null}` es ruido que algunos clientes interpretan
  distinto a "ausente". Por eso se agrega `detail`/`instance` **solo** si tienen valor. Construir el
  dict base y añadir condicionalmente es más claro que crear todo y luego filtrar.
- **`**extensions` con `update`.** RFC 9457 permite extender el objeto con campos propios
  (`campos_invalidos`, `cupo_maximo`, etc.). `update` los mezcla tal cual.
- **`choose_status` como diccionario.** El mapeo es declarativo y fácil de auditar; `.get` + `raise
  ValueError` evita que una situación no contemplada pase silenciosa (fail-fast).

## Los status codes, defendidos
- **400 vs 404 vs 422:** 400 = la petición está mal formada (JSON inválido, falta un campo); 404 = la
  petición es válida pero el recurso no existe; 422 = sintaxis correcta pero la validación de negocio
  falla.
- **401 vs 403:** 401 = no sé quién eres (sin credencial o inválida); 403 = sé quién eres pero no
  puedes hacer esto.
- **409:** el recurso existe y la petición es válida, pero choca con el **estado actual** (libro ya
  prestado, evento lleno). No es 400 ni 404.
- **204:** operación exitosa sin cuerpo que devolver (el caso típico de `DELETE`).

## Test propio aceptable (ejemplos)

```python
def test_instance_se_omite_si_solo_paso_detail():
    p = build_problem_detail(404, "No encontrado", detail="El id 9 no existe.")
    assert "detail" in p and "instance" not in p


def test_extension_puede_convivir_con_campos_estandar():
    p = build_problem_detail(409, "Conflicto", cupo_maximo=200, inscritos=200)
    assert p["status"] == 409 and p["cupo_maximo"] == 200
```

## Puntos resbalosos (donde el corrector debe mirar)
1. **`"detail": None` colado.** El error más común; el test `test_ningun_valor_none_se_cuela` lo caza.
2. **`type` faltante en vez de `about:blank`.** Si el alumno omite la clave, falla el test del mínimo.
3. **401↔403 o 409↔422 cruzados** en `choose_status`.
4. **No levantar `ValueError`** ante situación desconocida (devolver `None`/`500` por defecto).
5. **Test propio vacío** (`assert True`) o duplicado de uno existente: no demuestra comprensión.

## Rango de respuestas aceptables
- Builder: aceptar variaciones (`type_ or "about:blank"` vs `if type_ is not None`) siempre que el
  resultado sea idéntico y no se cuelen `None`.
- `choose_status`: aceptar `dict`, `match`/`case` o `if/elif`; exigir `ValueError` ante desconocida.
- ❌ **No aceptable como competente:** tests rojos, `"detail": null` en el dict, status codes
  cruzados, o no manejar la situación desconocida.
