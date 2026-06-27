---
ejercicio_id: fase-4/especificidad-cascada-a-mano
fase: fase-4
sub_unidad: "4.1"
version: 1
---

# Rúbrica — Especificidad y box model a mano

> Rúbrica analítica para un ejercicio **a-mano**. Lo que se evalúa es el **proceso de razonamiento** (la tabla de especificidad y el cálculo del box model), no solo si los colores finales coinciden. Un alumno puede acertar un color por intuición y seguir sin entender la cascada; otro puede errar y tener el modelo casi correcto. La rúbrica distingue ambos casos.

## Objetivos evaluados
- **O1** — Predecir el color final aplicando especificidad y, ante empate, el orden de origen.
- **O2** — Calcular el ancho total de una caja en `content-box` y en `border-box`.
- **O3** — Diagnosticar el propio error (predicción vs. DevTools).

> Resultados correctos: primer `<p class="intro">` queda **green** (empate `(0,1,1)` entre `.post p` y `main .intro`, lo rompe el orden: `main .intro` va después). Segundo `<p>` queda **orange** (`.post p` `(0,1,1)` es el más específico que lo toca). Ancho del `.post`: **600px** en `border-box`; **652px** en `content-box`. El corrector lo sabe; **no se lo dice al alumno** salvo al cerrar, y nunca como atajo que evite la tabla.

## Criterios y niveles

### C1 — Corrección de los colores predichos · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay predicción, o se "predijo" tras abrir el navegador (la predicción es lo que vio en DevTools). |
| **en-progreso** | Predice colores con razonamiento, pero erra por un malentendido sistemático (cree que gana el último escrito, o no detecta el empate). |
| **competente** | Predice **green** y **orange** con razonamiento coherente, aunque alguna terna `(a,b,c)` tenga un desliz menor. |
| **excelente** | Predice ambos y además **nombra explícitamente el empate** `(0,1,1)` del primer `<p>` y por qué el orden lo desempata a favor de `main .intro`. |

### C2 — Calidad de la tabla de especificidad · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla, o solo el color final sin las ternas. |
| **en-progreso** | Tabla parcial o con conteo equivocado (p. ej. cuenta `article p` como `(0,1,0)` confundiendo tipo con clase). |
| **competente** | Las cinco ternas correctas: `p`=(0,0,1), `article p`=(0,0,2), `.intro`=(0,1,0), `.post p`=(0,1,1), `main .intro`=(0,1,1). |
| **excelente** | Además explica la comparación columna a columna (que `b` pesa más que `c`, que un empate total se va al orden). |

### C3 — Box model en ambos modos · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No calcula anchos, o da uno solo sin distinguir los modos. |
| **en-progreso** | Calcula uno bien y el otro mal (típico: olvida sumar el border, o suma el margin al ancho de la caja). |
| **competente** | **600px** en border-box y **652px** en content-box, con la aritmética visible (600 + 24·2 + 2·2). |
| **excelente** | Además aclara que el `margin: 0 auto` **no** entra en el ancho de la caja (es espacio externo) y que en border-box el *content* se encoge a 548px. |

### C4 — Diagnóstico del propio error (metacognición) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No verificó con DevTools, o no hay `reflexion.md`. |
| **en-progreso** | Verificó, pero la reflexión es superficial ("me equivoqué en un color") sin nombrar la idea de fondo. |
| **competente** | Nombra con precisión la idea equivocada (p. ej. "creía que ganaba el último", "olvidé el border") y la liga a la regla. |
| **excelente** | Convierte el error en regla reutilizable ("cuando dos reglas empatan en `(a,b,c)`, recién ahí miro el orden"). |

## Errores típicos a marcar
- **"Gana el último"**: aplicar el orden de origen antes de comparar especificidad. Solo desempata cuando `(a,b,c)` es idéntico.
- **No detectar el empate** del primer `<p>` entre `.post p` y `main .intro` (ambos `(0,1,1)`): predice uno sin justificar por qué, por suerte.
- **Confundir tipo con clase** al contar: `article p` son dos **tipos** `(0,0,2)`, no clases.
- **Box model**: olvidar multiplicar padding/border por 2 (son dos lados), o **sumar el margin** al ancho de la caja (el margin es externo, no cuenta).
- **Olvidar el efecto de `border-box`**: dar 652px aunque el `box-sizing: border-box` esté presente.
- **Verificar antes de predecir**: invalida O1 aunque el resto esté impecable.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- `prediccion.md` con los colores correctos pero **sin tabla de ternas**, o con una tabla que no podría haber producido ese razonamiento.
- Reflexión genérica que no menciona ni la especificidad ni el border, como si no hubiera trazado el código concreto.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, qué pasa si se **agrega** `#contenido p { color: red; }` al CSS, o el ancho de una caja con `width: 320px; padding: 8px; border: 4px` en ambos modos. Si trazó de verdad, lo resuelve; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar los colores ni los anchos antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Para el primer `<p>`, dos de tus reglas tienen la misma terna. ¿Cuál? Solo cuando empatan se mira el orden."
- **Pregunta socrática (nivel 2):** "¿Cuántos ids, clases y tipos tiene `.post p`? ¿Y `main .intro`? Compáralas columna por columna. Y para la caja: ¿el `width` incluye el border en el modo que está activo?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Arma la tabla `(a,b,c)` de las cinco reglas y subraya el empate `(0,1,1)`; recién ahí aplica el orden. Para el box model, suma `padding·2 + border·2` solo en `content-box`; en `border-box` el total es el `width` tal cual."

## Conexión con el proyecto / capstone
- Predecir la cascada a mano es el músculo que evita la "guerra de `!important`" en el **Capstone F4**: cuando un estilo de tu app React "no se aplica", sabrás que es especificidad y lo depuras en segundos en vez de parchear a ciegas.
