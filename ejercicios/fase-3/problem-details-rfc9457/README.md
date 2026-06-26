# Ejercicio 3.7 — Construye errores problem+json (RFC 9457)

> **Modalidad: código (Python puro, sin frameworks), Primero-Sin-IA.** Un cuerpo de error
> `problem+json` es, al final, un diccionario con forma fija. Implementarlo a mano te obliga a
> entender el estándar que después FastAPI te dará "gratis" — y a saber cuándo se rompe.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.7` Diseño de APIs REST
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Implementar dos funciones puras: (1) `build_problem_detail(...)`, que construye un cuerpo de error
`problem+json` válido según **RFC 9457** (campos correctos, defaults correctos, sin claves con valor
`None`), y (2) `choose_status(...)`, que elige el **status code** correcto para una situación dada.
Al terminar, sabrás producir errores HTTP consistentes y elegir el código que cada caso merece.

## 📋 Contexto

En el capstone tu API tendrá un manejador de errores global. Si cada endpoint devuelve los errores
de una forma distinta —o todo con `200`, o filtrando stack traces— pierdes el Definition of Done por
seguridad y consistencia. Este builder es ese manejador, reducido a su esencia testeable.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano, dentro del timebox. Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** (RFC 9457; MDN HTTP status codes).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescribe `build_problem_detail` de memoria. Si no puedes, no caló todavía.

## 🛠️ Instrucciones

1. Abre `problem_details.py` y completa las dos funciones + la constante `PROBLEM_CONTENT_TYPE`
   (no cambies las firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   pytest               # si ya tienes pytest en el entorno
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_problem_details.py` (hay un hueco al final con ideas).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa en verde.
- [ ] `status` y `title` están siempre; `type` ausente cae en `"about:blank"`.
- [ ] `detail` e `instance` **no aparecen** si no se pasan (nada de `"detail": null`).
- [ ] Los `**extensions` se incluyen tal cual en el dict.
- [ ] `choose_status` mapea las 10 situaciones y **levanta `ValueError`** ante una desconocida.
- [ ] `PROBLEM_CONTENT_TYPE == "application/problem+json"`.
- [ ] Agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué un error con `200` es un anti-patrón y por qué 401 ≠ 403.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `build_problem_detail`: arranca con un dict que tenga `type` (usa `type_` si vino, si no
`"about:blank"`), `title` y `status`. Luego **agrega** `detail`/`instance` solo si no son `None`
(un `if detail is not None: problema["detail"] = detail`). Finalmente, `problema.update(extensions)`.
Así nunca metes una clave con valor `None`.

Para `choose_status`: un `dict` que mapee nombre → código es lo más limpio; recupera con `.get(...)`
y si sale `None`, levanta `ValueError`. Repasa la sección 4.5 (problem+json) y 4.2/5 (status codes)
de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `problem_details.py` + `test_problem_details.py` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/problem-details-rfc9457.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/problem-details-rfc9457.md` — no la
mires antes de intentarlo de verdad.
