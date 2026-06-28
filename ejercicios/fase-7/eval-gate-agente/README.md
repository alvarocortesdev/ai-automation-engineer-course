# Ejercicio 7.7 — El eval gate de un agente

> **Modalidad: código (Primero-Sin-IA, timebox 40 min).** Construyes el gate que
> impide desplegar un agente que decide peor que el anterior. Sin red: las
> predicciones del agente y el golden set son listas/dicts que tú controlas.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.7` Agentes de automatización con IA
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Implementar el **eval gate** de un agente de automatización: dada una lista de predicciones del agente y un **golden set** (la categoría y los campos correctos anotados), medir la **accuracy de routing/clasificación** y la **exactitud de extracción**, y decidir si el despliegue **pasa o se bloquea** —por umbral fijo o por **regresión** respecto del baseline.

## 📋 Contexto

Es el punto 5 del Definition of Done del [capstone de la fase](/fase-7-automatizacion/proyecto/): eval harness versionado + número + gate de regresión. Para una automatización, la métrica que importa es la **decisión correcta**, no la fluidez del texto. Este gate corre en CI como los tests: igual que no mergeas con tests rojos, no despliegas un agente que decide peor que el de ayer.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta documentación oficial.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescribe de memoria** la diferencia entre umbral fijo y gate de regresión. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `eval_gate.py` e implementa `evaluar(...)` y `gate(...)` (no cambies sus firmas). El contrato está en el docstring.
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**. Cuidado con: la convención de lista vacía (verdad vacua → 1.0) y la **frontera** (accuracy igual al umbral **pasa**).
4. Añade al menos **un test propio** (sugerencia en el `TODO` al final del archivo).
5. Escribe `write-up.md` respondiendo:
   - (a) ¿Por qué para una **automatización** la métrica que importa es la accuracy de routing/extracción y no la fluidez del texto?
   - (b) ¿Por qué un gate de **regresión** (no solo un umbral fijo)? Da un escenario donde el umbral pasa pero la regresión debería bloquear.
   - (c) ¿De dónde sale un golden set realista, y por qué el eval offline (este gate) no reemplaza al monitoreo online en producción?
   - (d) Justifica la convención de lista vacía (1.0): ¿cuándo 0.0 sería más seguro?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `uv run pytest` pasa: accuracy y exactitud correctas en casos mixtos, lista vacía sin crash, gate por umbral y por regresión por separado.
- [ ] `gate` distingue "bajo umbral" de "regresión" en el `motivo`.
- [ ] La frontera (accuracy igual al umbral) **pasa**.
- [ ] Agregaste al menos un test propio.
- [ ] El `write-up.md` explica por qué la fluidez es la métrica equivocada para un agente de acción y de dónde sale el golden set.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `evaluar`: recorre `predicciones`, busca cada `input_id` en `esperado`,
cuenta aciertos de `categoria`; para los campos, suma sobre todas las claves
**esperadas** cuántas coinciden exactamente (numerador) y cuántas hay en total
(denominador). La exactitud es numerador/denominador global, no un promedio de
promedios. Para `gate`: dos chequeos separados con motivos distintos; la
regresión solo aplica si `baseline` no es `None`, y bloquea cuando la accuracy es
**estrictamente menor** que la del baseline. Revisa la sección 4.7 de la lección
antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, con `write-up.md`),
- la **rúbrica**: `.ai/rubricas/fase-7/eval-gate-agente.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/eval-gate-agente.md` — no la mires antes de intentarlo de verdad.
