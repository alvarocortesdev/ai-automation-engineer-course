# Ejercicio 7.4 — Decisor: ¿código, navegador o RPA?

> **Modalidad: código (función pura, testeable).** Codificar la escalera de integración te obliga a
> volver tu criterio **preciso**: hablar de "depende" está bien en una charla; un `if` no admite
> vaguedad.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.4` De RPA a código
**Ruta:** opcional / profundización · **Timebox:** 35 min

## 🎯 Objetivo

Implementar una función **pura** `recomendar_automatizacion(caso)` que aplique la **escalera de
integración** (API → navegador semántico → RPA de UI → rediseñar el proceso) y devuelva la estrategia
correcta con un motivo que explique la **restricción dominante**.

## 📋 Contexto

La lección argumenta el criterio en prosa; aquí lo conviertes en código que un test puede verificar.
El caso resbaloso es "ni API ni web **pero** crítico o de alto volumen": ahí la RPA de UI no es una
base aceptable y la respuesta correcta es subir el problema (pedir API / export / ETL), no clickear
pantallas. Este decisor es el músculo de criterio que aplicarás al elegir cómo integra tu capstone.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Escribe la escalera como una cadena de `if`.
2. Solo entonces, consulta documentación oficial si la necesitas.
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, reescríbelo de memoria. Si no te sale la escalera, no la aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `decisor.py` y completa `recomendar_automatizacion` (no cambies las firmas ni los nombres de
   los campos de `Caso` / `Recomendacion`: los tests dependen de ellos).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso de prueba tuyo** en `tests/test_decisor.py` (ver el TODO del final: ¿qué
   debería decir el `motivo` cuando `ui_cambia_seguido=True`?).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Todos los tests pasan.
- [ ] La función es **pura**: sin I/O, sin estado global, mismo input → mismo output.
- [ ] Cubre los **cuatro** destinos: `api`, `navegador`, `rpa-ui`, `rediseñar-proceso`.
- [ ] El `motivo` explica el **porqué** (la restricción dominante), no solo repite la estrategia.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar tu escalera sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Escribe la escalera **de arriba hacia abajo** como `if` encadenados y devuelve apenas encuentres el
escalón. El primero es el atajo: `if caso.tiene_api: return ... "api"`. Después de descartar la API,
estás obligado a automatizar una UI (frágil): pregúntate si el proceso aguanta esa fragilidad como
base (`critico` o `volumen_alto` → no, rediseña). Recién entonces decides web (`navegador`) vs
escritorio (`rpa-ui`). El orden de los `if` **es** la escalera.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-7/decisor-codigo-vs-rpa.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/decisor-codigo-vs-rpa.md` — no la mires
antes de intentarlo de verdad.
