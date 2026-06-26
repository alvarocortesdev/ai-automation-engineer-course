# 1.5 — Cliente de API resiliente y testeable

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.5` Archivos, JSON y APIs
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** código

## 🎯 Objetivo

Implementar `nombre_de_usuario(user_id, fetch)`: un cliente de API que distingue los
distintos modos de fallo de una llamada HTTP (status 4xx vs 5xx, error de red) y los
convierte en errores de dominio claros — **sin tocar la red**, gracias a inyectar la
función de fetch (un seam testeable).

## 📋 Contexto

Este es el ejercicio que separa "sé llamar una API" de "sé manejar una API en producción".
La técnica de **inyectar la dependencia de red** (`fetch`) es la misma que usarás en la
sub-unidad `2.11` para testear código que llama a LLMs: un LLM es una API, y se mockea igual.
Plantar el seam ahora te ahorra reescribir todo después.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta la documentación oficial de [`httpx`](https://www.python-httpx.org/exceptions/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `nombre_de_usuario` (no cambies su firma).
   Las excepciones de dominio ya están definidas en el starter.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_solucion.py`.

### Contrato de `nombre_de_usuario(user_id, fetch)`

`fetch` es una función que recibe el `user_id` y devuelve un objeto-respuesta con dos
atributos: `.status_code` (int) y `.json()` (dict). En producción haría la llamada real
con `httpx`; en los tests es una función falsa que devuelve lo que tú quieras.

| Condición | Comportamiento esperado |
|---|---|
| `user_id` ≤ 0 o no es `int` | lanza `ValueError` **antes** de llamar `fetch` |
| `fetch` lanza `TimeoutError` o `ConnectionError` | lanza `ServicioInalcanzable` |
| status `200` | devuelve `resp.json()["name"]` |
| status `404` | lanza `UsuarioNoEncontrado` |
| status `>= 500` | lanza `ServicioCaido` |
| cualquier otro status | lanza `RespuestaInesperada` |

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Validas `user_id` **antes** de llamar `fetch` (no malgastas una petición en input inválido).
- [ ] Distingues los cuatro destinos de status (200 / 404 / 5xx / otro), cada uno con su excepción.
- [ ] Conviertes el error de red en `ServicioInalcanzable` (no dejas escapar el `TimeoutError` crudo).
- [ ] Todos los tests pasan **sin red** y agregaste al menos un caso propio.
- [ ] Puedes explicar **sin notas** por qué inyectar `fetch` hace el código testeable.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Orden de las guardas: primero **valida** `user_id` (esto va **antes** del `try`, para no gastar
una petición). Luego envuelve `fetch(user_id)` en un `try/except (TimeoutError, ConnectionError)`
que re-lanza `ServicioInalcanzable`. Con la respuesta en mano, ramifica por `status_code`: el caso
feliz (200) primero, luego 404, luego `>= 500`, y un catch-all final (`RespuestaInesperada`).
Recuerda la sección 4.6 de la lección: el **orden** de los `if` importa. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/cliente-api-resiliente.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/cliente-api-resiliente.md` — no la
mires antes de intentarlo de verdad.
