# data-contracts-quality — Gate de calidad shift-left

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.5d` Data contracts + data quality/observability
**Ruta:** crítica · **Timebox:** 45 min (objetivo 25–45)

## 🎯 Objetivo

Implementar **a mano** el gate de calidad que decide, en el borde de entrada de un
pipeline, si un lote de datos cumple su **data contract**. No usas Great Expectations:
construyes el motor que hay detrás (un test = un predicado que cuenta filas malas; cero =
verde). Al terminar sabrás explicar la diferencia entre contract / test / observability y
por qué validar shift-left (en el borde) es más barato que validar antes del dashboard.

## 📋 Contexto

Un sistema externo te manda lotes de eventos de pago. El contrato `eventos_pago v1` (ya
definido en `gate.py`, NO lo cambies) declara el esquema, los valores válidos y las
garantías de freshness/volumen. Este ejercicio alimenta el **capstone de la Fase 7**: el
gate es la primera línea de defensa antes de que un dato malo contamine una decisión del
agente o el índice de un RAG.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento y feo.
2. Solo entonces, consulta la **documentación oficial**: <https://docs.greatexpectations.io/docs/core/introduction/> (para ver cómo lo hace una librería real).
3. **Solo al final**, usa IA para *revisar y explicar* tu solución — nunca para *generarla*.
4. Mañana, reescribe `validar_lote` **de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

### Parte obligatoria (nivel "competente")

Completa `_tipo_ok` y `validar_lote` en `gate.py` para detectar, acumulando **todas** las
violaciones (no cortes en la primera):

1. **campo_faltante** — fila a la que le falta un campo `requerido`.
2. **campo_extra** — fila con un campo **no** declarado en el contrato (schema drift).
3. **tipo** — valor presente cuyo tipo no calza (`string`/`number`/`datetime`).
4. **nulo** — campo `requerido` presente pero con valor `None`.
5. **duplicado** — campo `unico: true` con valores repetidos en el lote.
6. **valor_no_aceptado** — campo con `valores` que trae algo fuera de la lista.
7. **fuera_de_rango** — campo numérico con `min`/`max` que se sale.

Cada `Violacion` debe traer su `regla`, el `campo` y los **índices de filas** afectadas. El
gate pasa (`reporte.ok == True`) si y solo si no hay violaciones. Corre y deja en verde:

```bash
pip install pytest        # si no lo tienes
pytest -v
```

> **Cuidado con el orden:** si un campo es `None`, no evalúes su tipo ni su `min`/`max` (ya
> es una violación de `nulo`; evitas un `TypeError`). Recuerda: `True`/`False` **no** son
> `number` válidos.

### Parte de profundización (nivel "excelente" — hilos transversales)

8. **frescura** — si el contrato trae `garantias.frescura_horas`, valida que el `ts` (ISO
   8601) más nuevo no supere ese umbral respecto del parámetro `ahora`. (`datetime.fromisoformat`.)
9. **volumen** — si trae `garantias.volumen_min`/`volumen_max`, valida que `len(filas)` caiga en la banda.
10. **Observabilidad mínima** — usa/extiende `Reporte.resumen()` para exponer una métrica
    (`filas_totales`, `filas_rechazadas`, reglas violadas): la base de un evento de lineage.
11. **`WRITEUP.md`** (4–6 líneas): ¿por qué el gate va en el *borde* y no antes del dashboard?
    Conecta con RAG: ¿qué patología de tu gate, si se colara, produciría una **alucinación
    silenciosa**, y por qué no saltaría ningún error?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest -v` en verde (todos los casos de violación + el caso feliz).
- [ ] El gate **bloquea** (`ok == False`) cualquier lote con ≥1 violación y **pasa** un lote limpio.
- [ ] Cada `Violacion` identifica `regla`, `campo` y los **índices de filas** (no solo "falló algo").
- [ ] Agregaste **al menos un test propio** con un caso borde (p. ej. lote vacío, bool como number).
- [ ] Puedes **explicar sin notas**: contract vs test vs observability, y por qué shift-left es más barato.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Recorre el contrato, no el dato.** Para cada campo en `contrato["campos"]`, verifica esa
  regla sobre todas las filas: así obtienes `campo` y `filas` naturalmente.
- **Duplicados:** recolecta los valores del campo `unico`, cuenta con `collections.Counter`,
  y marca los índices cuyo valor aparece más de una vez.
- **Campo extra:** compara `set(fila)` contra `set(contrato["campos"])`. Lo que sobra es drift.
- **Tipo `number`:** `isinstance(v, (int, float)) and not isinstance(v, bool)` — porque en
  Python `True == 1` y `isinstance(True, int)` es `True`.
- Si un test `relationships`/regla falla, no "ajustes el dato para que pase": el gate está
  haciendo su trabajo. Lee la sección 4 de la lección `7.5d` antes de mirar nada más.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta, con `gate.py` completo + la salida de `pytest -v`),
- la **rúbrica**: `.ai/rubricas/fase-7/data-contracts-quality.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** (`.ai/soluciones/fase-7/data-contracts-quality/`) es material
del corrector — no la mires antes de intentarlo de verdad.
