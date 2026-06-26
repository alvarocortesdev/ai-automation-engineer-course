# Ejercicio 3.13a — Cierra el IDOR y la fuga de datos

> **Modalidad: código (Python + FastAPI, sin IA).** Te dan una API de notas **vulnerable**: cualquier usuario autenticado lee, borra y lista notas ajenas, y la respuesta filtra un campo interno. Tu trabajo es cerrar el Broken Access Control (A01 del OWASP Top 10) y la fuga de datos. Todo en memoria, sin base de datos.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.13` OWASP Top 10 web hands-on
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Editar `app.py` para que `pytest` quede en verde, cerrando tres fallas de control de acceso y una fuga:

1. **Listado acotado** — `GET /notas` debe devolver **solo** las notas del usuario actual.
2. **IDOR en lectura** — `GET /notas/{id}` debe devolver **404** si la nota no existe **o** no es del usuario actual (no 403: no filtres la existencia del recurso ajeno).
3. **IDOR en borrado** — `DELETE /notas/{id}` debe aplicar el **mismo** chequeo de dueño antes de borrar.
4. **Fuga de datos** — la respuesta de la nota **no** debe incluir `nota_privada_interna` (usa `response_model`).

## 📋 Contexto

La autenticación (saber **quién** llama) ya está resuelta con un header `x-user-id` que simula un JWT. Lo que falta es la **autorización**: comprobar que ESE usuario es dueño de ESE recurso. Confundir ambas cosas es la raíz del IDOR, la falla #1 del OWASP Top 10 (2021). El chequeo de propiedad debe repetirse en **cada** operación: proteger el `GET` y olvidar el `DELETE` es un clásico que deja la puerta abierta.

## ⚙️ Requisitos

```bash
uv add fastapi httpx pytest      # o:  pip install fastapi httpx pytest
```

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Corre el test y mira fallar cada falla por separado (verás el 200 que devuelve datos ajenos y el campo interno filtrado).
2. Solo entonces, consulta la **documentación oficial** (FastAPI: *Dependencies*, *Response Model*) y la lección (secciones 4.2 y 6.2).
3. **Solo al final**, usa IA para *revisar* — no para generar.
4. Mañana, reescribe de memoria el chequeo de propiedad de `obtener_nota` (incluido por qué 404 y no 403).

## 🛠️ Instrucciones

1. Abre `app.py`. El estado, los modelos y la dependencia `usuario_actual` ya están dados. **No los cambies** (salvo donde el TODO lo pida).
2. **TODO (1)** en `listar_notas`: filtra a `owner_id == usuario.id`.
3. **TODO (2a)** en `obtener_nota`: agrega `response_model=NotaPublica` al decorador (filtra la fuga).
4. **TODO (2b)** en `obtener_nota`: devuelve 404 si la nota no existe **o** no es del usuario actual.
5. **TODO (3)** en `borrar_nota`: aplica el mismo chequeo de dueño antes de `del`.
6. Corre el test:

   ```bash
   uv run pytest        # o:  pytest
   ```

7. Escribe `bitacora.md`: ¿por qué 404 y no 403? ¿por qué el chequeo de dueño debe repetirse en cada operación y no solo en `GET`? ¿cuál es la diferencia entre autenticación y autorización en este ejercicio?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: 401 sin header, 404 en GET/DELETE de nota ajena (sin borrarla), 200/204 para el dueño, listado acotado, sin campo interno en la respuesta.
- [ ] El recurso ajeno responde **404**, no 403 ni 200.
- [ ] La respuesta nunca contiene `nota_privada_interna` ni `owner_id`.
- [ ] `bitacora.md` responde las tres preguntas del paso 7.
- [ ] Puedes explicar **sin notas** la diferencia entre autenticación y autorización con este ejemplo.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- El chequeo de dueño es una sola condición compuesta:

  ```python
  if nota is None or nota["owner_id"] != usuario.id:
      raise HTTPException(status_code=404, detail="Nota no encontrada")
  ```

- Para la fuga, basta declarar `response_model=NotaPublica` en el decorador del `GET /notas/{id}`: FastAPI filtra a los campos del modelo aunque devuelvas el dict completo.
- Para el listado: `return [n for n in _NOTAS.values() if n["owner_id"] == usuario.id]`.

Repasa las secciones 4.2 y 6.2 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `app.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/cerrar-idor-y-fugas.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/cerrar-idor-y-fugas.md` — no la mires antes de intentarlo de verdad.
