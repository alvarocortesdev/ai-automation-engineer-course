"""Construye errores HTTP estándar (RFC 9457 — problem+json) en Python puro.

No usa ningún framework: un cuerpo problem+json es, al final, un simple diccionario.
Completa las funciones marcadas con TODO. NO cambies las firmas (los tests dependen de ellas).

Corre los tests desde esta carpeta:
    uv run pytest        # recomendado
    pytest               # si ya tienes pytest en el entorno
"""

# El media type que DEBE acompañar a un cuerpo problem+json (header Content-Type).
PROBLEM_CONTENT_TYPE = ""  # TODO: el Content-Type correcto según RFC 9457


def build_problem_detail(status, title, *, type_=None, detail=None, instance=None, **extensions):
    """Devuelve un dict con la forma problem+json (RFC 9457).

    Reglas (léelas con cuidado, son el ejercicio):
      - `status` y `title` SIEMPRE están presentes en el dict.
      - `type`: la CLAVE del dict es "type" (no "type_"). Si no se pasa `type_`,
        su valor por defecto es "about:blank" (lo que dice el estándar cuando el
        miembro está ausente).
      - `detail` e `instance`: SOLO aparecen en el dict si se pasaron (distintos de None).
        No incluyas claves con valor None (un `{"detail": null}` es un error de diseño).
      - Cualquier campo extra en `**extensions` se agrega tal cual al dict
        (RFC 9457 permite "extension members", p. ej. campos_invalidos=[...]).

    Ejemplo:
        build_problem_detail(404, "No encontrado")
        # -> {"type": "about:blank", "title": "No encontrado", "status": 404}
    """
    raise NotImplementedError("TODO: construye el dict problem+json")


def choose_status(situation):
    """Devuelve el status code HTTP (int) correcto para una situación nombrada.

    Situaciones que debes soportar (str -> int):
        "ok"                -> 200
        "created"           -> 201
        "no_content"        -> 204
        "malformed_body"    -> 400   (JSON inválido / falta un campo obligatorio)
        "missing_auth"      -> 401   (sin credencial o credencial inválida)
        "forbidden"         -> 403   (autenticado pero sin permiso)
        "not_found"         -> 404   (el recurso no existe)
        "state_conflict"    -> 409   (choca con el estado actual del recurso)
        "validation_failed" -> 422   (sintaxis OK, validación de negocio falla)
        "server_error"      -> 500   (error del servidor)

    Para una situación desconocida, levanta ValueError.
    """
    raise NotImplementedError("TODO: mapea cada situación a su status code")
