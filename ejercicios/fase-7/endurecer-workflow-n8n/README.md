# endurecer-workflow-n8n — Endurece un workflow frágil de n8n

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.1` n8n: de tool a arquitectura
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** código (JSON)

## 🎯 Objetivo

Tomar un workflow de n8n de **happy path** (Webhook → Crear factura → Slack) y
volverlo **confiable**: idempotente (que el mismo evento dos veces no duplique la
factura), con **reintentos** ante fallos transitorios, y con un **error workflow**
asociado para que nada falle en silencio.

## 📋 Contexto

Es el esqueleto de confiabilidad del **Capstone F7** (la estrella de tu portafolio):
un agente que ejecuta acciones en sistemas externos **no puede** duplicar efectos
ni morir callado. Lo que practicas acá —dedup corriente arriba del efecto
secundario, reintentos en la acción peligrosa, error workflow— es requisito directo
del Definition of Done de ese capstone.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Edita el JSON con tus manos.
2. Solo entonces, consulta **documentación oficial** (`docs.n8n.io`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el JSON.
4. Mañana, **reescribe de memoria** los tres agujeros que tapaste. Si no puedes, no
   lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `workflow.json`. Es un export simplificado de n8n con el flujo frágil.
2. Edítalo para que cumpla las cuatro propiedades:
   - **Idempotencia:** inserta un nodo `n8n-nodes-base.removeDuplicates` **entre**
     el Webhook y "Crear factura". Reconecta `connections` para que el Webhook
     fluya **primero** al dedup, y el dedup fluya a "Crear factura". La clave de
     dedup debe ser algo **estable** del evento (un `payment_id`), no el item
     entero ni nada que cambie entre intentos.
   - **Reintentos:** en "Crear factura", pon `"retryOnFail": true`,
     `"maxTries"` entre 2 y 5, y `"waitBetweenTries"` mayor que 0 (en ms).
   - **Error workflow:** agrega `"errorWorkflow"` (id no vacío) dentro de `settings`.
3. Valida la **estructura** de tu JSON (no necesitas una instancia de n8n):

   ```bash
   uv run pytest test_workflow.py     # o:  pytest test_workflow.py
   ```

   El test solo usa la librería estándar (`json`); no instala nada.
4. Itera hasta que `test_workflow.py` esté **verde**. Cada assert te dice qué falta.
5. Escribe `hardening.md` (5–8 líneas): por qué el dedup va **antes** del efecto
   secundario, y por qué **reintentar sin idempotencia es peligroso**.

> El formato de una conexión en n8n es:
> `"NodoOrigen": { "main": [[ { "node": "NodoDestino", "type": "main", "index": 0 } ]] }`.
> Los settings de reintento (`retryOnFail`, `maxTries`, `waitBetweenTries`, `onError`)
> viven **en el objeto del nodo**, no dentro de `parameters`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest test_workflow.py` pasa (dedup presente, Webhook → dedup →
      "Crear factura", reintentos en "Crear factura", `settings.errorWorkflow`).
- [ ] El dedup está **corriente arriba** del efecto secundario (no después).
- [ ] `hardening.md` explica el **orden** (dedup antes) y el **riesgo de reintentar
      sin idempotencia**.
- [ ] Puedes **explicar sin notas** la diferencia entre tolerar fallos transitorios
      (reintentos) y no duplicar efectos (idempotencia).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Lee `test_workflow.py`: es tu **spec**. Cada función nombra una propiedad y su
mensaje de error te dice qué falta. El cambio más fiddly son las `connections`: hoy
el Webhook apunta a "Crear factura"; tienes que hacer que el Webhook apunte al nodo
de **dedup**, y que el dedup apunte a "Crear factura". No borres la conexión de
"Crear factura" → "Notificar Slack". Para la clave de dedup, piensa: ¿qué dato del
pago es el mismo en el evento original y en su repetición? Ese es tu `payment_id`.
Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu IA:

- tu solución (este directorio, con tu `workflow.json` y `hardening.md`),
- la **rúbrica**: `.ai/rubricas/fase-7/endurecer-workflow-n8n.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/endurecer-workflow-n8n.md`
— no la mires antes de intentarlo de verdad.
