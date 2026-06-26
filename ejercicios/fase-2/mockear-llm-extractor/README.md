# 2.11 — Mockear el LLM: suite para un extractor de pedidos

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.11` Testing de código que llama a LLMs
**Ruta:** crítica · **Timebox:** 40 min · **Modalidad:** código

## 🎯 Objetivo

Escribir la **suite de tests** (no el código bajo prueba, que ya existe y es
correcto) de un extractor que llama a un LLM, usando *fakes* deterministas que
reemplazan la frontera del modelo. Pruebas tu código —construcción de prompt,
parseo, validación, manejo de error— **sin red, sin tokens y sin
no-determinismo**. La prueba de que tu suite *sirve* es que **caza un mutante**
con un bug introducido.

## 📋 Contexto

`solucion.py` es el **system under test (SUT)** y está correcto. `extraer_pedido`
recibe un callable inyectado `generar(prompt) -> str`: esa es la **frontera** (en
producción, una llamada a un LLM). Todo lo demás —validar la entrada, construir el
prompt, parsear el JSON, validar campos— es lógica pura y determinista, y es justo
donde viven los bugs. Esto es exactamente lo que harás en el **Capstone F2** si tu
app toca un LLM: aislar la llamada detrás de un *port* y testear tu pegamento.

Lo que **no** vas a probar aquí: que el modelo "extraiga bien". Tus fakes devuelven
respuestas que **tú** escribes; tus asserts verifican que tu código las parsea y
valida, no que el modelo acierte. Medir si el modelo acierta es un **eval** (Fase 6).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Lee el SUT y calcula cada
   `esperado` leyéndolo, no ejecutando primero.
2. Solo entonces, consulta la [documentación oficial de pytest](https://docs.pytest.org/)
   y de [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe la suite de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `test_solucion.py` y completa los **cinco** bloques marcados con `TODO`.
   **No modifiques `solucion.py`.**
2. Corre la suite hasta tener **verde**:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. **Autochequeo (obligatorio):** confirma que tu suite caza el bug. Cambia, en
   `test_solucion.py`, la línea:

   ```python
   from solucion import (
   ```

   por `from mutantes.mutante_a import (`, corre `pytest` y confirma que tu suite
   se pone **ROJA**. Luego **revierte** el import a `solucion`. Si el mutante deja
   tu suite en verde, te falta el caso de **cantidad inválida** (TODO 4): el
   mutante omite esa validación.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La suite pasa **verde** contra `solucion.py` (no modificaste el SUT).
- [ ] **Happy path**: un fake con JSON válido y afirmas el `Pedido` correcto.
- [ ] **Prompt** (spy con `Mock`): afirmas que el prompt enviado contiene el
      mensaje del cliente (`generar.call_args.args[0]`).
- [ ] Tres `pytest.raises(ExtraccionInvalida)`: respuesta **no-JSON**, **cantidad
      inválida** (≤ 0 o no entera), y **mensaje vacío**.
- [ ] El test de mensaje vacío usa un `Mock` como `generar` y afirma
      `generar.assert_not_called()` (no se gasta llamada al modelo).
- [ ] Tu suite **caza al mutante** (rojo con `mutantes.mutante_a`) y revertiste el import.
- [ ] Puedes explicar **sin notas** por qué ningún test prueba que el modelo
      "extraiga bien" y qué tipo de prueba sí lo haría.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `test_solucion.py` — tu suite, verde contra `solucion.py`.
- (Opcional) `notas.md` — qué caso atrapó al mutante y qué hueco tenía tu primera versión.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Un *fake* es solo una función que devuelve lo que tú decidas:
`def fake(resp): return lambda prompt: resp`. Para el **spy** del prompt, usa
`generar = Mock(return_value='{"producto": "café", "cantidad": 2}')`, llama a
`extraer_pedido("quiero 2 cafés", generar)` y revisa `generar.call_args.args[0]`.
Para el **no-JSON**, un fake que devuelve `"Claro, 2 cafés"` hace explotar
`json.loads`, que tu código convierte en `ExtraccionInvalida`. Para la **cantidad
inválida**, un fake con `'{"producto": "café", "cantidad": -3}'` (o `"2"` como
string) — ese caso es el que caza al mutante. Para el **mensaje vacío**, pásale un
`Mock` y afirma `generar.assert_not_called()`. **No mockees `json.loads` ni la
validación**: si lo haces, dejas de probar el parseo. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `test_solucion.py`**),
- la **rúbrica**: `.ai/rubricas/fase-2/mockear-llm-extractor.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/mockear-llm-extractor.md`
— no la mires antes de intentarlo de verdad.
