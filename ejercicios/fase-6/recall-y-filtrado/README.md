# Ejercicio 6.6 — Recall de un índice + filtrado por metadata

> **Modalidad: código (Python puro, sin IA hasta cerrar tu intento).** No levantas
> ninguna base de datos: implementas las tres ideas que hacen funcionar (o fallar) a
> una vector DB, de forma determinista y offline. Es lo que un AI Engineer debe poder
> escribir y defender sin librería mágica.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.6` Vector databases
**Ruta:** crítica · **Timebox:** 45 min · **Modalidad:** código

## 🎯 Objetivo

Implementar, en `recall.py`, el motor conceptual de una vector DB:

1. **Búsqueda exacta** (fuerza bruta) como **ground truth**.
2. **`recall@k`**: la métrica que cuantifica cuánto se aleja un índice **aproximado**
   (ANN) de ese ground truth.
3. **Filtrado por metadata** con sus dos modos —**pre-filter** y **post-filter**— para
   ver con tus propias manos por qué el post-filter ingenuo es un bug de retrieval (y,
   con `tenant_id`, una fuga de datos).

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Reusa el coseno de 6.0/6.5.
2. Solo después consulta documentación oficial si te trabas.
3. Solo al final usa IA para *revisar y explicar*, no para *generar*.
4. Reescribe de memoria al día siguiente: si no puedes, no lo aprendiste.

## 🛠️ Instrucciones

Completa las cuatro funciones de `recall.py` (no cambies las firmas):

- `similitud_coseno(a, b)` — el coseno de siempre.
- `buscar_exacto(consulta, corpus, k)` — top-k `(indice, score)` por coseno, descendente.
- `recall_at_k(ids_aprox, ids_exactos)` — fracción de exactos encontrados; ground truth
  vacío → `1.0` (sin dividir por cero).
- `buscar_con_filtro(consulta, corpus, metadatas, where, k, modo)` — top-k respetando un
  filtro de metadata, en modo `"pre"` (filtra antes de rankear) y `"post"` (rankea el
  top-k global y luego descarta).

Corre los tests desde esta carpeta:

```bash
uv run pytest        # recomendado
pytest               # si ya tienes pytest en el entorno
```

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan (`pytest`).
- [ ] `recall_at_k` maneja el caso de ground truth vacío sin dividir por cero.
- [ ] `buscar_con_filtro` en modo `"post"` puede devolver **menos** de `k`; en `"pre"`
      devuelve hasta `k` que cumplen el filtro.
- [ ] Los índices devueltos son la **posición original** en `corpus`, no la del
      subconjunto filtrado.
- [ ] Agregaste **un test borde tuyo** (ideas en el `TODO` del archivo de tests).
- [ ] Puedes **explicar sin notas** por qué el post-filter puede devolver menos de `k` y
      por qué, cuando el filtro es `tenant_id`, eso es además un problema de seguridad.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/recall-y-filtrado/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** y tu comprensión (por qué el post-filter falla), no
solo si los tests están en verde. La solución de referencia vive en `.ai/soluciones/` —
no la mires antes de intentarlo de verdad.
