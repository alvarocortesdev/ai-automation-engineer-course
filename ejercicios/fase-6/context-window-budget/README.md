# Ejercicio 6.2 — Token budget: arma el contexto que cabe

> **Modalidad: mixto (a mano + código).** Primero predices a mano, sin ejecutar ni
> usar IA. Luego implementas el corazón del context engineering: la función que
> decide **qué entra en la ventana de contexto** cuando el historial ya no cabe.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.2` Prompt & Context Engineering
**Ruta:** crítica · **Timebox:** 40 min

## Objetivos

- **O1** — Implementar una política de **token budgeting** que conserve el `system`
  y los turnos más recientes dentro de un presupuesto dado.
- **O2** — Predecir qué turnos entran y cuáles se descartan, **sin ejecutar**.
- **O3** — Explicar por qué descartar los turnos **viejos** (y no los recientes)
  mitiga el **context rot**.

## El problema

La API de un LLM es **sin estado** (_stateless_): en cada turno reenvías toda la
conversación. La ventana de contexto tiene un presupuesto finito de tokens, así que
cuando el historial crece hay que decidir **qué cabe**. La política estándar:

1. El `system` es **obligatorio** y va primero (es el contrato, nunca se descarta).
2. Se conservan los turnos **más recientes** que quepan en lo que sobra del
   presupuesto (la recencia gana — combate el context rot).
3. Un turno entra **entero o no entra** (nunca se parte un mensaje).
4. La salida mantiene el **orden cronológico** (más viejo primero), como espera la API.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, para este caso de prueba (usa un contador de tokens
igual a **número de palabras**):

```
system  = "sys sys sys sys sys"                 (5 palabras)
historial (del más viejo al más reciente):
  t0 (user)      = 10 palabras
  t1 (assistant) = 10 palabras
  t2 (user)      = 10 palabras
  t3 (assistant) = 10 palabras
  t4 (user)      = 10 palabras
presupuesto_tokens = 35
```

Predice: **¿qué turnos entran y cuáles se descartan?** Escribe una línea de
razonamiento. **No ejecutes nada todavía.**

### Parte 2 — Código (verificación), ~25 min

1. Abre `presupuesto.py` y completa `armar_contexto(system, historial,
   presupuesto_tokens, contar)` (no cambies su firma). Nota que el **contador de
   tokens se inyecta** como parámetro `contar`: así pruebas la lógica sin depender de
   ninguna API ni librería externa.

2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, explica en 2-3 frases por qué conservar los turnos recientes y
descartar los viejos es mejor para la **calidad** de las respuestas, conectándolo con
el concepto de **context rot** de la lección (no basta con "para que quepa").

## Contrato de la función

```python
def armar_contexto(system, historial, presupuesto_tokens, contar):
    """
    system: str  -> mensaje de sistema, obligatorio, va primero.
    historial: list[dict]  -> [{"role": "user"|"assistant", "content": str}, ...]
                              en orden cronológico (más viejo primero).
    presupuesto_tokens: int  -> tope total (system + mensajes incluidos).
    contar: callable[[str], int]  -> cuenta tokens de un string (inyectado).

    Devuelve: {"system": system, "messages": [<turnos incluidos, cronológicos>]}
    Lanza ValueError si contar(system) > presupuesto_tokens.
    """
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — qué turnos entran/salen + razonamiento, **antes** de ejecutar.
- `presupuesto.py` — con la función completada (los tests pasan).
- `verificacion.md` — la reflexión que conecta la política con **context rot**.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con la predicción + razonamiento, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] La función conserva el orden cronológico, nunca parte un mensaje, y lanza
      `ValueError` si el `system` solo ya excede el presupuesto.
- [ ] `verificacion.md` conecta la política de descarte con **context rot**.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/context-window-budget/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir? ¿la reflexión
nombra el context rot?), no solo si los tests pasan.
