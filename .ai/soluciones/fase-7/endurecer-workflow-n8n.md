---
ejercicio_id: fase-7/endurecer-workflow-n8n
fase: fase-7
sub_unidad: "7.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Hay variantes válidas: lo que
> importa es que cumpla las propiedades estructurales y que el alumno **pueda explicar** cada decisión.

# Solución de referencia — Endurece un workflow frágil de n8n

## Cómo usar esta solución

El alumno entrega `workflow.json` + `hardening.md`. La señal objetiva es `test_workflow.py` en verde.
La señal **pedagógica** es si su `hardening.md` defiende el **orden** del dedup y el **riesgo de
reintentar sin idempotencia**. Un JSON verde pero un `hardening.md` que no distingue fallo transitorio
de efecto duplicado es `en-progreso`, no `competente`.

## `workflow.json` de referencia (una versión correcta)

```json
{
  "name": "Procesar pago (endurecido)",
  "nodes": [
    { "name": "Webhook pago", "type": "n8n-nodes-base.webhook", "typeVersion": 2,
      "parameters": { "httpMethod": "POST", "path": "pago-recibido" } },
    { "name": "Dedup por payment_id", "type": "n8n-nodes-base.removeDuplicates", "typeVersion": 2,
      "parameters": {
        "operation": "removeItemsSeenInPreviousExecutions",
        "dedupeValue": "={{ $json.body.payment_id }}"
      } },
    { "name": "Crear factura", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2,
      "parameters": { "method": "POST", "url": "https://facturador.example.com/api/invoices" },
      "retryOnFail": true, "maxTries": 3, "waitBetweenTries": 5000, "onError": "stopWorkflow" },
    { "name": "Notificar Slack", "type": "n8n-nodes-base.slack", "typeVersion": 2,
      "parameters": { "text": "Factura creada" } }
  ],
  "connections": {
    "Webhook pago":        { "main": [[{ "node": "Dedup por payment_id", "type": "main", "index": 0 }]] },
    "Dedup por payment_id":{ "main": [[{ "node": "Crear factura", "type": "main", "index": 0 }]] },
    "Crear factura":       { "main": [[{ "node": "Notificar Slack", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1", "errorWorkflow": "wf-error-global" }
}
```

## Por qué cada pieza (lo que el alumno debe poder defender)

- **Dedup corriente arriba.** El nodo Remove Duplicates va **entre** el Webhook y "Crear factura".
  Si fuera después, la factura duplicada ya estaría creada. La barrera protege el efecto secundario,
  así que va antes de él. Esto es lo más importante del ejercicio.
- **Clave estable.** Deduplica por `payment_id` (un dato estable del evento), no por el item entero ni
  por un id generado en cada corrida. Si la clave cambia entre el evento original y su repetición, no
  deduplica nada.
- **Operación correcta.** `removeItemsSeenInPreviousExecutions` recuerda claves **entre ejecuciones**.
  Deduplicar solo "dentro de la misma ejecución" no sirve: los webhooks repetidos llegan en ejecuciones
  distintas. (El test no exige el nombre exacto de la operación; sí la posición y la existencia del nodo.)
- **Reintentos sanos.** `retryOnFail: true`, `maxTries: 3` (rango 2-5), `waitBetweenTries: 5000` ms
  (no martillar la API sobrecargada). `onError: stopWorkflow` para que un fallo real dispare el error
  workflow en vez de seguir como si nada.
- **Error workflow.** `settings.errorWorkflow` apunta a un flujo que arranca con Error Trigger y alerta
  con el id de la execution. Sin él, los fallos mueren en silencio.

## `hardening.md` esperado (ideas, no literal)

Debe contener, con las palabras del alumno:
1. El dedup va **antes** del efecto secundario porque la barrera protege la acción peligrosa; ponerlo
   después no deshace la factura duplicada.
2. Reintentar **sin** idempotencia es peligroso: si la API creó la factura pero la respuesta se perdió
   (timeout), el reintento crea una **segunda** factura. Reintentos cubren fallos transitorios;
   idempotencia evita duplicar efectos. Son problemas distintos y van juntos.

## Notas para el corrector

- Variantes válidas: otro nombre de nodo, otra clave estable razonable, `maxTries: 2` o `4`, `wait` de
  3000-5000 ms. El orden y la presencia de las tres protecciones no cambian.
- Si el alumno rompió la conexión "Crear factura" → "Notificar Slack" al reconectar, señálalo (el aviso
  dejó de salir), aunque el test no lo verifique.
- Si activó reintentos pero el `hardening.md` dice "ahora es idempotente gracias a los reintentos",
  es la misconception central: márcala, no la dejes pasar aunque el test esté verde.
- `onError`/`maxTries` van **en el objeto del nodo**, no dentro de `parameters`. Si el alumno los metió
  en `parameters`, el test de reintentos falla y el mensaje lo guía.
