# Ejercicio 8.1 — Estimación de capacidad y diagnóstico de cuello de botella

> **Modalidad: a mano (razonamiento/diseño, sin IA).** No escribes código aquí. Entrenas el músculo
> que define la entrevista de system design: mirar un sistema bajo carga, estimar su capacidad con un
> cálculo de servilleta, y señalar **dónde** se rompe y por qué —antes de que lo haga producción.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.1` Fundamentos de System Design
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

Aplicar el método del Worked Example 1 de la lección a un sistema nuevo: estimar QPS y concurrencia,
identificar el cuello de botella real, proponer un plan de escala con sus trade-offs, y resolver una
decisión CAP. Es el paso previo obligatorio al [capstone de la fase](../../../) (diseñar 3 sistemas
en papel).

## 📋 Contexto

`sistema.md` describe un **servicio de comentarios para un medio digital** con sus números de
tráfico. Se ve manejable. Cuando publican una noticia viral, el tráfico se dispara. Tu trabajo es
anticipar qué se cae y cómo evitarlo, con números, no con intuición.

## 📏 Primero-Sin-IA

1. Lee `sistema.md` con calma. **A mano**, sin IA, sin buscar en internet, escribe tu análisis.
2. Solo entonces, consulta la **documentación oficial** si necesitas confirmar un término (la ley de
   Little, cache-aside, CAP).
3. **Solo al final**, usa IA para *revisar* tu análisis —no para generarlo.
4. Mañana, explícale el diagnóstico a alguien (o en voz alta). Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Crea `capacidad.md` en esta carpeta con **cinco secciones**:

1. **Estimación.** De DAU a QPS promedio y **pico** (declara tu factor de pico y por qué). Calcula la
   **concurrencia** con la ley de Little (concurrencia ≈ tasa × latencia). **Muestra la aritmética.**
2. **Cuello de botella.** Qué recurso se satura **primero** y por qué (no asumas la CPU). Nombra la
   métrica de saturación (RED/USE) que lo confirmaría en producción.
3. **Plan de escala** ordenado por costo/beneficio: **≥3 intervenciones**, de la más barata y de
   mayor impacto hacia abajo, cada una con su **trade-off** explícito (incluida la obsolescencia de
   la caché y el *replication lag* si usas réplicas).
4. **Una decisión CAP.** Señala **un** punto del sistema donde aparece el dilema C vs A; di qué
   elegirías **y por qué** (es una decisión de negocio).
5. **Diagrama Mermaid** del sistema resultante, con el presupuesto de latencia anotado por salto.

> No diseñes "el sistema perfecto" ni metas microservicios: el ejercicio es **estimar y diagnosticar**
> con las piezas de la lección.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `capacidad.md` tiene las 5 secciones.
- [ ] Sección 1: aritmética de QPS promedio, QPS pico (con factor declarado) y concurrencia (Little), mostrada.
- [ ] Sección 2: el cuello de botella es el recurso compartido correcto (no "la CPU"), con su métrica.
- [ ] Sección 3: ≥3 intervenciones ordenadas, cada una con su trade-off nombrado.
- [ ] Sección 4: una decisión CAP defendida como decisión de negocio.
- [ ] Sección 5: diagrama Mermaid que renderiza y refleja el plan.
- [ ] Puedes **explicar tu análisis sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el cuello de botella: pregúntate qué recurso es **clonable** (agrego otro igual y listo: la capa
de app stateless) y cuál es **compartido y único** (la base de datos primaria). El que no se clona
fácil es casi siempre el cuello. Para el plan: ¿qué fracción del tráfico son lecturas y qué técnica
quita carga de lecturas casi gratis antes de tocar la DB? Para CAP: piensa en qué pasa con el contador
de comentarios o los votos cuando dos nodos no se hablan —¿prefieres un número viejo (AP) o un error
(CP)? Y para concurrencia, usa el **pico**, no el promedio.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `capacidad.md` (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-8/estimacion-capacidad-cuello-botella.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-8/estimacion-capacidad-cuello-botella.md`
— no la mires antes de intentarlo de verdad.
