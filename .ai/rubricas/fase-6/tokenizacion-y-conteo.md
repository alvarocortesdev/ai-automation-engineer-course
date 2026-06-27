---
ejercicio_id: fase-6/tokenizacion-y-conteo
fase: fase-6
sub_unidad: "6.1"
version: 1
---

# Rúbrica — Tokenización: predice y verifica con un tokenizer real

> Rúbrica analítica para un ejercicio **mixto**. Lo central es el **proceso**:
> ¿predijo antes de medir? ¿la reflexión nombra la idea de fondo equivocada, o solo
> "fallé un número"? Un alumno puede tener la función correcta y aun así no haber
> aprendido nada si saltó la predicción. La rúbrica distingue ambos casos.

## Objetivos evaluados
- **O1** — Predecir el orden relativo de tokens sin ejecutar.
- **O2** — Implementar `contar_tokens` con tiktoken (offline).
- **O3** — Diagnosticar la propia intuición (predicción vs realidad).

## Criterios y niveles

### C1 — Corrección de la predicción (proceso) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay `prediccion.md`, o claramente se escribió después de medir (los conteos "predichos" coinciden exactos con los reales, incluido el emoji). |
| **en-progreso** | Predice un orden pero sin razonamiento, o con un malentendido sistemático (cree que el emoji es 1 token, que el espacio no cuenta, que el código es barato). |
| **competente** | Orden razonable con una línea de razonamiento por cadena; acierta las relaciones gruesas (palabra larga > palabra común; código alto). |
| **excelente** | Además anticipa los puntos resbalosos (acentos del español = más bytes = más tokens; el emoji cuesta varios; el espacio viaja pegado a la palabra). |

### C2 — Calidad de ingeniería (la función + tests) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `contar_tokens` no implementada o lanza error; tests en rojo. |
| **en-progreso** | Funciona para el caso general pero falla el borde (string vacío != 0), o reimplementa el conteo a mano en vez de usar `encode`. |
| **competente** | Implementación limpia con `tiktoken` (`len(encode(...))`), string vacío = 0, todos los tests verdes. |
| **excelente** | Además añadió un test propio significativo (otro borde / otra codificación) y/o usó `ver_tokens` para inspeccionar el split. |

### C3 — Comprensión demostrada (la reflexión) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `verificacion.md`, o no compara con la predicción. |
| **en-progreso** | Compara pero la reflexión es superficial ("me equivoqué en un número") sin nombrar la idea de fondo. |
| **competente** | Nombra con precisión una idea equivocada de fondo (p. ej. "creía que 1 palabra = 1 token" o "no esperaba que ñ/í costaran tanto"). |
| **excelente** | Convierte el error en una regla reutilizable ("para estimar costo en español, asumo más tokens por carácter que en inglés") y conecta con el costo/context window. |

## Errores típicos a marcar
- **Medir antes de predecir** (o escribir la "predicción" copiando los conteos reales): invalida O1 aunque el código sea perfecto.
- **String vacío != 0**: olvidar que `encode("")` devuelve lista vacía.
- **Reimplementar el conteo** (contar palabras, contar caracteres / 4) en vez de usar `encode`: no es lo que mide el objetivo.
- **Confundir tiktoken con "el tokenizer de todos los modelos"**: no notar que es de OpenAI y que Claude/Gemini tokenizan distinto.
- (transversal costo) No conectar el conteo con la factura ni con el límite de context window.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Predicción con números exactos idénticos a los reales (incluido el emoji y el español) — improbable a mano; sugiere que se ejecutó o se pidió a la IA primero.
- Reflexión genérica que no menciona ni acentos, ni espacios, ni código — como si no hubiera mirado las 6 cadenas concretas.
- **Verificación sugerida:** pedir que prediga, sin ejecutar, el orden de dos cadenas nuevas (p. ej. `"OpenAI"` vs `"こんにちは"`). Si entendió, razona el porqué; si dependió de la IA, se traba.

## Feedback sugerido (graduado)
> Nunca dar los conteos exactos antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Mira tu `ver_tokens` sobre la cadena del emoji y sobre la del español. ¿Cuántos pedazos salen? ¿Calza con lo que predijiste?"
- **Pregunta socrática (nivel 2):** "¿Por qué un carácter acentuado costaría más que una letra ASCII? Pista: piensa en bytes, no en letras."
- **Dirección concreta (nivel 3, solo tras intento real):** "La idea a corregir es 'tokens = palabras'. El tokenizer trabaja sobre bytes/sub-palabras: lo raro y lo no-ASCII se parte en más piezas. Reescribe tu reflexión nombrando esa idea y conéctala con por qué el español cuesta más en la factura."

## Conexión con el proyecto / capstone
- Contar tokens es la base del **presupuesto de costo** y del **chunking** del Capstone F6 (Plataforma RAG): sin entender esto, no se puede estimar cuánto cuesta una consulta ni por qué hay que trocear los documentos.
