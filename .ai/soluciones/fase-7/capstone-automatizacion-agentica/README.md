---
ejercicio_id: fase-7/capstone-automatizacion-agentica
fase: fase-7
sub_unidad: "7.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un **brief de solución de referencia**, no un repo completo: el capstone tiene muchos caminos válidos; esto fija la forma correcta y los puntos resbalosos.

# Solución de referencia — Capstone Fase 7: Automatización end-to-end agéntica

## Respuesta canónica: forma del sistema

```
Webhook (FastAPI)
  → verifica HMAC + anti-replay (timestamp/nonce)        [DoD #3 web]
  → idempotency key = message_id; si ya visto → 200, no re-ejecuta   [DoD #6]
  → arranca workflow Temporal (durable)                   [DoD #6, durabilidad]

Workflow Temporal (cuerpo DETERMINISTA; solo orquesta + funciones puras)
  → actividad: clasificar_y_extraer (LLM, salida estructurada validada)  [I/O en actividad]
  → si schema inválido → actividad enviar_a_dlq + alerta  [DoD #3 LLM05, DLQ]
  → decidir(...) [función PURA]                           [DoD #6]
       RECHAZO  → cierra
       HITL     → workflow.wait_condition(aprobación, timeout=24h)  [espera durable]
       AUTO     → actividad: ejecutar_accion (idempotente, least-privilege)
  → cada paso emite span OTel; correlation id = message_id; tokens/latencia/costo  [DoD #4]

CI: lint + tests + eval_gate (golden set, baseline, regresión) + gitleaks + SCA   [DoD #2,#3,#5]
```

### Plano de control (la pieza que gatean los tests del starter)

```python
def decidir(propuesta, *, schema_valido, ya_procesado, costo_acumulado_usd,
            techo_costo_usd, umbral_confianza=0.85) -> Decision:
    if ya_procesado:
        return Decision(Ruta.DUPLICADO, "input ya procesado (idempotency key)")
    if not schema_valido:
        return Decision(Ruta.RECHAZO, "salida del LLM no valida contra el schema")
    if costo_acumulado_usd >= techo_costo_usd:
        return Decision(Ruta.RECHAZO, "techo de costo excedido")
    if propuesta.accion_propuesta in ACCIONES_SENSIBLES:
        return Decision(Ruta.HITL, "accion sensible: requiere aprobacion humana")
    if propuesta.confianza < umbral_confianza:
        return Decision(Ruta.HITL, "confianza bajo umbral")
    return Decision(Ruta.AUTO, "auto-ejecutable")
```

## Razonamiento paso a paso (el porqué, no solo el qué)

1. **Idempotencia primero.** Un duplicado no debe re-ejecutar nada NI gastar una llamada al LLM. Por eso la idempotency key se consulta al inicio del workflow (o antes, en el webhook). Gana sobre todas las demás barreras: un duplicado con schema inválido y acción sensible es `DUPLICADO`. El problema at-least-once es del transporte, no de la IA — el agente lo hereda igual que cualquier integración (7.2).
2. **Guardrail de schema antes que cualquier lógica de negocio.** Validar la **forma** (LLM05). Pero validar el schema NO es confiar en el contenido: `monto_clp` válido puede ser un disparate; por eso las reglas de negocio y el HITL van encima.
3. **Techo de costo como circuit-breaker** (Unbounded Consumption). Va antes de la acción sensible porque un run que ya gastó de más no debe seguir, sea sensible o no.
4. **Acción sensible → HITL obligatorio, aunque confianza sea 0.99** (LLM06). La confianza auto-reportada no está calibrada; la acción es irreversible. La autonomía sobre lo irreversible es el riesgo central de un agente que actúa. Least-privilege: `ACCIONES_SENSIBLES` es una lista explícita.
5. **Confianza al final y solo para no-sensibles.** Frontera: `confianza == umbral` PASA (es `>= umbral`).
6. **LLM en actividad, no en el workflow.** El cuerpo del workflow se re-ejecuta en cada replay (durabilidad). Una llamada al LLM, a `time` o a `random` rompería el determinismo. `decidir()` es pura, así que correrla en el workflow es seguro.
7. **HITL durable.** `workflow.wait_condition(lambda: self._aprobacion is not None, timeout=timedelta(hours=24))` + un `@workflow.signal aprobar(...)`. El workflow duerme sin consumir recursos y retoma exacto tras un reinicio del worker. Un cron + cola perdería el estado.
8. **Eval gate.** Mide accuracy de routing + exactitud de extracción sobre un golden set anotado (idealmente desde trazas reales). Bloquea por umbral fijo Y por regresión vs baseline versionado. Corre en CI. Mide la **decisión**, no la fluidez.
9. **Observabilidad.** `message_id` como correlation id propagado por todo el call-chain; un span por paso con tokens/latencia/costo. Estas trazas son las que respaldan el post-mortem.

## Puntos resbalosos (dónde el corrector debe mirar)

1. **Orden del plano de control.** El error clásico: confianza primero, o combinar barreras en un `if ... and ...` perdiendo el `motivo`. Los tests de orden del starter lo cazan; verifica que el caso duplicado+inválido+sensible da `DUPLICADO`.
2. **Determinismo del workflow.** Buscar llamadas a LLM/HTTP/DB/`time`/`random` dentro del cuerpo `@workflow.run`. Es el error más sutil y el más grave: pasa la demo y corrompe el replay.
3. **Idempotencia real vs decorativa.** ¿La key se consulta ANTES de ejecutar y se persiste atómicamente? Un replay del mismo webhook debe NO re-ejecutar. Race conditions cuentan como `en-progreso`.
4. **HITL durable de verdad.** Pedir evidencia de que mataron y reiniciaron el worker a mitad de la espera y el workflow retomó. Un HITL en memoria (que se pierde con el proceso) NO cumple.
5. **Eval gate que mide lo correcto.** Si mide BLEU/fluidez o no tiene baseline/regresión, es `en-progreso`. La métrica es tasa de decisión correcta.
6. **Seguridad del webhook.** HMAC sin anti-replay deja pasar replays con firma válida. Falta frecuente.
7. **Comunicación.** README en español o ausente, commits sin Conventional Commits, write-up sin números (eval, costo) → no cumple DoD #8/#9 aunque el código sea bueno.
8. **Post-mortem inventado.** Sin traza que lo respalde ni reconciliación concreta = no hubo falla real ni usuarios reales (Track-0 incumplido).

## Rango de soluciones aceptables

- **Orquestador:** Temporal es lo recomendado y lo que pide el ADR, pero un alumno que justifique sólidamente otra herramienta de ejecución durable (p. ej. otra con replay determinista) y demuestre que el HITL sobrevive a reinicios, es aceptable. Un cron + cola que pierde estado NO es aceptable para este caso.
- **Acción externa:** real o simulada idempotente — lo que importa es que el manejo de fallas (reintentos, idempotencia, DLQ) sea real, no el sistema externo.
- **Dominio:** tickets/reembolsos es la sugerencia; facturas, onboarding o correos son igual de válidos si gatillan una acción sensible irreversible.
- **Convención de frontera de confianza:** `== umbral` PASA (fijado por los tests); un alumno que la quiera estricta debe justificarlo y alinear con los tests.
- **UI del HITL:** una consola/endpoint mínimo es aceptable; si construyen UI web, aplica DoD #7 (WCAG mínima + 4 estados). No construir UI y aprobar por API/CLI también es válido (DoD #7 es condicional a "si hay UI").
- **Excelente** se reserva para: plano de control puro y testeado + durabilidad probada con reinicio + eval gate con golden set de trazas reales + post-mortem con reconciliación real + explicación en inglés en menos de 5 min. Métricas extra (matriz de confusión por categoría, dashboard de costo) suman pero no son requisito.

## Vara para los write-ups

- **`DISENO.md`** debe tener el diagrama con los 9 puntos del DoD ubicados, la tabla de decisión con al menos un caso de dos barreras, y el ADR de Temporal con el trade-off explícito (durabilidad/HITL vs complejidad operacional).
- **`WRITE-UP.md`** debe traer al menos un trade-off que el alumno haya medido (no recitado): número del eval gate + baseline, y costo/latencia por caso. Sin números, es `en-progreso`.
- **`POST-MORTEM.md`** debe ser específico: qué se rompió, cómo se vio en la traza (con el correlation id), cómo se reconcilió sin perder ni duplicar, y el cambio que evita la recurrencia.
