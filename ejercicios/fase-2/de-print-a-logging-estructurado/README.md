# 2.12 — De print-spam a logging estructurado

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.12` Debugging y código legado
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** código

## 🎯 Objetivo

Convertir la instrumentación amateur de un script legado (`print()` por todos lados)
en **logging estructurado profesional**: un logger por módulo, el **nivel** correcto
en cada mensaje (`debug`/`info`/`warning`), **contexto** en `extra=` (`pedido_id`,
`correlation_id`) y configuración **centralizada** con salida a `stdout`. Y poder
defender por qué `print` no sobrevive a producción.

## 📋 Contexto

`procesar_pedidos` funciona, pero "depura" con `print`: sin nivel, sin contexto, sin
forma de apagarlo. En tu máquina se ve útil; en un servidor es una linterna que se
quedó prendida y no puedes filtrar. Instrumentar con `logging` es lo que en la Fase 5
se vuelve **observabilidad** (logs/trazas/correlation IDs) y lo que te deja, en la
Fase 6, seguir la traza de un agente. Alimenta el **Capstone F2** (instrumentar tu
proyecto con logging, no print).

## 📏 Primero-Sin-IA

1. Hazlo **solo**, a mano (timebox arriba). Decide tú qué nivel va en cada mensaje.
2. Solo entonces, consulta el [HOWTO oficial de `logging`](https://docs.python.org/3/howto/logging.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar la solución*.
4. Mañana, **reescríbelo de memoria**. Si no te sale `getLogger(__name__)` + `extra=`, no lo aprendiste.

## 🛠️ Instrucciones

1. **Logger por módulo.** Crea `logger = logging.getLogger(__name__)` arriba (TODO 1).
   No lo configures ahí: un logger se **obtiene** en el módulo y se **configura** afuera.
2. **Reemplaza cada `print`** por la llamada de `logging` con el **nivel correcto**:
   - `logger.debug(...)` para el detalle interno (procesando / total calculado),
   - `logger.warning(...)` para la anomalía recuperable (pedido inválido omitido),
   - `logger.info(...)` para el ciclo de vida (pedido procesado).
3. **Contexto estructurado:** cada log lleva `extra={"pedido_id": <id>, "correlation_id": correlation_id}`.
4. **Configura una sola vez** (TODO 2 en `configurar_logging`): `StreamHandler` a
   `sys.stdout` con el nivel dado. Idealmente un formateador JSON (lección 4.6).
5. **Comprueba el off-switch:** con `configurar_logging(logging.INFO)` el `debug`
   desaparece **sin tocar la lógica**. Con `logging.DEBUG`, vuelve a aparecer.
6. **Escribe `por-que.md`** (máx. ½ página): 3 razones por las que `print` es un
   antipatrón de observabilidad en producción, y qué te da el logging estructurado
   que `print` no puede. Conéctalo con la observabilidad de la Fase 5.

Corre los tests hasta verde:

```bash
uv run pytest        # o simplemente:  pytest
```

> ⚠️ **No toques la lógica de negocio.** `cantidad * precio`, la validación y el
> valor de retorno se quedan igual. `test_logica_intacta` lo vigila: si lo rompes,
> te avisará. Solo cambias la **instrumentación**.

> 💡 Para que los tests (`caplog`) capturen tus logs, el logger debe **propagar**
> (es el default — no pongas `logger.propagate = False`).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **Cero** `print` en `solucion.py` (`test_no_quedan_prints` con `capsys` lo confirma).
- [ ] Cada log usa el **nivel** correcto y lleva `pedido_id` y `correlation_id` en `extra=`.
- [ ] El `DEBUG` se silencia con `configurar_logging(logging.INFO)` **sin** tocar las llamadas de log.
- [ ] El pedido inválido emite un `WARNING` (no un crash, no un `print`).
- [ ] `por-que.md` defiende niveles + contexto + routing + off-switch (no "queda más prolijo").
- [ ] Puedes explicar **sin notas** por qué un `print` en una librería que otros importan es un problema.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `solucion.py` — con logging estructurado y `configurar_logging` implementada.
- `por-que.md` — tu defensa de logging vs print (3 razones + qué resuelve).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`logger = logging.getLogger(__name__)` a nivel de módulo; **no** lo configures ahí.
El contexto va como dict en `extra=`; en un formateador JSON lo lees con
`getattr(record, "pedido_id", None)` para que no reviente si falta. En
`configurar_logging`: `handler = logging.StreamHandler(sys.stdout)` +
`logging.basicConfig(level=nivel, handlers=[handler])`. El `warning` del pedido
inválido es donde más se nota la diferencia con `print`: tiene nivel propio y se
puede alertar sobre él. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `por-que.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/de-print-a-logging-estructurado.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/de-print-a-logging-estructurado.md`
— no la mires antes de intentarlo de verdad.
