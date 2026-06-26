# Mi respuesta — Diseño de algoritmo + traza

## 1. Algoritmo (pseudocódigo)

> Escribe los pasos sin ambigüedad. Maneja los dos casos borde DENTRO del diseño.
> Borra estas instrucciones al completar.

```text
algoritmo archivo_mas_grande(archivos):
    # caso borde — carpeta vacía:
    si ... :
        devolver ...

    mejor ← ...        # tu "mejor hasta ahora" inicial
    para cada archivo en archivos:
        si ... :        # ¿cuándo el actual supera al mejor?
            mejor ← ...
    devolver mejor.nombre
```

**Regla de empate (escrita, no "el que sea"):**

- Si dos archivos tienen el tamaño máximo, gana: ...  *(porque ...)*

**Qué devuelve con carpeta vacía:** ...

---

## 2. Traza a mano

> Lista de ejemplo:
> `[ ("notas.txt", 12), ("foto.jpg", 340), ("video.mp4", 1500), ("musica.mp3", 1500) ]`

| Archivo actual | Tamaño | ¿Supera al mejor? | mejor hasta ahora (nombre, tamaño) |
|---|---|---|---|
| (inicio)       | —      | —                 | ...                                |
| notas.txt      | 12     | ...               | ...                                |
| foto.jpg       | 340    | ...               | ...                                |
| video.mp4      | 1500   | ...               | ...                                |
| musica.mp3     | 1500   | ...               | ...                                |

**Resultado final:** ...

**¿Por qué basta recorrer la lista una sola vez?** ...
