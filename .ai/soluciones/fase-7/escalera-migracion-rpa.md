---
ejercicio_id: fase-7/escalera-migracion-rpa
fase: fase-7
sub_unidad: "7.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Plan de migración de un RPA frágil

No hay una única redacción correcta. Lo que sigue es el conjunto de hallazgos que un plan
**competente** cubre. **Excelente** = además cuestiona el supuesto "no hay API" y articula el
trade-off honesto de migrar.

## Sección 1 — Diagnóstico (modos de falla)

| # | Qué se rompe | Línea / paso | Causa raíz |
|---|--------------|--------------|------------|
| 1 | El botón se mueve (rediseño, otra resolución, una barra de notificación) y el `click(820, 410)` cae en el vacío o en otro botón; el bot sigue tecleando. | `pyautogui.click(820, 410)` / `click(960, 720)` | Apunta a la **posición**, no al **significado**. |
| 2 | El `sleep(3)` es una apuesta: si la red va lenta, teclea antes de que exista el campo; si va rápida, desperdicia segundos por iteración. | `time.sleep(3)` / `time.sleep(2)` | Espera fija en vez de esperar al estado real (web-first). |
| 3 | Si el RUT ya existía y el portal muestra "duplicado", el bot clickea "Guardar" igual y continúa. Falla **silenciosa**. | tras `click(960, 720)` (no hay verificación) | No verifica el resultado de la acción. |
| 4 | Si el proceso se cae y se re-lanza desde el inicio, da de alta dos veces a los ya ingresados. | `main()` (sin registro de progreso) | No idempotente, sin reanudación. |
| 5 | (extra) RUT inválido se descarta con `continue` sin avisar; nadie sabe cuántos ni cuáles se saltaron. | `if not validar_rut(...): continue` | Ciego para operaciones (sin logs/traza). |

Peor estado (excelente): alta **duplicada** de proveedores, o registros válidos descartados en
silencio — invisible hasta que alguien reclama. Causa raíz común: el bot opera la **UI** (un contrato
que cambia sin avisar) por **posición**, y no observa el resultado de sus acciones.

## Sección 2 — Escalera por paso

| Paso del bot | Escalón | Restricción dominante |
|--------------|---------|-----------------------|
| `cargar_proveedores` | **código puro** (ya lo es) | Lee un CSV: no toca UI; queda en código. Primer corte natural. |
| `validar_rut` | **código puro** (ya lo es) | Lógica pura, testeable; no toca UI. Sale del bot hoy mismo. |
| `dar_de_alta` (abrir form, escribir, guardar) | **navegador** (escalón 2) | No hay API (supuesto), pero es **web** → navegador headless con selectores semánticos (`get_by_role`/`get_by_label`), no coordenadas. |
| (si apareciera una API del portal) | **api** (escalón 1) | Sería el salto correcto: `PUT /proveedores/{rut}` idempotente. |

Punto fino (excelente): cuestionar el supuesto "no hay API" — ¿quién lo confirmó? Conseguir aunque
sea un endpoint de alta convierte todo el paso web en una llamada idempotente. Y si el alta fuera
**crítica o de alto volumen**, lo correcto sería **presionar por esa API** antes de aceptar
automatizar la UI.

## Sección 3 — Plan Strangler Fig

1. **Corte 1 (hoy):** extraer `cargar_proveedores` y `validar_rut` a un módulo de código puro con
   tests. Son las piezas que no tocan UI: el corte más barato y seguro, sin tocar el portal.
2. **Instrumentar** el bot existente: log por proveedor (intentado/ok/error) + captura de pantalla al
   fallar. Necesitas medir antes de migrar.
3. **Corte 2:** reemplazar `dar_de_alta` (coordenadas) por un Page Object con Playwright (selectores
   semánticos + esperas web-first + verificación explícita de "guardado").
4. **En paralelo:** durante un periodo, correr viejo y nuevo sobre el mismo input y **comparar
   resultados** (mismos RUT dados de alta, mismas omisiones). Métrica de confianza: 0 discrepancias en
   N corridas, tasa de error igual o menor, latencia aceptable.
5. **Cortar** cuando la versión nueva iguala o supera a la vieja; retirar el bot por coordenadas.
6. (Opcional/objetivo) negociar una **API** y repetir el patrón: el navegador pasa a ser el "viejo".

Idempotencia y reanudación (de 7.2/7.3): registrar qué RUT ya se procesaron para no duplicar tras un
crash.

## Sección 4 — ADR (esqueleto) + BPMN

**ADR — migrar el alta de proveedores de RPA por coordenadas a navegador semántico**

- **Contexto:** bot por coordenadas + `sleep` fijos; se rompe con cada cambio del portal, falla en
  silencio y no es idempotente.
- **Decisión:** sacar la carga y validación a código puro; migrar `dar_de_alta` a Playwright con Page
  Object; mantener el bot viejo en paralelo hasta confiar; perseguir una API a futuro.
- **Alternativas:** (a) quedarse en coordenadas — insostenible; (b) reescribir todo de golpe — riesgo
  alto sin red; (c) exigir API antes de tocar nada — bloquea el valor inmediato.
- **Trade-off honesto (excelente):** ganamos robustez, verificación y testabilidad; **cuesta** tiempo
  de migración, operar un runtime de navegador, y perder la "visibilidad" visual del bot grabado.
  Migrar no es gratis.

**BPMN/carriles mínimo** (cualquier diagrama legible con actores por carril, tasks, un gateway de
"¿RUT existe/válido?" y eventos de inicio/fin, cuenta como competente).

## Rango de soluciones aceptables

- Cualquier conjunto de **≥4 modos de falla distintos** anclados a líneas concretas = competente.
- La escalera es aceptable mientras `dar_de_alta` (web sin API) vaya a **navegador** (no a RPA por
  coordenadas) y las piezas puras se reconozcan como el primer corte.
- El plan debe ser **incremental y reversible** (Strangler Fig). Un big-bang rewrite, aunque
  detallado, no es competente.
- El ADR es competente con contexto/decisión/alternativas/trade-off; excelente si el trade-off admite
  el costo real de migrar. El BPMN solo necesita comunicar el proceso, no ser exhaustivo.
