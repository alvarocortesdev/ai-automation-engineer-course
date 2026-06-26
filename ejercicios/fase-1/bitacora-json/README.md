# 1.5 — Bitácora en JSON (round-trip robusto)

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.5` Archivos, JSON y APIs
**Ruta:** crítica · **Timebox:** 35–45 min · **Modalidad:** código

## 🎯 Objetivo

Implementar un módulo de **bitácora persistente** que carga registros de un archivo JSON,
agrega uno nuevo y vuelve a guardar — sin corromper los datos ni la codificación, y
manejando los casos borde (archivo inexistente, JSON corrupto).

## 📋 Contexto

Persistir datos en JSON es la forma más simple de que un programa "recuerde" entre ejecuciones,
y es el primer paso del **Capstone F1** (tu mini-API necesitará guardar y cargar estado). Aquí
entrenas el *round-trip* fiel y la decisión de ingeniería de **qué error se traga y cuál se propaga**.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta la **documentación oficial** de [`json`](https://docs.python.org/3/library/json.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `cargar`, `agregar` y `resumen` (no cambies las firmas).
   Las excepciones `BitacoraCorrupta` ya están definidas en el starter.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_solucion.py` (un caso borde que se te ocurra).

### Contrato de las funciones

- `cargar(ruta: str | Path) -> list` — devuelve la lista de registros.
  - Si el archivo **no existe** → devuelve `[]` (no es un error: es la primera vez).
  - Si existe pero el JSON es **inválido** → lanza `BitacoraCorrupta` (no un `JSONDecodeError` crudo).
- `agregar(ruta, mensaje: str) -> None` — carga, agrega `{"mensaje": mensaje}` al final de la lista,
  y guarda el resultado con `encoding="utf-8"`, `ensure_ascii=False` e `indent=2`.
- `resumen(registros: list) -> dict` — devuelve `{"total": n}` con la cantidad de registros.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El *round-trip* es fiel: `agregar` y recargar devuelve los mismos datos, con acentos/`ñ` intactos.
- [ ] Archivo inexistente → `cargar` devuelve `[]` sin reventar.
- [ ] JSON corrupto → `cargar` lanza `BitacoraCorrupta` (envolviendo el error original).
- [ ] Todos los tests pasan y agregaste al menos un caso propio.
- [ ] Puedes explicar **sin notas** por qué usas `encoding="utf-8"` y `ensure_ascii=False`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa el **contrato** primero: qué entra, qué sale, qué casos borde. `cargar` necesita dos
`except` distintos: `FileNotFoundError` → `return []`; `json.JSONDecodeError` →
`raise BitacoraCorrupta(...) from e`. `agregar` es `cargar` + `.append({"mensaje": mensaje})` +
guardar con `json.dump(..., ensure_ascii=False, indent=2)`. No reinventes la serialización: el
módulo `json` ya hace todo el trabajo. Revisa la sección 4.3 de la lección antes de mirar la
solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/bitacora-json.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/bitacora-json.md` — no la mires antes
de intentarlo de verdad.
