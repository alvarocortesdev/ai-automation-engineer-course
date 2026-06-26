# Diseño — POST /pagos idempotente

> Completa cada sección con tu razonamiento. Esto NO es una implementación: es el
> documento de diseño que defenderías ante un revisor senior. Sé concreto.

## 1. Esquema (ver `esquema.sql`)

Explica en 2–3 líneas tus decisiones de esquema: cuál es la columna que arbitra la
carrera, qué constraint usas y por qué, cuál es el alcance de la clave, y cómo
representas "en vuelo" vs "terminada".

> _(tu respuesta)_

## 2. Flujo paso a paso

### (a) Primer request con una clave nueva

> _(qué hace el servidor, en orden)_

### (b) Reintento de una operación que YA terminó (misma clave)

> _(qué devuelve y por qué no vuelve a cobrar)_

### (c) Dos requests concurrentes con la MISMA clave (la carrera)

> _(quién gana, qué le pasa al que pierde, y por qué tu diseño no cobra dos veces.
> Nombra el mecanismo que serializa la carrera.)_

## 3. Status HTTP por caso

| Caso | Status | Por qué |
|---|---|---|
| Primer request, cobro exitoso | | |
| Reintento de algo terminado | | |
| Misma clave aún "en vuelo" | | |
| Clave reusada con un body DISTINTO | | |

> Comenta especialmente el caso "en vuelo" y el de "misma clave, body distinto"
> (¿qué harías y por qué?).

## 4. Trade-off fail-open vs fail-closed

Si el banco no responde (timeout o circuit breaker abierto), ¿degradas (fail-open)
o propagas el error (fail-closed)? Justifica para ESTE endpoint de pago.

> _(tu respuesta)_

## 5. Dos preguntas de defensa (responde sin notas)

- ¿Por qué la idempotency key la genera el **cliente** y no el servidor?
- ¿Por qué "comprobar y luego actuar" (SELECT y después INSERT) abre una ventana
  de carrera que "INSERT-primero" cierra?

> _(tus respuestas)_
