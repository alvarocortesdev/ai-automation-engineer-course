# Ejercicio 4.9 B — ¿Tailwind directo, shadcn/ui o design system? (mini-ADR)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.9` Design systems
**Ruta:** opcional / profundización · **Modalidad:** a mano (razonamiento / diseño) · **Timebox:** 30 min

> **Sin código.** Este ejercicio entrena el **criterio** que un revisor senior aplica en segundos: elegir el peldaño justo de complejidad de UI. Es un mini-ADR (Architecture Decision Record): decides la estrategia y **justificas el trade-off** (lo que ganas y el costo que aceptas).

## 🎯 Objetivo

Para cuatro escenarios reales, decidir la estrategia de UI —(a) **Tailwind directo**, (b) **shadcn/ui + tokens**, o (c) **design system publicado** (tokens versionados + paquete compartido + Storybook)— y defender cada decisión apelando al trade-off **costo de montar/mantener vs costo de la inconsistencia**. Más dos preguntas trampa sobre el modelo de shadcn y sobre accesibilidad.

## 📋 Los cuatro escenarios

1. **Portafolio personal.** Tú solo, un sitio de ~4 páginas (landing, proyectos, sobre mí, contacto). Botones, tarjetas y un formulario de contacto. Quieres que se vea prolijo y consistente, pero el plazo es corto y eres el único dev.
2. **Capstone de chat con IA (ChatLab).** Tú solo, ~6 pantallas. Necesitas **modales** (confirmar borrado), un **menú desplegable** (elegir modelo), **tooltips** y un **select**, todos accesibles por teclado, además de tema claro/oscuro.
3. **MVP de una startup de 3 personas.** Un producto que crecerá; dos devs frontend tocando los mismos componentes. Quieren ir rápido pero sin que la UI diverja entre lo que hace cada uno.
4. **Empresa con 4 equipos y 3 productos** (web app, panel de administración, sitio de marketing) que deben compartir **la misma identidad de marca** y evolucionarla de forma coordinada.

## 🛠️ Tu tarea (en este orden — Primero-Sin-IA, timebox 30 min)

1. Para cada escenario, **decide** (a / b / c) y escribe **una o dos frases** de justificación tipo ADR: qué eliges, por qué, y **qué costo aceptas**. Recorre la escalera de decisión de la sección 4.5 de la lección.
2. Responde las dos **preguntas trampa** (abajo).
3. Para al menos un escenario **ambiguo**, explica por qué dudaste entre dos opciones y qué inclina la balanza.

Deja tu trabajo en `decision-ds.md` (hay una plantilla en esta carpeta).

### Preguntas trampa

- **T1.** Un compañero dice: "shadcn/ui es una dependencia más; la instalo y listo, como cualquier librería de UI". ¿En qué se equivoca? Nombra la consecuencia práctica concreta del modelo real de shadcn.
- **T2.** En el escenario 2 propones construir el modal y el menú "a mano con `div` y `onClick`, para tener control total". ¿Por qué es mala idea? Responde **desde la accesibilidad** y conéctalo con WCAG ([4.4](/fase-4-frontend/4-4-accesibilidad-wcag/)).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los **4 escenarios** decididos, cada uno con su estrategia y una justificación que apele al **trade-off real** (no a "porque es lo moderno").
- [ ] Reconoces que el **portafolio (1)** NO necesita un DS publicado (evitas el sobre-engineering) y que la **empresa multi-equipo (4)** SÍ lo justifica.
- [ ] Eliges **shadcn/ui** para el **capstone (2)** y lo justificas por componentes accesibles + consistencia sin reinventar.
- [ ] Respondes **T1** nombrando el modelo "open code" (el CLI copia el código en tu repo; lo posees / no se actualiza solo).
- [ ] Respondes **T2** desde accesibilidad (foco atrapado, `Esc`, teclado, ARIA) y la conexión con WCAG.
- [ ] Explicas la duda de al menos un escenario ambiguo (típicamente el 3).
- [ ] Puedes **defender tus decisiones sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para cada escenario pregúntate, en orden: (1) ¿pocas pantallas y un solo dev sin mucha repetición? → Tailwind
directo. (2) ¿muchos componentes interactivos (modales, menús, selects) y quiero accesibilidad + consistencia
sin reinventar? → shadcn/ui + tokens. (3) ¿varios equipos o productos comparten una marca que hay que
evolucionar coordinadamente? → design system publicado. La pregunta que decide siempre: **¿el costo de la
inconsistencia ya supera el costo de montar la herramienta?** Para T1 piensa en *dónde vive el código* (tu repo
vs `node_modules`). Para T2 piensa en lo más difícil de un diálogo accesible: foco, teclado, ARIA. Esto es una
pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/adoptar-design-system/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **razonamiento** (las justificaciones y el trade-off), no solo si elegiste la letra correcta. La **solución de referencia** vive en `.ai/soluciones/fase-4/adoptar-design-system.md` — no la mires antes de intentarlo de verdad.
