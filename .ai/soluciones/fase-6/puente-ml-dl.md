---
ejercicio_id: fase-6/puente-ml-dl
fase: fase-6
sub_unidad: "6.0b"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Las respuestas del alumno **no** tienen que coincidir palabra por palabra: lo que importa es que el modelo mental sea correcto y que el ejemplo calce con la definición.

# Solución de referencia — Defiende tus fundamentos (modo entrevista)

## Parte A — Respuestas canónicas (resumen de lo aceptable)

**1. Qué es un modelo.**
Una **función con parámetros (pesos) ajustables**: entra un input, salen números, y en medio hay pesos que **no se escriben a mano** sino que se ajustan a partir de datos. No es una base de datos de respuestas ni reglas `if/else`: los pesos codifican *patrones*. Por eso responde cosas que nunca vio exactas (y por eso alucina). Cualquier analogía de "cantidades de una receta afinadas cocinando mil veces" es válida.

**2. Entrenar vs inferir.**
- **Entrenar** = ajustar los pesos con muchos ejemplos (caro, una vez/pocas). Los pesos **cambian**.
- **Inferir** = usar los pesos **congelados** sobre un input nuevo (barato, cada llamada). Los pesos **no cambian**.
- Al llamar a una API de LLM, el alumno **infiere**. Punto clave aceptable: la "memoria" entre mensajes es la *context window* reenviada, **no** aprendizaje.

**3. Red neuronal.**
Pila de **capas** de neuronas; cada neurona = **producto punto** del input con un vector de pesos (+ bias) pasado por una **activación no lineal** (ReLU, etc.). El dot product de 6.0 es la operación central. La no linealidad es lo que permite aprender patrones complejos (no solo rectas). "Deep" = muchas capas. Entrenar = ajustar todos esos pesos con gradient descent.

**4. Overfitting y train/test split.**
**Overfitting** = el modelo memoriza el train set (incluido el ruido) en vez de aprender el patrón → brilla en train y falla en datos nuevos. Se separan **train** (para ajustar) y **test** (apartado, nunca visto en entrenamiento) para medir **generalización** honestamente. Medir en el train set sería mentirse (analogía del examen filtrado memorizado). La diferencia train−test es el *generalization gap*.

**5. Intuición de attention.**
Cada token **mira a todos los demás a la vez** y decide a cuáles atender según el contexto, asignando pesos (el "match" se calcula con producto punto: Query·Key, y se mezcla el Value). Ejemplo de ambigüedad: cualquiera propio (pronombre/referente). Dos ventajas: (a) relaciones a **larga distancia** sin memoria que se desvanece; (b) **se paraleliza** (todo el input a la vez) → entrenar modelos gigantes. NO es comprensión consciente: es ponderación aprendida.

**6. De dónde salen los embeddings.**
Son **parámetros aprendidos**. La embedding layer es una tabla token→vector que empieza **aleatoria** y se ajusta con gradient descent (como cualquier peso) para que el modelo prediga mejor; emerge que palabras/textos similares quedan cerca. Los embeddings de oraciones salen de pasar texto por un encoder entrenado para esa cercanía. **No se mezclan** embeddings de dos modelos: cada modelo define su propio espacio vectorial.

## Parte B — Diagnóstico (respuesta canónica)

| Modelo | Train | Test | Gap | Diagnóstico | Acción |
|---|---|---|---|---|---|
| A | 99% | 72% | **27** | **Overfitting** (gap enorme, train muy alto) | Más datos / regularización / early stopping. **NO** más épocas. |
| B | 70% | 68% | **2** | **Underfitting** (bajo en ambos, sin gap) | Modelo más rico / mejores features / entrenar más. |
| C | 94% | 91% | **3** | **Sano** (altos y cercanos) | Listo para validar en el mundo real; cuidar que el test no se haya "filtrado". |

**Cierre:** medir en el train set sería mentirse porque el modelo ya lo "vio" y pudo memorizarlo; el número reflejaría memoria, no capacidad de generalizar a datos nuevos. El test set es el examen limpio.

## Rango de respuestas aceptables
- **Competente** no exige las dos ventajas de attention ni la conexión Query·Key↔dot product; basta una ventaja + ejemplo propio coherente. Esos extras son **excelente**.
- Las analogías pueden ser cualesquiera mientras **calcen** con la definición. Una analogía bonita que contradice el concepto (p. ej. "entrenar es como buscar en Google") baja el nivel, no lo sube.
- En la Parte B se acepta cualquier redacción del gap mientras las **tres etiquetas** sean correctas y **justificadas por la relación entre train y test**, no por un número aislado.
- Si el alumno reutiliza el ejemplo del trofeo en attention, marca C4 en-progreso (el enunciado pedía uno propio) aunque la definición sea correcta.

## Puntos donde el corrector debe mirar con lupa
1. **Inferencia no cambia pesos.** Es la frase bisagra. Si falta o está mal, casi todo el resto del mapa mental se contagia.
2. **Embedding = vector aprendido.** Si lo trata como propiedad fija del texto, no entendió de dónde sale (y no podrá justificar por qué no se mezclan).
3. **Diagnóstico por gap, no por número suelto.** "A es bueno porque 99%" es el error clásico.
4. **Antropomorfizar attention.** "Entiende" es bandera roja; "pondera según contexto" es la respuesta de ingeniero.
