# Ejercicio 7.3 — Mini-proyecto: saga de checkout durable

> **Modalidad: código.** Implementas un workflow durable de verdad en Temporal y lo verificas con una
> suite que usa el *time-skipping environment* (corre en segundos, sin Docker, sin esperar los 30
> minutos reales). Es la pieza "durable" que tu capstone agéntico va a exigir.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.3` Durable execution / Temporal
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar un workflow durable con la separación **workflow/activity** correcta, una `RetryPolicy`,
una espera durable (`workflow.sleep`) y un patrón **saga**: si el cobro falla, compensar liberando el
inventario reservado y dejar el sistema en estado **consistente**.

## 📋 Contexto

Es el `ProcesoCheckoutWorkflow` del worked example de la lección: reservar inventario → esperar 30 min
→ cobrar → confirmar envío. Las activities (`actividades.py`) y los tests (`tests/test_saga.py`) ya
están escritos. **Tu único trabajo es `workflow.py`**. Antes de codear, conviene haber hecho el
[diagnóstico durable vs cron](../durable-vs-cron-diagnostico/).

## ⚙️ Setup

```bash
# con uv (recomendado): instala temporalio + pytest desde pyproject.toml
uv run pytest
# o con pip:
pip install temporalio pytest && pytest
```

> La **primera** corrida de los tests descarga el binario del test-server de Temporal (necesita
> internet una vez). Después corre offline. **No** necesitas Docker ni levantar un servidor para los
> tests. (Para correrlo "de verdad", ver `worker.py` e `iniciar.py` — opcional.)

## 📏 Primero-Sin-IA

1. Implementa `workflow.py` **solo**, a mano (timebox arriba). Apóyate en el worked example y en la
   regla de la frontera workflow/activity. Está bien que sea lento.
2. Solo entonces, consulta la **documentación oficial** de Temporal si te trabas en una firma.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el workflow.
4. Mañana, reescríbelo de memoria. Si no te sale la compensación de la saga, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `workflow.py` y completa el método `run` (los `TODO`). **No cambies** las firmas ni
   `actividades.py` ni los tests.
2. Respeta las reglas del determinismo: cero I/O, cero `random`, cero `datetime.now()`, cero
   `time.sleep` **dentro** del workflow. La espera es `workflow.sleep`.
3. Pasa `retry_policy=REINTENTOS` a las activities.
4. Implementa la saga en un `try/except`: si `cobrar_pago` falla, llama a `liberar_inventario` y
   luego `raise`.
5. Corre los tests hasta verlos **en verde**:

   ```bash
   uv run pytest        # o:  pytest
   ```

6. Añade **al menos un test propio** en `tests/test_saga.py` (ideas al final del archivo): idempotencia
   por `workflow_id` repetido, o que un fallo transitorio se reintente.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `test_happy_path_orden_de_pasos` pasa: orden reservar→cobrar→confirmar, sin compensación.
- [ ] `test_tarjeta_rechazada_compensa_y_falla` pasa: el inventario **se libera** y el envío **no** se
      ejecuta; el workflow falla.
- [ ] **Cero** I/O / no-determinismo dentro del workflow; la espera usa `workflow.sleep`.
- [ ] La `RetryPolicy` se pasa a las activities.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué el cobro va en una activity y no en el workflow, y por qué
      la compensación va **antes** del `raise`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El esqueleto del `run` es lineal: una variable `reserva_id` del primer `execute_activity`, un
`workflow.sleep`, y luego el `try/except` alrededor del cobro. La clave de la saga: la compensación
(`liberar_inventario`) va **dentro** del `except`, **antes** del `raise`. Para `confirmar_envio`, que
recibe dos argumentos, usa `args=[orden, reserva_id]` en vez de pasar un solo argumento posicional.
Revisa el worked example 2 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-7/saga-pago-durable.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/saga-pago-durable.md` — no la mires antes
de intentarlo de verdad.
