---
ejercicio_id: fase-0/disena-tu-sistema-de-estudio
fase: fase-0
sub_unidad: "0.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).
> Ojo: este ejercicio es de **diseño personal**. No existe una única respuesta
> correcta; esta es una **referencia ejemplar** + el criterio para juzgar otras.

# Solución de referencia — Diseña tu sistema de estudio

## Respuesta canónica (ejemplo de entrega "excelente")

### 1. Protocolo Primero-Sin-IA (con palabras propias)
1. Lo intento solo, a mano, con un timebox de 25–45 min, aunque salga feo.
2. Solo si me trabo (o al terminar), abro la **documentación oficial**.
3. Solo al final uso IA, y solo para **revisar y explicar** lo que ya hice.
4. Al día siguiente lo **reescribo de memoria**; si no me sale, vuelvo al paso 1.

Frase visible: *"Primero pienso yo; la IA revisa, no resuelve."*

### 2. Tabla de novedad (ejemplo para un cero real)
| Tarea | Etiqueta | Primera acción | Justificación |
|---|---|---|---|
| (a) `git rebase` | nuevo | worked example | Nunca lo he usado; reordenar historial es abstracto. |
| (b) `if/else` | nuevo | worked example | No he programado aún; necesito ver la forma primero. |
| (c) embedding | nuevo | worked example | Concepto totalmente nuevo; sin base no puedo "intentarlo". |
| (d) sumar dos números en una función | repaso | Primero-Sin-IA | Sumar lo sé; la "función" es envoltorio mínimo. |
| (e) desplegar con Docker | nuevo | worked example | Nunca desplegué nada; demasiadas piezas nuevas. |
| (f) leer un stack trace | nuevo | faded | No he visto errores aún, pero con un ejemplo guiado puedo completar. |

> **Clave de corrección:** las etiquetas correctas **dependen del alumno**. Para
> alguien con experiencia previa (perfil oxidado-con-experiencia), `git rebase`,
> Docker o stack traces pueden ser `repaso` → Primero-Sin-IA de entrada, y sería
> igualmente válido. Lo que **no** es válido: incoherencia etiqueta↔acción, o
> justificar "en abstracto" en vez de "respecto a mi historia".

### 3. Horario + drill (ejemplo a 12 h/sem)
- Lun/Mié/Vie 19:00–21:00 (bloque profundo) · Sáb 10:00–12:00 (proyecto).
- **Drill diario:** 1 problema pequeño (p. ej. un trazado a mano o un mini-reto)
  resuelto en papel **antes** de abrir el editor; lo registro con una marca en
  `progreso.md`.

### 4. Cadencia de spaced repetition
| Hito | Acción de recuperación |
|---|---|
| Mismo día | Resumen de 3 líneas de memoria. |
| +1 día | Reescribir la solución/idea sin mirar. |
| +3 días | Re-derivar un caso **nuevo** del mismo concepto. |
| +1 semana | Explicárselo a alguien o quiz rápido. |

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **Novedad escala el punto de partida.** Material nuevo → worked example (evita
   fijar misconceptions; efecto del worked example). Conocido → Primero-Sin-IA de
   entrada (la dificultad deseable construye memoria).
2. **La etiqueta manda sobre la acción.** `nuevo` ⇒ worked example/faded primero;
   `repaso` ⇒ intento solo primero. Invertirlo es el error #1.
3. **Spacing + recall, no relectura.** El repaso vale cuando **recuperas** de
   memoria (reescribir/predecir/enseñar). Releer hasta que "suene familiar" es
   ilusión de fluidez.
4. **La IA va al final.** Su rol es revisar/explicar, no generar el pensamiento.
   "No usar IA" ≠ "no necesitarla para pensar".

## Puntos resbalosos (donde el corrector debe mirar)
- **Incoherencia etiqueta↔primera acción** (lo más común). Verificar fila por fila.
- **Clasificación en abstracto** ("es difícil") en vez de "para mí" ("no lo he
  hecho"). El criterio rector es *¿lo he hecho antes con éxito?*.
- **Spacing falso:** todos los hitos el mismo día, o "releer" como acción de repaso.
- **Horario-deseo** sin bloques concretos; drill sin qué/cuándo/registro.
- **Malentendido de la regla:** poner la IA antes del intento, o equiparar la
  regla con prohibir la IA.

## Rango de soluciones aceptables
- Cualquier horario realista y concreto cuenta, sin importar los días/horas
  elegidos, siempre que tenga bloques fijos + drill + cadencia de recall.
- Las etiquetas de la tabla pueden diferir de este ejemplo y seguir siendo
  `excelente` **si la justificación es coherente con la experiencia del alumno** y
  la primera acción concuerda con la etiqueta.
- La cadencia de spacing puede usar otros intervalos (p. ej. +2/+5/+10) o una app
  como Anki; lo que importa es que sea **recuperación distribuida**, no relectura
  masiva. Herramientas distintas, mismo principio = aceptable.
