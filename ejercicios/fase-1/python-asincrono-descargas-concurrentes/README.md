# 1.3 — Descargas concurrentes que se miden solas

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.3` Python asíncrono
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Implementar una corutina que ejecute varias operaciones de I/O **concurrentemente** (no en serie),
preservando el orden de entrada de los resultados, y demostrar con una **medición de tiempo** que la
latencia total baja de la suma de las demoras a, aproximadamente, la mayor.

## 📋 Contexto

Esto es, en miniatura, lo que hará tu agente de IA cuando llame a varias herramientas a la vez, o tu
endpoint de FastAPI cuando consulte la base de datos y un servicio externo. Si lo haces de a uno,
sumas latencias (y en serverless, costo). El truco —lanzar todo y esperar junto— se entrena aquí.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta la **documentación oficial** de `asyncio` (Coroutines and Tasks).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa la corutina `obtener_todos` (no cambies su firma).

   Contrato:
   - **Entrada:** una `list[dict]`; cada `dict` tiene `"nombre"` (str) y `"demora"` (float, segundos).
   - Cada "descarga" se simula con `await asyncio.sleep(demora)` y devuelve `f"datos de {nombre}"`.
   - **Salida:** la `list[str]` de resultados **en el mismo orden de entrada**.
   - Todas las descargas deben correr **concurrentemente** (solapadas), no una tras otra.
   - La lista vacía devuelve `[]`.

2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

   > Solo necesitas `pytest`. Los tests corren tu corutina con `asyncio.run(...)`, así que **no**
   > hace falta el plugin `pytest-asyncio`.

3. Itera hasta que **todos los tests pasen en verde**. Presta atención a `test_es_concurrente`: si tu
   solución es secuencial, ese test fallará porque tardará la suma de las demoras.
4. Añade al menos **un caso de prueba tuyo** en `test_solucion.py` (por ejemplo, la lista vacía, o un
   solo recurso).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los resultados salen **en orden de entrada**, no de finalización.
- [ ] `test_es_concurrente` pasa: el total es ~la mayor demora, no la suma.
- [ ] La lista vacía devuelve `[]` sin reventar.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes explicar **sin notas** por qué `await` dentro de un `for` no habría servido.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Define una corutina interna `descargar(recurso)` que haga el `sleep` y devuelva el string. Luego
**no** la esperes dentro del bucle: arma una lista de corutinas (`[descargar(r) for r in recursos]`) y
pásala completa a `asyncio.gather(*corutinas)`, que ya te devuelve los resultados en orden. (Alternativa
moderna: un `asyncio.TaskGroup` en Python 3.11+.) Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/python-asincrono-descargas-concurrentes.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/python-asincrono-descargas-concurrentes.md`
— no la mires antes de intentarlo de verdad.
