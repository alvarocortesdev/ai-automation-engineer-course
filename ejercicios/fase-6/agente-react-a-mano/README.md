# Ejercicio 6.8 — El agent loop ReAct, a mano

> **Modalidad: código (sin IA para resolver).** Implementas el corazón de un agente: el
> **bucle** razonar → actuar → observar. Para que sea testeable **sin API ni API key**, el
> "modelo" se te **inyecta** como parámetro. Si entiendes este loop, entiendes cualquier
> framework de agentes — todos esconden este mismo bucle.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.8` AI Agents desde cero
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar `ejecutar_agente(pregunta, llamar_modelo)`: un loop ReAct que llama al modelo,
y mientras el modelo pida herramientas, las **valida** (allowlist), las **ejecuta** y le
**devuelve** el resultado, hasta que el modelo termina (`end_turn`) o se alcanza el **techo
de pasos** (`MAX_PASOS`). Sin loop infinito, sin ejecutar herramientas no permitidas.

## 📋 Contexto

Un agente es el tool use de la lección 6.4 dentro de un `while`. Una vuelta = function
calling; N vueltas = agente. El "modelo" se inyecta (`llamar_modelo(mensajes)`) en vez de
llamar a `client.messages.create(...)`, para que puedas probar la **lógica del loop** de
forma determinista con un modelo falso guionizado. Cablearlo a la API real es, después,
reemplazar `llamar_modelo` por una llamada real. Este loop —con su techo de costo, su gate
de allowlist y su HITL— es el esqueleto del capstone agéntico de la Fase 7.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** (tool use de Anthropic, LangGraph).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ El contrato (lo que ya está en `agente.py`)

- `Bloque`, `Respuesta`, `ResultadoAgente`: las dataclasses del contrato.
- `MAX_PASOS = 5`, `HERRAMIENTAS_PERMITIDAS` (la allowlist), `REGISTRO` (nombre → función).
- `invocar(nombre, args)`: ejecuta una tool del registro (asume que ya pasó el gate).
- Las herramientas `buscar_precio` y `convertir_clp_a_usd`.

El "modelo" inyectado devuelve un `Respuesta` con `.stop_reason` (`"tool_use"` o
`"end_turn"`) y `.content` (lista de `Bloque`). Tú lo recibes y **no lo llamas a una API**.

La lista de mensajes (memoria de corto plazo) usa este formato:

```python
{"rol": "assistant", "contenido": resp.content}                       # turno del modelo
{"rol": "user", "contenido": [                                        # tus observaciones
    {"tipo": "tool_result", "tool_use_id": "t1", "contenido": "200000", "es_error": False},
]}
```

Las reglas del loop, **en este orden** por vuelta:

1. **Razonar:** `resp = llamar_modelo(mensajes)`.
2. **Observar:** añade `{"rol": "assistant", "contenido": resp.content}` a `mensajes`,
   **siempre** (antes de decidir nada).
3. **¿Terminó?:** si `resp.stop_reason != "tool_use"`, devuelve el texto del primer bloque
   tipo `"text"` con `detenido_por="end_turn"`.
4. **Gate + actuar:** por cada bloque `tool_use`:
   - si `nombre` **no** está en `HERRAMIENTAS_PERMITIDAS` → `tool_result` con
     `es_error=True` y contenido `"herramienta no permitida"`, **sin ejecutarla**;
   - si está permitido → `invocar(nombre, input)` y devuelve `str(salida)`.
5. Añade `{"rol": "user", "contenido": [<tool_result dicts>]}` y deja que el `for` repita.

Si el loop se agota sin `end_turn`: `respuesta=None`, `detenido_por="tope_pasos"`.

## 🧩 Instrucciones

1. Abre `agente.py` y completa `ejecutar_agente`.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **los 5 tests pasen en verde**.
4. Añade al menos **un test propio** (idea: el modelo pide **dos** tools en la misma vuelta;
   o una tool permitida y otra no en el mismo turno).

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — para los 3 casos de abajo, qué devuelve `ejecutar_agente` y cuántas
  vueltas da. **Escríbelo ANTES de ejecutar.**
- `agente.py` — tu implementación (los 5 tests en verde).
- `verificacion.md` — 2-3 frases: por qué el techo de pasos es a la vez defensa de **costo**
  y de **seguridad**, y por qué la allowlist es **least privilege** (conéctalo con Excessive
  Agency, OWASP LLM06).

Los 3 casos a predecir en `prediccion.md`:
- Una respuesta directa (el modelo no pide tools).
- Una tool y luego responde (`buscar_precio` → `end_turn`).
- Un modelo terco que pide `buscar_precio` para siempre.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe **antes** de ejecutar, con las 3 predicciones + razón.
- [ ] Los 5 tests pasan (`pytest`).
- [ ] Una tool fuera de la allowlist se rechaza con `es_error=True` y **nunca se ejecuta**.
- [ ] Un modelo que nunca termina se corta en `MAX_PASOS` (sin loop infinito).
- [ ] Agregaste al menos un test propio.
- [ ] `verificacion.md` conecta el techo con costo + seguridad y la allowlist con LLM06.
- [ ] Puedes **explicar tu loop sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/agente-react-a-mano/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad.
