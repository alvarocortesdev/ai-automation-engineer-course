# Brief — Capstone agéntico de F7 (úsalo si aún no tienes un proyecto propio)

> Usa este brief solo si todavía no construiste un proyecto fuerte. Si ya tienes uno, articúlalo a él en
> su lugar. No edites este archivo: es el input.

## Qué es el sistema

Un sistema de **automatización end-to-end con IA** que procesa tickets de soporte:

1. **Recibe** un ticket (por email o webhook): texto libre de un cliente.
2. **Clasifica** el ticket con un LLM (categoría + prioridad + ruta de resolución).
3. **Extrae** datos estructurados (cliente, producto, urgencia) contra un esquema.
4. **Decide** una acción: responder con una plantilla, escalar a un humano, o cerrar.
5. **Ejecuta** la acción en sistemas externos (crea/actualiza el ticket en la herramienta de soporte).

## Contexto de producción (lo que lo hace interesante de articular)

- El sistema **actúa en el mundo**: una decisión equivocada (cerrar el ticket de un cliente real, o
  responder con la plantilla incorrecta) tiene costo. No es un demo de juguete.
- Procesa **volumen variable**: la mayoría de los tickets son comunes y repetitivos; una minoría es
  ambigua y difícil.
- Corre con un **presupuesto**: cada llamada al LLM cuesta dinero y suma latencia.
- El LLM **puede fallar**: devolver una clasificación fuera del esquema, alucinar una categoría, o
  equivocarse en un caso ambiguo.

## Cruces de diseño donde tuviste que decidir (para tu write-up)

Estos son cruces reales con al menos dos caminos razonables. Elige y articula al menos dos:

- **Autonomía vs control:** ¿el agente ejecuta la acción directamente, o valida su salida y pide
  confirmación humana para acciones sensibles (human-in-the-loop)?
- **Costo:** ¿usas el modelo más capaz (y caro) para todos los tickets, o ruteas los comunes a un modelo
  barato y reservas el caro para los ambiguos?
- **Manejo de fallas:** ¿qué pasa cuando el LLM devuelve algo fuera del esquema? ¿reintentas, usas un
  fallback determinista, escalas a humano?
- **Observabilidad:** ¿registras la traza del call-chain (qué decidió, con qué tokens/latencia/costo por
  paso), o solo el resultado final?

## Métricas plausibles (para tus bullets de impacto — márcalas como medidas o estimadas)

Estas son cifras *plausibles* que tu sistema podría haber producido. Úsalas como punto de partida, pero
sé honesto sobre si las medirías o las estimarías:

- Tiempo de triage manual antes: ~15 min/ticket. Con el sistema: menos de 1 min/ticket.
- Costo por ticket: bajó ~60% al rutear el 80% de los casos comunes a un modelo barato.
- Tasa de clasificaciones fuera de esquema antes de la validación: ~4%; todas atrapadas antes de ejecutar.
