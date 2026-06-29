# Ejercicio T0.8 — Demo de valor para no-ingenieros + manejo de expectativas

> **Modalidad: diseño/razonamiento (sin código, sin IA primero).** Al stakeholder de negocio no le
> importa el reranker ni las dimensiones del embedding: le importa **qué cambia en su semana**. El
> Forward-Deployed Engineer traduce *feature → valor → outcome* en el idioma del cliente, y maneja las
> expectativas con honestidad calibrada (sub-promete, sobre-entrega). La jerga erosiona la confianza;
> sobre-prometer en IA la destruye en la entrega.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.8` Lane Forward-Deployed / cliente-facing
**Ruta:** profundización · **Timebox:** 35 min

## 🎯 Objetivo

- **O1** — Traducir una feature técnica a una **demo de valor para no-ingenieros** (outcome y "antes /
  después", cero jerga).
- **O2** — Manejar expectativas de forma honesta: una tabla **qué hace / qué NO hace** (incluidos los
  límites de la IA) y una respuesta de FDE a un **scope creep** que ni promete a ciegas ni cierra la
  puerta.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox 35 min). No le pidas a la IA que escriba el guion por ti.
2. Solo entonces relee el músculo 2 (demo de valor) y el 3 (expectativas) de la lección si dudaste.
3. **Solo al final**, usa IA para *revisar* tu guion —no para generarlo.
4. Mañana, toma un proyecto tuyo y explícalo **de memoria** en una frase de valor, sin una sola palabra
   técnica.

## 📋 La feature a traducir

Lee `feature-tecnica.md` (en esta carpeta): la descripción de una feature escrita en **jerga de
ingeniería**. Tu trabajo es presentarla a una stakeholder no técnica sin que se sienta perdida.

## 🛠️ Tu tarea (en este orden)

En `demo-y-expectativas.md` (parte de `demo.starter.md`):

1. **Guion de demo (máx. 6 frases), en lenguaje de negocio:** traduce la feature a **valor y outcome**,
   con un **antes / después** concreto. Si aparece **una sola** palabra técnica que un gerente no
   entendería, la demo falló: reescríbela.
2. **Tabla "qué hace / qué NO hace":** al menos **3** cosas que el sistema **sí** hace y **3** que **no**
   (o que requieren un humano). Aquí va, de frente, el techo de precisión y el riesgo de alucinación.
3. **Maneja un scope creep:** en plena demo, la stakeholder pide "¿y de paso puede también [feature
   nueva]?". Escribe tu respuesta de FDE —ni un "sí" reflejo que revienta el plazo, ni un "no" seco—
   dejando **registro por escrito**.
4. **Una línea de cierre:** por qué sub-prometer y sobre-entregar protege la relación mejor que
   prometerlo todo.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] El **guion** no contiene jerga técnica y muestra un **antes / después** de outcome.
- [ ] La **tabla** tiene **≥3 "hace"** y **≥3 "no hace"** honestos, incluidos límites de la IA.
- [ ] La respuesta al **scope creep** ni promete a ciegas ni cierra la puerta, y queda **registrada**.
- [ ] La línea de cierre conecta **sub-prometer** con **confianza**.
- [ ] Puedes **explicar por qué la jerga erosiona la confianza sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para el guion: por cada término técnico, pregúntate "¿qué hace esto **para el usuario**?". "Búsqueda
vectorial" no es valor; "encuentras la respuesta aunque no uses las palabras exactas del documento" sí.
Usa un caso real ("imagina que llega el correo de la señora Pérez...") en vez de uno abstracto. Para el
scope creep: la fórmula es **reconocer + acotar + registrar**: "buena idea, eso es una fase 2; lo anoto y
lo estimamos después de entregar el MVP" —nunca un sí que mete una feature nueva al plazo actual. Para la
tabla "no hace": ser honesto sobre que la IA puede equivocarse y que por eso hay un humano revisando NO
te hace ver peor; te hace ver como alguien en quien se puede confiar.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/track-0/demo-valor-no-features.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/track-0/demo-valor-no-features.md` — no la mires
antes de intentarlo. El corrector evaluará tu **criterio de traducción** (cero jerga, honestidad de
expectativas, manejo del scope creep), no que tu guion coincida palabra por palabra con un ejemplo.
