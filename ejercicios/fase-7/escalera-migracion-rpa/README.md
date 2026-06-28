# Ejercicio 7.4 — Plan de migración de un RPA frágil

> **Modalidad: a mano (razonamiento / diseño, sin IA).** No escribes el código nuevo aquí. Entrenas
> el músculo que separa al que "graba otro bot" del que **diagnostica por qué el bot se rompe** y
> diseña la salida: la escalera de integración + una migración con red de seguridad.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.4` De RPA a código
**Ruta:** opcional / profundización · **Timebox:** 45 min

## 🎯 Objetivo

Diseñar la migración de un bot RPA frágil (`bot_legado.py`) a código mantenible: diagnosticar sus
modos de falla, clasificar cada paso en la **escalera de integración**, y planear el corte
**incremental** (Strangler Fig) con un ADR honesto y un BPMN mínimo.

## 📋 Contexto

`bot_legado.py` da de alta proveedores clickeando coordenadas en un portal web y esperando con
`sleep` fijos. Se ve "funcional"; en producción es una bomba de tiempo. Diagnosticarlo y planear su
reemplazo es justo la conversación de entrevista detrás de "migración de procesos legados" —y el paso
previo a integrar bien las acciones externas de tu capstone.

## 📏 Primero-Sin-IA

1. Lee `bot_legado.py` con calma. **A mano**, sin IA, completa `migracion.md`.
2. Solo entonces, consulta documentación oficial (Playwright, Strangler Fig) si necesitas confirmar.
3. **Solo al final**, usa IA para *revisar* tu plan — no para generarlo.
4. Mañana, explícale el plan a alguien (o en voz alta). Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Completa `migracion.md` (la plantilla ya está en esta carpeta) con **cuatro secciones**:

1. **Diagnóstico:** ≥4 modos de falla, cada uno anclado a una línea/paso de `bot_legado.py` y a su
   causa raíz (posición vs significado, `sleep` adivinado, falla silenciosa, no idempotente, ciego
   para operaciones).
2. **Escalera por paso:** clasifica cada paso del bot en su escalón (`api` / `navegador` / `rpa-ui` /
   `rediseñar-proceso`) y justifica con la restricción dominante.
3. **Plan Strangler Fig:** qué cortas primero y por qué, cómo corres viejo y nuevo en paralelo, y qué
   métrica te da confianza antes de cada corte.
4. **ADR + BPMN mínimo:** un ADR corto (con un trade-off honesto: migrar también cuesta) y un
   diagrama de carriles en Mermaid del proceso objetivo.

> No escribas el código nuevo: este ejercicio es de **diseño**. La implementación (Playwright,
> función pura de decisión) la trabajas en el reto `decisor-codigo-vs-rpa` y, a fondo, en el capstone.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `migracion.md` tiene las 4 secciones.
- [ ] Sección 1: ≥4 modos de falla **distintos**, cada uno ligado a una línea/paso concreto.
- [ ] Sección 2: cada paso en un escalón justificado; no bajas de escalón sin razón.
- [ ] Sección 3: plan **incremental y reversible** (no big-bang), con métrica de confianza.
- [ ] Sección 4: ADR nombra ≥1 trade-off real de migrar; el BPMN comunica el proceso a alguien no
      técnico.
- [ ] Puedes **explicar tu plan sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el diagnóstico, pregúntate por cada `click`/`sleep`: *"si el portal cambia un píxel, o si la red
va lenta, o si el RUT ya existía, ¿qué hace el bot?"*. Para la escalera, fíjate que `cargar_proveedores`
y `validar_rut` **no tocan ninguna UI**: ya son código puro, son el corte más barato y seguro para
empezar el Strangler Fig. El paso difícil es `dar_de_alta`: ¿hay API? (dicen que no) → ¿es web? (sí)
→ navegador semántico, no coordenadas. El ADR debe admitir que migrar **cuesta** (negociar/operar más
cosas), no venderlo como gratis.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `migracion.md` (esta carpeta),
- la **rúbrica**: `.ai/rubricas/fase-7/escalera-migracion-rpa.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/escalera-migracion-rpa.md` — no la mires
antes de intentarlo de verdad.
