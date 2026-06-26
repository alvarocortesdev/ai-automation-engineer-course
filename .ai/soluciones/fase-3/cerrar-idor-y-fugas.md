---
ejercicio_id: fase-3/cerrar-idor-y-fugas
fase: fase-3
sub_unidad: "3.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Cierra el IDOR y la fuga de datos

## Implementación canónica (endpoints corregidos de `app.py`)

```python
@app.get("/notas", response_model=list[NotaPublica])
async def listar_notas(usuario: UsuarioActual) -> list[dict]:
    # acotado al usuario actual: nunca exponer notas ajenas
    return [n for n in _NOTAS.values() if n["owner_id"] == usuario.id]


@app.get("/notas/{nota_id}", response_model=NotaPublica)
async def obtener_nota(nota_id: int, usuario: UsuarioActual):
    nota = _NOTAS.get(nota_id)
    if nota is None or nota["owner_id"] != usuario.id:
        raise HTTPException(status_code=404, detail="Nota no encontrada")  # 404, NO 403
    return nota  # response_model filtra nota_privada_interna y owner_id


@app.delete("/notas/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
async def borrar_nota(nota_id: int, usuario: UsuarioActual) -> Response:
    nota = _NOTAS.get(nota_id)
    if nota is None or nota["owner_id"] != usuario.id:   # mismo chequeo que en GET
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    del _NOTAS[nota_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

Verificado contra `test_app.py`: **6 passed**.

## Por qué cada decisión

- **Chequeo de propiedad (`nota["owner_id"] != usuario.id`)** — la autenticación (el header `x-user-id`) dice *quién* llama; este `if` es la **autorización**: *si puede* tocar ESTE recurso. Sin él, cualquier usuario autenticado lee/borra/lista recursos ajenos = IDOR (A01, la falla #1 del OWASP Top 10 2021).
- **404, no 403** — devolver 403 ("existe pero no es tuya") le confirma al atacante que el recurso existe, habilitando enumeración. Con 404 ("no encontrada") el recurso ajeno es indistinguible de uno inexistente. Es una decisión defendible que conviene anotar en un ADR.
- **El chequeo va en CADA operación** — `GET`, `DELETE` y el listado. Proteger la lectura y olvidar el borrado es el bug clásico. El listado se acota filtrando por `owner_id` (el backend devuelve solo lo autorizado; jamás "filtrar en el frontend").
- **`response_model=NotaPublica`** — barrera anti-fuga: aunque el dict tenga `nota_privada_interna` y `owner_id`, solo viajan los campos del modelo público. Validar la entrada no protege la salida; el `response_model` sí.

## Variantes aceptables
- **Centralizar en una dependencia** (preferible, nivel excelente):

  ```python
  def obtener_nota_propia(nota_id: int, usuario: UsuarioActual) -> dict:
      nota = _NOTAS.get(nota_id)
      if nota is None or nota["owner_id"] != usuario.id:
          raise HTTPException(404, "Nota no encontrada")
      return nota

  NotaPropia = Annotated[dict, Depends(obtener_nota_propia)]
  ```

  y usar `nota: NotaPropia` en `GET` y `DELETE`. Una sola fuente de verdad para la autorización.
- Listado con comprehension, `filter`, o bucle: equivalente mientras devuelva solo lo del usuario.
- Endpoints `def` en vez de `async def`: aceptable (no hay I/O real).

## No aceptable como competente
- ❌ Devolver **403** para el recurso ajeno: el test exige 404 (y filtra la existencia).
- ❌ Cerrar el `GET` pero dejar el `DELETE` o el listado sin chequeo: IDOR sigue abierto.
- ❌ Devolver el dict crudo sin `response_model`: filtra `nota_privada_interna`.
- ❌ "Filtrar el campo interno en el cliente": un atacante no usa tu frontend; la respuesta del backend no debe contenerlo.

## Puntos resbalosos (donde el corrector debe mirar)
1. **El status del recurso ajeno.** El test compara `== 404`. Un 403 (o 200) falla.
2. **El `DELETE` no debe borrar la nota ajena.** El test verifica, tras el 404, que la nota sigue viva para su dueña.
3. **El listado.** El test compara el conjunto exacto de títulos del usuario; si aparece una nota de otro, falla.
4. **`bitacora.md`** debe explicar: por qué 404 y no 403 (no filtrar existencia), por qué el chequeo por operación, y la diferencia autenticación (quién) vs autorización (qué puede).
