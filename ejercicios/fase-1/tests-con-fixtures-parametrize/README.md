# 1.6 — Diseñar tests con fixtures y parametrize

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.6` Primer test unitario con pytest
**Ruta:** crítica · **Timebox:** 30–40 min · **Modalidad:** código

## 🎯 Objetivo

Escribir la suite de tests de un módulo **ya implementado y correcto** (`agenda.py`),
aplicando las tres herramientas que separan un test plano de un buen test:
`tmp_path` (aislar el disco), `@pytest.fixture` (datos reutilizables) y
`@pytest.mark.parametrize` (muchos casos sin repetir).

## 📋 Contexto

Aquí no escribes lógica: **diseñas tests**. Te damos `agenda.py` —una mini-agenda
persistida en JSON— y tú escribes `test_agenda.py`. Saber testear *código ajeno y
correcto* es exactamente lo que harás en la Fase 2 (refactor con red de tests) y en
todo capstone. El reto real no es "que pase": es que tus tests sean **aislados**
(no dejan basura, no dependen del orden) y **expresivos** (cada caso se lee solo).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba).
2. Solo entonces, consulta la documentación oficial de [pytest](https://docs.pytest.org/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Lee `agenda.py` (no lo modifiques) para entender el contrato de sus funciones.
2. Abre `test_agenda.py`. Hay una **semilla** (el round-trip con `tmp_path`). Córrela:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

   Debería pasar en **verde** (el módulo es correcto). Tu trabajo es agregar el resto.
3. Completa los `TODO` hasta cubrir todo lo de la lista de abajo.

### Lo que tu suite debe cubrir (mínimo)

| Caso | Herramienta clave |
|---|---|
| `guardar_eventos` + `cargar_eventos` devuelven los mismos datos | `tmp_path` |
| `cargar_eventos` de una ruta inexistente devuelve `[]` | `tmp_path` (ruta que no creas) |
| `cargar_eventos` de un archivo con texto no-JSON lanza `AgendaCorrupta` | `pytest.raises` + `tmp_path` |
| `proximos(eventos, hoy)` con varios `hoy` y su salida esperada | `@pytest.mark.parametrize` |
| eventos de ejemplo reutilizados en ≥ 2 tests | `@pytest.fixture` propia |

> 💡 Las fechas son strings `"YYYY-MM-DD"`: su orden como texto coincide con el
> cronológico, así que `proximos` filtra con `>=` sobre strings. Eso te simplifica
> los valores esperados de tus casos parametrizados.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Usas `tmp_path` para **todo** lo que toca disco (cero archivos creados en el repo).
- [ ] Extraes los datos de ejemplo a una `@pytest.fixture` y la reutilizas en ≥ 2 tests.
- [ ] Comprimes los casos de `proximos` con `@pytest.mark.parametrize`.
- [ ] El caso corrupto usa `pytest.raises(AgendaCorrupta)`.
- [ ] Todos los tests pasan y agregaste al menos un caso borde propio.
- [ ] Puedes explicar **sin notas** por qué `tmp_path` evita tests frágiles.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el archivo inexistente, **no crees** el archivo: `ruta = tmp_path / "no_existe.json"`
y verifica `cargar_eventos(ruta) == []`. Para el corrupto, escribe basura primero:
`ruta.write_text("{roto", encoding="utf-8")` y luego `with pytest.raises(AgendaCorrupta): cargar_eventos(ruta)`.
La fixture es solo `@pytest.fixture` sobre una función que `return`-a tu lista de eventos;
la pides poniendo su nombre como parámetro del test. Para `proximos`, parametriza
`(hoy, titulos_esperados)` y compara los títulos en orden. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `test_agenda.py`**),
- la **rúbrica**: `.ai/rubricas/fase-1/tests-con-fixtures-parametrize.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/tests-con-fixtures-parametrize.md` —
no la mires antes de intentarlo de verdad.
