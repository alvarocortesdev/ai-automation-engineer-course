# Ejercicio 0.2 — Diseña un algoritmo preciso (y luego trázalo)

> **Modalidad: a mano (pseudocódigo, sin IA, sin ejecutar).** Aquí ejercitas la cuarta herramienta: convertir un problema en una **secuencia de pasos sin ambigüedad**. No escribes Python ni TypeScript: escribes el *algoritmo*, que es independiente del lenguaje. Después lo **trazas a mano** para comprobar que funciona —el puente directo a la sub-unidad **0.3 · Notional machine y trazado a mano**.

## Objetivos

- **O1** — Diseñar un algoritmo en pseudocódigo que resuelva un problema concreto **sin pasos ambiguos**.
- **O2** — Anticipar y manejar **casos borde** en el diseño (no después de que rompe).
- **O3** — **Trazar a mano** el propio algoritmo sobre datos de ejemplo para verificar que produce el resultado correcto.

## El problema

> Diseña el algoritmo de una herramienta pequeña: **"encontrar el archivo más grande dentro de una carpeta"**.

Entrada: una lista de archivos, cada uno con `nombre` y `tamaño` (en KB).
Salida: el nombre del archivo más grande.

## Tu tarea (en este orden — Primero-Sin-IA, timebox 30 min)

A mano, sin IA, sin ejecutar:

1. **Diseña el algoritmo** en pseudocódigo. Usa lenguaje preciso ("recorre cada archivo", "si... entonces...", "devuelve..."). Cada paso debe ejecutarse igual sin importar quién lo lea.
2. **Maneja los casos borde** *dentro* del diseño:
   - **Carpeta vacía:** ¿qué devuelve si no hay archivos? Decídelo tú y déjalo explícito.
   - **Empate:** si dos archivos tienen el tamaño máximo, ¿cuál ganas? Cualquier regla sirve, pero tiene que estar **escrita** (no "el que sea").
3. **Traza a mano** tu algoritmo sobre esta lista de ejemplo, mostrando cómo cambia tu variable "mejor hasta ahora" en cada paso:

   ```text
   [ ("notas.txt", 12), ("foto.jpg", 340), ("video.mp4", 1500), ("musica.mp3", 1500) ]
   ```

   Haz una **tabla de traza**: una fila por archivo, columnas para `archivo actual`, `tamaño`, `mejor hasta ahora`.

## Qué entregar

Completa `PLANTILLA-RESPUESTA.md` (en esta carpeta) o crea:

- `algoritmo.md` — el pseudocódigo con los dos casos borde explícitos.
- `traza.md` — la tabla de traza sobre la lista de ejemplo + el resultado final.

> Diseña **antes** de trazar. Si trazas primero y ajustas el algoritmo para que "dé bien", te saltas el aprendizaje: el objetivo es que tu diseño sea correcto *por construcción*.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El pseudocódigo no tiene pasos ambiguos (dos personas lo ejecutarían igual).
- [ ] El caso **carpeta vacía** está manejado explícitamente.
- [ ] La regla de **empate** está escrita (no "el que sea").
- [ ] La **tabla de traza** muestra `mejor hasta ahora` en cada paso y llega al resultado correcto.
- [ ] Puedes explicar **por qué** tu algoritmo solo necesita recorrer la lista **una vez**.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-0/disenar-algoritmo-pseudocodigo/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisa que tu **diseño sea correcto por construcción** y que tu traza coincida con él —no si memorizaste una respuesta. La **solución de referencia** vive en `.ai/soluciones/` — no la mires antes de intentarlo de verdad.
