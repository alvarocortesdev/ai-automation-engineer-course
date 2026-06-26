# Ejercicio 3.14 — Circuit breaker: la máquina de estados (a mano)

> **Modalidad: código (Python, sin IA).** Implementas el cortacircuitos que protege a tu servicio (y a la dependencia caída) cuando los reintentos ya no alcanzan. Una máquina de estados pequeña pero con transiciones que es fácil equivocar.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.14` Idempotencia y resiliencia
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar la clase `CircuitBreaker` con sus tres estados (closed/open/half-open) y el método `llamar(fn)`: contar fallos consecutivos, abrir al alcanzar el umbral, rechazar llamadas mientras está abierto, y dejar pasar **una** prueba al cumplirse la ventana de espera (half-open) que cierra o reabre el circuito.

## 📋 Contexto

Reintentar asume que la falla es breve. Cuando una dependencia lleva minutos caída, seguir golpeándola desperdicia recursos y alarga cada request. El breaker corta y da una falla **rápida**. Es el complemento natural del retry del ejercicio anterior y entra al diseño de cualquier dependencia externa crítica del capstone.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Dibuja la máquina de estados antes de teclear.
2. Solo entonces consulta **documentación oficial** (Martin Fowler, CircuitBreaker; `time.monotonic`).
3. **Solo al final**, usa IA para *revisar* — no para generar la clase.
4. Mañana, reescríbela de memoria.

## 🛠️ Instrucciones

1. Abre `solucion.py` e implementa `CircuitBreaker` **sin cambiar las firmas**. `CircuitoAbierto` ya está definida.
2. El **reloj** se inyecta (default `time.monotonic`) para avanzar el tiempo en los tests sin esperar. Pista para `estado`: si el estado interno es `"open"` pero ya pasó la ventana, repórtalo como `"half-open"` (así es observable y `llamar` usa la misma condición para permitir la prueba).
3. Corre el test:

   ```bash
   uv run pytest        # o: pytest
   ```

4. Escribe `bitacora.md`: diferencia breaker vs retry, y para qué sirve half-open.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: arranca cerrado, el umbral lo abre, abierto rechaza sin invocar `fn`, tras la ventana queda half-open, prueba exitosa cierra y fallida reabre, un éxito reinicia el contador.
- [ ] Estando abierto **nunca** invocas `fn` (lanzas `CircuitoAbierto` directo).
- [ ] La prueba fallida en half-open **reinicia** el temporizador de apertura.
- [ ] `bitacora.md` distingue breaker de retry y justifica el half-open.
- [ ] Agregaste **un test borde tuyo** (p. ej. `umbral_fallos=1`).
- [ ] Puedes explicar **sin notas** por qué la falla "rápida" del breaker protege a la dependencia caída.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Guarda `_estado` ("closed"/"open"), `_fallos`, `_abierto_en`. La propiedad `estado`: `if self._estado == "open" and (reloj() - self._abierto_en) >= espera: return "half-open"`, si no devuelve `self._estado`. En `llamar`: si `estado == "open"` lanza `CircuitoAbierto`; si no, `try: r = fn()` → en éxito reinicia (fallos=0, closed) y devuelve `r`; en `except Exception:` registra el fallo (si estaba en half-open reabre y reinicia el reloj; si no, incrementa y abre al llegar al umbral) y re-lanza. Repasa la sección 4.5 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `solucion.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/circuit-breaker-estados.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/circuit-breaker-estados.md` — no la mires antes de intentarlo.
