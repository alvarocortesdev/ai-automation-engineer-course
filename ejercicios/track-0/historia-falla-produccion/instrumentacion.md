# Instrumentación — [tu app]

> Reemplaza TODO el contenido de ejemplo por lo tuyo. Esto demuestra que tu app
> está **observada**: sin instrumentación no hay detección, y sin detección el
> único que te avisa del fallo es el usuario.

## La app y sus usuarios reales

- **App:** _[nombre + 1 línea de qué hace]_
- **Usuarios reales (mínimo 3):** _[quiénes — p. ej. "mi pareja y dos amigos que la usan para X"]_
- **¿La usan de verdad?** _[con qué frecuencia / desde cuándo]_

> Si AÚN no tienes usuarios o instrumentación, no finjas: escribe aquí el **plan
> concreto** para tenerlos esta semana (a quién se la das, qué log/alerta agregas y
> cuándo). Ser honesto sobre el "todavía no" es parte del ejercicio.

## Log estructurado (ejemplo de una línea real)

> Una línea JSON por request, con un identificador para correlacionar. Pega una
> línea real de tus logs (anonimiza datos sensibles).

```json
{"ts":"2026-06-13T14:02:11-04:00","level":"error","request_id":"a1b2c3","route":"POST /shopping-list/items","status":500,"user":"u_42","msg":"write failed: container shutting down"}
```

## Alerta(s) activa(s)

| Alerta | Condición que la dispara | Por dónde me llega |
|--------|--------------------------|--------------------|
| _[ej. Write-path 5xx]_ | _[ej. tasa de 5xx en POST de escritura supera el umbral en 5 min]_ | _[ej. mensaje a mi teléfono]_ |

## Reflexión rápida

- Si algo se rompiera ahora mismo, ¿me enteraría por una **señal** o por una
  **queja**? _[responde honesto]_
