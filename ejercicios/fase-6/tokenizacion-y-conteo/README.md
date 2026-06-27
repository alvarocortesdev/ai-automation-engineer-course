# Ejercicio 6.1 — Tokenización: predice y verifica con un tokenizer real

> **Modalidad: mixto (a mano + código).** Primero predices a mano, sin ejecutar ni
> usar IA. Luego escribes la función que mide de verdad. El objetivo no es acertar
> los números: es **destruir la intuición de que 1 palabra = 1 token** con
> evidencia que tú mismo generaste.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.1` Fundamentos de LLMs
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O1** — Predecir el orden relativo de tokens de varias cadenas, **sin ejecutar**.
- **O2** — Implementar una función que cuente tokens con `tiktoken` (offline).
- **O3** — Diagnosticar tu propia intuición: comparar predicción vs realidad y
  nombrar la idea equivocada de fondo.

## Las 6 cadenas a analizar

```text
(a) "hello world"
(b) "antidisestablishmentarianism"
(c) "  "                                  (dos espacios)
(d) "def suma(a, b): return a + b"
(e) "El murciélago ñoño comió crème brûlée"
(f) "🎂🎂🎂"
```

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~15 min

En un archivo `prediccion.md`:

1. **Ordena** las 6 cadenas de **menos** a **más** tokens, según tu intuición.
2. Para cada cadena, escribe **una línea** de razonamiento (por qué crees que cuesta
   pocos o muchos tokens).
3. **No ejecutes nada todavía** y no uses IA. El valor está en predecir primero.

### Parte 2 — Código (verificación), ~20 min

1. Abre `tokenizador.py` y completa la función `contar_tokens(texto, codificacion)`
   (no cambies su firma). Usa la librería `tiktoken`.

   Instalación (una vez): `pip install tiktoken` (o `uv add tiktoken`).

   > La **primera** ejecución descarga el vocabulario de la codificación y lo
   > cachea; necesita internet solo esa vez. Después funciona offline.

2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`: pega los conteos reales de las 6 cadenas (puedes usar tu
propia función o `python -c "..."`), pon el orden real, y compáralo con tu
predicción. Responde en 2–3 frases: **¿qué idea equivocada tenías?** (no "fallé un
número" — la idea de fondo: ¿pensabas que el espacio no contaba? ¿que el emoji era
1 token? ¿que el código era barato?).

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — orden predicho + razonamiento, **antes** de ejecutar.
- `tokenizador.py` — con la función completada (los tests pasan).
- `verificacion.md` — conteos reales + comparación + idea equivocada.
- (opcional) un test propio añadido en `test_tokenizador.py`.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con orden + razonamiento por cadena.
- [ ] Todos los tests pasan.
- [ ] `verificacion.md` compara predicción vs realidad y nombra una idea de fondo
      equivocada.
- [ ] Puedes **explicar sin notas** por qué el español/código cuesta más tokens
      que el inglés equivalente.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/tokenizacion-y-conteo/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir? ¿la reflexión
nombra la idea de fondo?), no solo si el número final cuadra.
