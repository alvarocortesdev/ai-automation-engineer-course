# 2.6 — Suite pytest para un módulo de envíos (parametrize + fixture + mock en la frontera)

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.6` Testing: fundamentos
**Ruta:** crítica · **Timebox:** 40 min · **Modalidad:** código

## 🎯 Objetivo

Escribir una **suite de tests** completa (no el código bajo prueba, que ya existe)
para un módulo de tarifas de envío, usando `@pytest.mark.parametrize`, una
`@pytest.fixture` y `pytest.raises`, y mockeando **solo la frontera** (`tasa_usd`)
sin tocar la lógica pura (`costo_envio`). La prueba de que tu suite *sirve* es que
**caza dos mutantes** con bugs introducidos.

## 📋 Contexto

`solucion.py` es el **system under test (SUT)** y está correcto. `costo_envio` es
lógica pura (se verifica por su retorno); `cotizar` usa una dependencia inyectada
`tasa_usd` que en producción consultaría un servicio externo: esa es la **frontera**.
Esto es exactamente lo que harás en el **Capstone F2** sobre tu propia API: muchos
tests unit sobre la lógica, mockeando solo lo que cruza una frontera.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Calcula cada `esperado` **leyendo
   el SUT**, no adivinando ni ejecutando primero.
2. Solo entonces, consulta la [documentación oficial de pytest](https://docs.pytest.org/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbela de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `test_solucion.py` y completa los cuatro bloques marcados con `TODO`.
   **No modifiques `solucion.py`.**
2. Corre la suite hasta tener **verde**:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. **Autochequeo (obligatorio):** confirma que tu suite caza los bugs. Cambia,
   en `test_solucion.py`, la línea:

   ```python
   from solucion import costo_envio, cotizar
   ```

   por `from mutantes.mutante_a import costo_envio, cotizar`, corre `pytest` y
   confirma que tu suite se pone **ROJA**. Repite con `mutante_b`. Luego
   **revierte** el import a `solucion`. Si algún mutante deja tu suite en verde,
   te falta un caso borde.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La suite pasa **verde** contra `solucion.py` (no modificaste el SUT).
- [ ] Hay un `parametrize` con **≥5 casos**, incluyendo el borde peso entero vs.
      con decimales (p. ej. `2.0` vs `2.1`), una zona remota y un caso de socio.
- [ ] Hay un `pytest.raises(ValueError)` para el peso ≤ 0.
- [ ] Usaste una `fixture` para el doble de `tasa_usd`.
- [ ] `cotizar` se testea con la frontera mockeada y `costo_envio` **real** (no
      mockeado).
- [ ] Tu suite **caza los dos mutantes** (rojo con `mutante_a` y con `mutante_b`).
- [ ] Puedes explicar **sin notas** por qué mockeas `tasa_usd` pero no `costo_envio`.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `test_solucion.py` — tu suite, verde contra `solucion.py`.
- (Opcional) `notas.md` — qué mutante te costó más cazar y qué caso borde lo atrapó.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el borde del redondeo de kg: se cobra por kg **completo** (`ceil`), así que
`2.0` kg y `2.1` kg dan resultados distintos — ese par caza al `mutante_a` (que usa
`floor`). Para cazar al `mutante_b`, necesitas al menos un caso con `es_socio=True`
(el mutante olvida el descuento del 15%). Para `cotizar`, la fixture puede devolver
un stub `lambda: 950` o un `Mock(return_value=950)` si quieres afirmar que se llamó
con `tasa.assert_called_once()`. **No mockees `costo_envio`**: si lo haces, el test
de `cotizar` deja de probar el cálculo. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `test_solucion.py`**),
- la **rúbrica**: `.ai/rubricas/fase-2/pytest-suite-envios.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/pytest-suite-envios.md`
— no la mires antes de intentarlo de verdad.
