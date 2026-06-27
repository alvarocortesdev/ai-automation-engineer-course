# Ejercicio 4.10 B — Auditoría de usabilidad con las heurísticas de Nielsen

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.10` Usabilidad + estados de primera clase
**Ruta:** crítica · **Modalidad:** a mano (razonamiento / diseño, sin código) · **Timebox:** 30–35 min

> **Sin código.** No vas a rediseñar en CSS: vas a **diagnosticar** una pantalla por escrito, nombrando la
> **heurística de Nielsen** exacta que viola cada problema. Es el músculo que te hace buen revisor en code
> review y buen cliente de la IA: si no nombras el problema con vocabulario compartido, no puedes evaluar
> la solución (ni pedirla con precisión).

## 🎯 Objetivo

- **O1** — Diagnosticar la interfaz nombrando, por cada problema, la **heurística de Nielsen concreta**
  (número + nombre canónico en inglés, p. ej. "H1 *Visibility of system status*") y por qué la viola.
- **O2** — Detectar al menos **un estado faltante** (empty / loading / error) y atarlo a su heurística
  (típicamente H1 o H9).
- **O3** — **Priorizar**: si solo pudieras arreglar tres cosas, cuáles y por qué (por impacto, no por orden
  de aparición).

## 📋 Contexto

La pantalla a auditar está descrita en detalle en `pantalla-a-auditar.md` (con su flujo, textos y
comportamiento). Es el "panel de subida de documentos" de una app de IA, justo el tipo de pantalla que
construirás en el capstone. Diagnosticarla con precisión es exactamente lo que harás cuando revises el PR
de un compañero o le pidas a una IA "mejora esta UI".

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba), con las 10 heurísticas al lado como checklist.
2. Documentación oficial permitida (NN/g, WCAG) para verificar nombres y umbrales.
3. **Solo al final**, usa IA para *contrastar* tu auditoría — no para *generarla*.
4. Mañana, mira una app que uses a diario y repite el diagnóstico de memoria.

## 🛠️ Instrucciones

1. Lee `pantalla-a-auditar.md`.
2. Recorre la pantalla con las **10 heurísticas** una por una. Por cada problema que encuentres, escribe en
   `auditoria.md` una entrada con esta forma:

   ```text
   - Problema: <qué está mal, concreto>
     Heurística: <H# + nombre, p. ej. "H5 Error prevention">
     Por qué la viola: <una frase>
     Corrección: <qué cambiarías, concreto>
   ```

3. Asegúrate de que **al menos un problema** sea un **estado faltante** (empty/loading/error) atado a su
   heurística.
4. Al final de `auditoria.md`, agrega un **top-3 priorizado**: las tres correcciones de mayor impacto, cada
   una con una frase de por qué va primero.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Identificaste **al menos seis** problemas distintos, cada uno atado a una **heurística concreta**
      (número + nombre), no a un juicio de gusto.
- [ ] Cubres al menos **un estado faltante** (empty/loading/error) conectado con su heurística.
- [ ] Identificaste al menos un problema de **prevención de errores (H5)** (evitar, no solo avisar).
- [ ] Cada problema trae una **corrección accionable**.
- [ ] El **top-3 priorizado** está justificado por impacto (qué bloquea/engaña a todos vs. molestia menor).
- [ ] Puedes **defender tu diagnóstico sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

No mires la pantalla "en general": pregúntate por **cada** heurística "¿se respeta aquí?". ¿El sistema dice
qué pasa mientras sube el archivo (H1)? ¿los textos hablan el idioma del usuario o el de la BD (H2)? ¿se
puede cancelar/deshacer (H3)? ¿se llama igual la misma acción en todos lados (H4)? ¿deja subir un archivo
inválido y recién después avisa, o lo previene (H5)? ¿obliga a recordar algo entre pasos (H6)? ¿hay ruido
que tapa el botón importante (H8)? ¿el error dice cómo recuperarse o solo "algo salió mal" (H9)? Para los
estados, pregunta qué ve el usuario mientras sube, si falla la subida, y si la lista de documentos está
vacía. Para priorizar: lo que **bloquea o engaña** va antes que lo que **molesta**. Esto es una pista, no la
solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/auditoria-heuristica-nielsen/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (si nombras la heurística correcta y priorizas bien), no si
"adivinaste" los mismos problemas que la solución. La **solución de referencia** vive en
`.ai/soluciones/fase-4/auditoria-heuristica-nielsen.md` — no la mires antes de intentarlo de verdad.
