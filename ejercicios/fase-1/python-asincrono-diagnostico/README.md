# 1.3 — Diagnostica el async roto

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.3` Python asíncrono
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** mixta (diagnóstico + corrección)

## 🎯 Objetivo

Diagnosticar y corregir los **tres errores clásicos** de async: olvidar un `await`, bloquear el event
loop con código síncrono, y hacer `await` en serie dentro de un bucle. No basta con que "funcione":
tienes que **explicar la causa** de cada uno.

## 📋 Contexto

Estos tres bugs son los que más vas a cometer (y ver en código ajeno) al empezar con async. El segundo
—un `time.sleep` o un `requests.get` síncrono dentro de una corutina— es especialmente traicionero:
no rompe nada, solo congela silenciosamente a todas las demás tareas. Aprender a olerlo te ahorra horas.

## 📏 Primero-Sin-IA

1. **Sin ejecutar todavía**, lee `roto.py` y diagnostica a mano.
2. Solo entonces ejecútalo para confirmar.
3. Corrige sin IA; usa la documentación oficial si la necesitas.
4. Mañana, explica los tres bugs de memoria.

## 🛠️ Instrucciones

1. **Lee `roto.py`** (no lo edites). Tiene tres bugs marcados con comentarios `(1)`, `(2)`, `(3)`.
2. **Sin ejecutar**, escribe `diagnostico.md` con, para cada bug:
   - qué línea es y qué está mal,
   - **por qué** está mal (la causa, no solo el síntoma),
   - qué síntoma produce (incluida la advertencia que imprime Python, si aplica).
3. **Ejecuta** `roto.py` y confirma tus hipótesis. Anota en `diagnostico.md` qué advertencia y qué
   tiempo viste realmente.
4. Escribe la versión corregida en `solucion.py` (completa `descargar_todo`) y corre los tests:

   ```bash
   uv run pytest        # o:  pytest
   ```

   > Ojo: `test_es_concurrente_y_no_bloquea` solo pasa si corriges **los dos** problemas de velocidad
   > (el `time.sleep` que bloquea el loop **y** el `await` secuencial). Arreglar uno solo no alcanza.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `diagnostico.md` identifica los **tres** bugs con su **causa** (no solo el síntoma).
- [ ] Explicaste por qué un `time.sleep` dentro de una corutina congela a **todas** las tareas.
- [ ] Nombraste la advertencia que imprime Python al olvidar un `await`
      (`coroutine '...' was never awaited`).
- [ ] Tu `solucion.py` es concurrente (el test de tiempo lo verifica) y devuelve los resultados en orden.
- [ ] Puedes explicar tu corrección **sin notas**.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **(1)** `registrar_inicio(nombre)` se llama sin `await`: la corutina nunca corre y Python avisa
  `RuntimeWarning: coroutine 'registrar_inicio' was never awaited`. Espérala (`await ...`) o agéndala.
- **(2)** `time.sleep(...)` es **síncrono**: bloquea el event loop entero. Cámbialo por
  `await asyncio.sleep(...)`. (Si fuera una librería bloqueante real sin versión async, usarías
  `await asyncio.to_thread(...)`.)
- **(3)** El `for` con `await descargar(...)` espera cada descarga antes de lanzar la siguiente
  (secuencial). Reúne las corutinas y usa `asyncio.gather(*corutinas)` o un `asyncio.TaskGroup`.

Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Entrega a tu IA: este directorio (con tu `diagnostico.md` y `solucion.py`), la **rúbrica**
`.ai/rubricas/fase-1/python-asincrono-diagnostico.md` y `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/python-asincrono-diagnostico.md` — no la
mires antes de intentarlo de verdad.
