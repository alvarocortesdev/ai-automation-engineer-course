---
ejercicio_id: fase-7/durable-vs-cron-diagnostico
fase: fase-7
sub_unidad: "7.3"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico: durable execution vs cron frágil

No hay una única redacción correcta. Lo que sigue es el conjunto de hallazgos que un análisis
**competente** cubre. **Excelente** = además articula la causa raíz y el caso del estado más dañino.

## Sección 1 — Modos de falla (el script deja el mundo roto o pierde trabajo)

| # | Qué pasa | Dónde | Garantía de durable execution que lo resuelve |
|---|---|---|---|
| 1 | El proceso muere durante el `time.sleep(6h)` (deploy, OOM, reinicio). Se reservaron fondos y nunca se transfiere; al volver, **no hay memoria** de la orden a medias. | paso 2 | **Reanudación por replay**: el motor reconstruye el estado y continúa donde quedó. El timer es **durable** (sobrevive el reinicio). |
| 2 | El proceso muere **entre transferir y notificar**. Transferiste el dinero y el proveedor nunca recibe el folio: estado inconsistente silencioso. | entre pasos 3 y 4 | **Reanudación por replay**: tras el crash, el workflow retoma en el paso 4 sin repetir la transferencia (que ya está en el historial). |
| 3 | El cron vuelve a disparar (o se solapan dos corridas). La misma orden se procesa de nuevo desde cero → **doble reserva y doble transferencia**. | `main()` / cron | **Idempotencia de workflow**: un `workflow_id` estable por pago hace que Temporal **rechace el duplicado**. (Y at-least-once + activities idempotentes evitan el doble efecto interno.) |
| 4 | El reintento `while True` pierde la cuenta de intentos si el proceso muere a mitad: el estado (`intentos`) vive solo en RAM. | paso 3 | **Reintentos con memoria**: la `RetryPolicy` de la activity persiste el progreso de reintentos en el historial; sobrevive crashes. |
| 5 | (extra) No hay registro paso a paso de en qué etapa va cada pago → depurar exige reconstruir desde logs sueltos. | todo | **Event history**: traza durable de cada paso (observabilidad de regalo). |

Causa raíz común (lo que marca "excelente"): **el estado del proceso —en qué paso voy, cuántos
reintentos llevo, qué timer corre— vive en la memoria de un proceso que puede morir.** El cron no
tiene memoria entre corridas; el script no tiene memoria tras un crash.

## Sección 2 — Violaciones de determinismo (romperían el replay)

Si se portara el cuerpo de `procesar_pago` tal cual al `run` de un workflow:

| Línea | Violación | Por qué rompe el replay | Alternativa correcta |
|---|---|---|---|
| `time.sleep(6 * 60 * 60)` | Sleep en proceso | Bloquea el worker y muere con él; en replay no es un timer registrado. | `await workflow.sleep(timedelta(hours=6))` (timer durable). |
| `requests.post(...)` / `requests.get(...)` | I/O de red dentro del workflow | Side effect no determinista: en replay no debe re-ejecutarse; su resultado debe leerse del historial. | Moverlo a una **activity** (`workflow.execute_activity(...)`). Doble falta: no determinista **y** side effect. |
| `datetime.now().isoformat()` | Reloj de pared | Da un valor distinto en cada replay → diverge del historial. | `workflow.now()`. |
| `random.uniform(...)` y `random.randint(...)` | Aleatoriedad | Distinto en cada replay. | `workflow.random()` (o `workflow.uuid4()` para el folio); o que el folio lo genere una activity. |

Causa raíz (excelente): el workflow **se re-ejecuta** durante el replay; cualquier cosa que cambie
entre corridas o toque el mundo debe salir del workflow (a una activity o a una API determinista de
`workflow`).

## Sección 3 — Frontera workflow / activity

**Activities** (tocan el mundo; reintentables; deben ser idempotentes):

- `pagos_pendientes()` → lee la API (en un workflow real suele ser el input, no una lectura interna).
- `reservar_fondos(monto)`
- `transferir(pago)`
- `notificar(proveedor, folio, ...)`

**Workflow** (orquesta; determinista; sin I/O):

- El orden de los pasos: reservar → esperar → transferir → notificar.
- La **espera** de 6 h como `workflow.sleep`.
- La **compensación** (si la transferencia falla definitivamente, liberar los fondos reservados).
- La generación de folio/marca de tiempo con APIs deterministas (`workflow.now`, `workflow.uuid4`) o
  delegada a una activity.

Punto fino (excelente): el `while True` de reintentos **desaparece** del código del workflow; se
reemplaza por una `RetryPolicy` en `workflow.execute_activity(transferir, ...)`. Reimplementar el
reintento a mano dentro del workflow es un anti-patrón: Temporal ya lo hace, con memoria y backoff.

## Rango de soluciones aceptables

- Cualquier conjunto de **≥4 modos de falla distintos** correctamente atribuidos cuenta como
  competente, aunque no use los mismos rótulos de garantía (siempre que la idea sea correcta).
- Para determinismo, **≥3 de las 4** violaciones con su alternativa = competente; las 4 + causa raíz
  = excelente.
- La frontera es aceptable mientras **ningún side effect** quede en el workflow y la orquestación no
  se modele como activity. Listar `pagos_pendientes` como input en vez de activity también es válido.
