# Ejercicio 6.0 — Precision, recall y F1 desde una verdad de referencia

> **Modalidad: código (Primero-Sin-IA).** Implementas a mano el núcleo de un eval: las
> métricas con las que se mide si un sistema de IA sirve. Sin scikit-learn y sin IA hasta cerrar tu intento.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.0` Matemática mínima para IA
**Ruta:** crítica · **Timebox:** 35 min

## 🎯 Objetivo

Implementar, en Python puro, `contar` (TP/FP/FN), `precision`, `recall`, `f1` y un `evaluar`
que los componga, a partir de dos listas: etiquetas reales (`y_true`) y predicciones (`y_pred`).

## 📋 Contexto

En tu **Capstone F6 (Plataforma RAG)** uno de los entregables obligatorios es un *eval harness*
con un **número** que sube o baja entre versiones y bloquea un deploy si empeora (Definition of
Done, punto 5). Ese número son, casi siempre, estas métricas. Calcularlas a mano una vez es la
diferencia entre "confío en que la IA mejoró" y "el recall subió de 0.60 a 0.80, aquí está".

## 📏 Primero-Sin-IA

1. **Antes de programar**, escribe el contrato en 3 líneas: ¿qué entra?, ¿qué sale?, ¿qué casos borde hay?
2. Resuélvelo **solo**, a mano (timebox arriba). Calcula primero un ejemplo en papel.
3. Solo entonces consulta documentación (la definición oficial de precision/recall).
4. **Solo al final**, usa IA para *revisar y explicar* — nunca para *generar*.
5. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `metricas.py` y completa las cinco funciones (no cambies sus firmas).
2. Corre los tests:

   ```bash
   uv run pytest        # recomendado
   # o, si ya tienes pytest:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test borde tuyo** en `test_metricas.py` (ver el TODO al final del archivo).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] Sobre el ejemplo del RAG (TP=6, FP=4, FN=2): precision 0.60, recall 0.75, F1 ≈ 0.667.
- [ ] Los **denominadores cero** devuelven 0.0 en vez de lanzar `ZeroDivisionError`.
- [ ] `f1(1.0, 0.0)` devuelve `0.0` (entiendes por qué la media armónica, no el promedio).
- [ ] Agregaste al menos **un test propio**.
- [ ] Puedes **explicar sin notas** en qué problema priorizarías recall sobre precision (y al revés).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para `contar`, recorre `zip(y_true, y_pred)` y suma a tres contadores según el par: `(1,1)` es TP,
`(0,1)` es FP, `(1,0)` es FN (el cuarto caso, `(0,0)`, es TN y no se usa aquí). Para cada métrica,
el patrón del caso borde es el mismo: `return numerador / denominador if denominador else 0.0`.
Para `f1`, el denominador es `p + r`. Para `evaluar`, llama a `contar` y luego a las otras tres.
Repasa la sección "Idea 5 — Precision, recall y F1" de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/precision-recall-f1/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de intentarlo de verdad.
