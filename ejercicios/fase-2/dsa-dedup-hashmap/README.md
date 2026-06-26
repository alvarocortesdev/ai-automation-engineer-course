# Ejercicio 2.1 — De O(n²) a O(n): two-sum con hashmap

> **Modalidad: código (Primero-Sin-IA).** Este ejercicio mide la jugada central de DSA a nivel de
> trabajo: tomar una solución obvia O(n²) y bajarla a O(n) cambiando tiempo por memoria con un `set`.
> Lo que se evalúa no es solo que pase los tests, sino que **puedas defender la complejidad**.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.1` DSA a nivel de trabajo
**Ruta:** crítica · **Timebox:** 30–40 min

## 🎯 Objetivo

Implementar `tiene_dos_que_suman(nums, objetivo)` en **O(n)** usando un `set`, y justificar por qué
mejora a la versión obvia O(n²) con bucle anidado, nombrando el trade-off de espacio.

## 📋 Contexto

Es el problema "two-sum" en su forma booleana: el ejemplo más limpio del patrón hashmap, el que
convierte "comparar todos con todos" en "recordar lo que ya viste". El mismo salto reaparece en la
Fase 3 como el **problema N+1** de los ORMs. Aprende a verlo aquí, en diez líneas.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que el primer intento sea el O(n²).
2. Solo entonces, consulta **documentación oficial** (la tabla de complejidades de Python).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa `tiene_dos_que_suman` (no cambies su firma).
2. La disciplina, en este orden (red-green-refactor):
   - Primero escribe la versión **obvia** con bucle anidado en papel y anota su Big-O.
   - Luego, **sin IA**, encuentra la versión O(n): por cada `x`, pregunta si ya viste su complemento
     `objetivo - x`.
   - Entrega solo la versión O(n) en `solucion.py`.
3. Escribe tus tests **antes** de la implementación final y córrelos:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

4. Itera hasta verde. Añade al menos **un caso borde tuyo** en `test_solucion.py`.
5. Escribe `NOTAS.md` (4–6 líneas): Big-O de **ambas** versiones (tiempo y espacio) y por qué el `set`
   baja el tiempo.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Pasan los casos del enunciado más un caso borde tuyo.
- [ ] La versión entregada es **O(n) en tiempo** (un solo bucle, lookups en `set`).
- [ ] `NOTAS.md` justifica el trade-off: tiempo O(n²)→O(n) a costa de espacio O(1)→O(n).
- [ ] Puedes **explicar sin notas** por qué el lookup en `set` es O(1) amortizado.

### Casos que tu solución debe respetar

| `nums` | `objetivo` | esperado | por qué |
|---|---|---|---|
| `[2, 7, 11, 15]` | `9` | `True` | 2 + 7 |
| `[3, 3]` | `6` | `True` | dos posiciones distintas, aunque el valor se repita |
| `[1]` | `2` | `False` | hace falta **dos** posiciones |
| `[]` | `0` | `False` | no hay elementos |
| `[1, 5, 9]` | `8` | `False` | ningún par suma 8 |

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No compares pares: recorre una sola vez con un `set` `vistos`. Para cada `x`, **antes** de agregarlo,
pregunta `if (objetivo - x) in vistos: return True`. Si el complemento no apareció aún, agrega `x` y
sigue. El orden (preguntar antes de agregar) evita emparejar un elemento consigo mismo. Verifica a
mano que `[3, 3]` con objetivo `6` da `True`. Revisa la sección 4.2 de la lección antes de mirar la
solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, incluido `NOTAS.md`),
- la **rúbrica**: `.ai/rubricas/fase-2/dsa-dedup-hashmap.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/dsa-dedup-hashmap.md` — no la mires antes
de intentarlo de verdad.
