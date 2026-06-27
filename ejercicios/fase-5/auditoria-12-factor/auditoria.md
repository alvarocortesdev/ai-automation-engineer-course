# Auditoría 12-factor — completa esta plantilla

> Tu entrega. Revisa `app.py`, `Dockerfile` y `compose.yaml` y lista cada
> violación que encuentres. Hay **al menos seis** reales. Calidad sobre
> cantidad: un síntoma bien explicado vale más que un factor citado de memoria.
> Borra esta cita al entregar.

## Violaciones encontradas

Para cada una: **dónde** está (archivo + línea/fragmento), **qué factor** incumple
(número + nombre), el **síntoma concreto en producción** (observable, no genérico),
y el **arreglo** en 1–2 líneas.

### V1
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

### V2
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

### V3
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

### V4
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

### V5
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

### V6
- **Dónde:**
- **Factor:**
- **Síntoma en producción:**
- **Arreglo:**

<!-- Añade V7, V8... si encuentras más. -->

## ADR corto — prioridad de arreglo

> De todos los arreglos, ¿cuál harías PRIMERO y por qué? (1 párrafo).
> Pista: piensa en riesgo de seguridad vs riesgo operativo.

## Defensa (responde sin notas)

- ¿Por qué un secreto horneado en la imagen es peor que uno en una variable de entorno?
- ¿Qué factor habilita el escalado horizontal y por qué este backend no escala hoy?
