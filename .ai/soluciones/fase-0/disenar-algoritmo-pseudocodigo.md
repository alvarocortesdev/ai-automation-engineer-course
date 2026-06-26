---
ejercicio_id: fase-0/disenar-algoritmo-pseudocodigo
fase: fase-0
sub_unidad: "0.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir y para calibrar pistas. Cualquier algoritmo correcto de una pasada (o incluso ordenar, con su trade-off comentado) es válido.

# Solución de referencia — Diseña un algoritmo preciso (y luego trázalo)

## Respuesta canónica

Algoritmo de **una sola pasada** ("mejor hasta ahora"):

```text
algoritmo archivo_mas_grande(archivos):
    si archivos está vacía:
        devolver NADA          # caso borde: carpeta vacía (decisión: None / aviso)

    mejor ← archivos[0]        # arranca como el primer archivo
    para cada archivo en archivos (desde el segundo):
        si archivo.tamaño > mejor.tamaño:     # ESTRICTO: el primero gana el empate
            mejor ← archivo
    devolver mejor.nombre
```

- **Caso borde — carpeta vacía:** se chequea **antes** del bucle y se devuelve un valor que signifique "no hay" (None, cadena vacía, o un aviso). Lo importante es que sea **explícito**, no que reviente en `archivos[0]`.
- **Regla de empate:** con `>` estricto, cuando un archivo iguala al máximo **no** reemplaza al actual ⇒ **gana el primero** que alcanzó ese tamaño. Con `>=` ganaría el último. Ambas son correctas; lo que se exige es que la regla esté **escrita** y sea consistente con la traza.

## Traza paso a paso (lista de ejemplo)

Lista: `[ ("notas.txt", 12), ("foto.jpg", 340), ("video.mp4", 1500), ("musica.mp3", 1500) ]`

| Archivo actual | Tamaño | ¿`> mejor`? | mejor hasta ahora |
|---|---|---|---|
| (inicio = archivos[0]) | — | — | (notas.txt, 12) |
| foto.jpg   | 340  | 340 > 12 ✓   | (foto.jpg, 340)  |
| video.mp4  | 1500 | 1500 > 340 ✓ | (video.mp4, 1500)|
| musica.mp3 | 1500 | 1500 > 1500 ✗ | (video.mp4, 1500) |

**Resultado:** `video.mp4`. El empate con `musica.mp3` **no** reemplaza al mejor porque `>` es estricto ⇒ gana el primero. (Con `>=` el resultado sería `musica.mp3`.)

## Por qué basta una sola pasada
Para encontrar un máximo no necesitas comparar todos contra todos ni ordenar: te alcanza con **recordar el mejor visto hasta ahora** y compararlo contra cada nuevo elemento. Recorres la lista **una vez**. Ordenar también funciona pero hace más trabajo del necesario (ordenar es más costoso que una pasada) — es un trade-off válido de mencionar, no un error.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Inicialización del "mejor".** Arrancar en 0 funciona aquí (tamaños positivos) pero es frágil; arrancar como `archivos[0]` o como centinela `-1` es más robusto. Penalizar solo si la inicialización **rompe** el primer caso.
2. **Orden diseño → traza.** Si la traza y el algoritmo no coinciden (la traza "corrige" pasos que el pseudocódigo no tiene), es señal de haber trazado primero. Pedir que reconcilie.
3. **`>` vs `>=` y el empate.** El error más común: escribir uno y trazar como el otro. Es la prueba de fuego de si entiende su propio diseño.
4. **Carpeta vacía silenciada.** Devolver `archivos[0]` sin chequear vacío es el bug clásico; debe manejarse **antes** del bucle.

## Rango de soluciones aceptables
- **Competente:** cualquier algoritmo de una pasada con "mejor hasta ahora", carpeta vacía manejada, regla de empate escrita, y traza consistente que devuelve `video.mp4` (o `musica.mp3` si declaró `>=`).
- **Excelente:** además inicialización justificada, comentario explícito de "una sola pasada", y la traza exponiendo el comportamiento del empate.
- **Aceptable con observación:** ordenar la lista y tomar el extremo —correcto en resultado; el corrector debe preguntar si vio la solución de una pasada y por qué elegiría una u otra (introduce el trade-off costo/simplicidad temprano).
- **No penalizar:** elegir devolver None vs. aviso vs. cadena vacía en el caso vacío (es decisión del alumno, mientras sea explícita).
