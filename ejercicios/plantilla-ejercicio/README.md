# [ID] — Título del ejercicio

> **Plantilla.** Esta es la estructura base que replica cada ejercicio del curso. Copia este
> directorio a `ejercicios/fase-N/<slug>/`, completa los campos y reemplaza el ejemplo ilustrativo
> (una función que pasa texto a mayúsculas) por el ejercicio real. Borra esta cita al usarla.

**Fase:** Fase N — Nombre de la fase · **Lección:** `N.x` Título de la sub-unidad
**Ruta:** crítica | opcional · **Timebox:** 25–45 min

## 🎯 Objetivo

Una o dos frases con un **verbo medible**: qué sabrás *hacer* al terminar. Ejemplo:
"Implementar una función pura que normalice texto a mayúsculas, con manejo del caso vacío".

## 📋 Contexto

Por qué importa este ejercicio y cómo conecta con el capstone de la fase. Mantenlo en 2–3 líneas.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta **documentación oficial**.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.py` y completa la función `resolver` (no cambies su firma).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `test_solucion.py` (un caso borde que se te ocurra).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] La función maneja el **caso borde** indicado (aquí: string vacío).
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar tu solución sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa en el **contrato** primero: ¿qué entra y qué sale? Para el ejemplo, una sola operación de
string resuelve el caso general; el caso vacío suele salir gratis si no asumes que hay al menos un
carácter. Revisa la sección correspondiente de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-N/<slug>.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-N/<slug>/` — no la mires antes de
intentarlo de verdad.
