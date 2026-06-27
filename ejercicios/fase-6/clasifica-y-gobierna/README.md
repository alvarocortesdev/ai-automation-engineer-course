# Ejercicio 6.15 — Clasifica y gobierna: 5 sistemas de IA

> **Modalidad: diseño / razonamiento (sin código).** No hay tests ni función que
> implementar. Entregas un documento donde **clasificas y gobiernas**, para cinco sistemas
> de IA reales: en qué tier de riesgo del EU AI Act caen, si el alcance extraterritorial los
> alcanza, qué obligaciones les tocan y qué artefactos de gobernanza escribirías. Es la
> conversación que tendrás con un cliente corporativo o un entrevistador en 2026.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.15` AI Governance / EU AI Act / Responsible AI
**Ruta:** crítica · **Timebox:** 40 min · **Modalidad:** a-mano (diseño)

## 🎯 Objetivo

Para cinco sistemas, decidir y **justificar**: (a) el **tier de riesgo** (inaceptable / alto
/ limitado / mínimo) derivado del criterio, (b) si el **alcance extraterritorial** del EU AI
Act los alcanza (a dónde llega la salida, no dónde corre el servidor), (c) las **obligaciones**
que les tocan, y (d) qué **artefactos de gobernanza** (model card, data card, audit log,
supervisión humana, etiqueta de transparencia) escribirías. Los tiers tienen veredicto
correcto; los matices y artefactos se evalúan por la **calidad de la justificación**.

## 📋 Contexto

El error #1 de quien recién entra a IA es creer que "la regulación es problema de otros" o que
"basta con que un abogado lo revise al final". Un AI Engineer clasifica su propio sistema y
deriva qué le aplica **antes** de desplegar, porque casi todas las obligaciones (medir sesgo,
loguear decisiones, mantener un humano en el loop, avisar que es una IA) **son decisiones de
ingeniería**. En el capstone de la fase usarás esto para escribir la sección de gobernanza de
tu RAG.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba), apoyándote solo en la lección.
2. Para cada caso aplica, **en orden**, las preguntas del worked example:
   1. ¿Es un uso **prohibido**? (si sí, párate)
   2. ¿**Decide algo serio** sobre personas (empleo, crédito, salud, justicia, educación,
      biometría)? → alto riesgo.
   3. ¿**Interactúa** con personas o **genera contenido**? → transparencia (Art. 50).
   4. Si nada de lo anterior → mínimo.
   Y aparte: **¿la salida llega a la UE?** → decide el alcance.
3. Solo al final, usa IA para *atacar* tus clasificaciones, no para escribirlas.
4. Mañana, **reescribe de memoria** los cuatro tiers con un ejemplo de cada uno. Si no
   puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Crea un archivo `clasificacion.md` en esta carpeta. Resuelve los **cinco** casos usando,
para cada uno, esta plantilla exacta:

```markdown
## Caso N — <nombre>

- **Tier de riesgo:** <inaceptable | alto | limitado | mínimo> — derivado de qué pregunta del orden.
- **¿Le aplica el EU AI Act (alcance extraterritorial)?** <sí | no> — porque la salida <llega | no llega> a la UE.
- **Obligaciones principales:** <qué le exige el Act, en concreto> (o "ninguna obligatoria").
- **Artefactos de gobernanza que escribiría:** <model card / data card / audit log / etiqueta Art. 50 / supervisión humana> — por qué.
- **Riesgo si lo clasificaras mal:** una consecuencia concreta (p. ej. tratar alto riesgo como mínimo → multa + sistema indefendible).
```

### Caso 1 — Screening de CVs

Una startup chilena vende una herramienta que **lee CVs y los rankea** para que RRHH decida a
quién entrevistar. Algunos clientes son empresas en **España**. Corre en un servidor en
Santiago.

### Caso 2 — Chatbot de soporte

Una empresa pone un **chatbot de IA** en su web para responder preguntas de soporte. Usuarios
de toda Latinoamérica y algunos de la UE. No decide nada: solo responde y, si no sabe, deriva
a un humano.

### Caso 3 — Generador de avatares "deepfake" para marketing

Una agencia usa IA para generar **videos sintéticos** de un presentador que nunca grabó esos
videos, para campañas publicitarias en mercados que incluyen la UE.

### Caso 4 — Filtro de spam

Un equipo entrena un modelo que **marca correos como spam o no-spam** en el buzón interno de
la empresa. Sin impacto sobre personas externas, sin contenido generado.

### Caso 5 — "Puntaje de confianza ciudadana"

Un organismo propone un sistema que asigna a cada ciudadano un **puntaje de confiabilidad**
agregando su comportamiento (pagos, redes, multas) para **darle o negarle acceso a servicios
públicos**.

> Pista honesta: los cinco casos cubren a propósito los cuatro tiers (uno es prohibido, uno
> es mínimo, y los del medio se reparten entre alto y limitado). Uno de los casos NO te
> alcanza por alcance extraterritorial si lo lees con cuidado. No fuerces que todos sean
> "alto riesgo".

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los cinco casos resueltos con la plantilla completa.
- [ ] Cada tier se **deriva** del orden de preguntas, no se adivina.
- [ ] Identificas correctamente el caso **prohibido** (inaceptable) y el caso **mínimo**, sin
      confundirlos con los del medio.
- [ ] Resuelves el **alcance extraterritorial** en cada caso (a dónde llega la salida), y al
      menos en uno concluyes que el Act **no** aplica con argumento.
- [ ] Para los casos de alto riesgo y limitado, nombras la **obligación concreta** (logging +
      supervisión humana + sesgo para alto riesgo; aviso Art. 50 / etiqueta para limitado).
- [ ] Puedes **defender oralmente** cada clasificación sin leer tus notas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Empieza siempre por la pregunta binaria: **¿es un uso prohibido?** Solo uno de los cinco lo
es, y es el que asigna puntajes a personas para darles o negarles servicios (suena a "social
scoring"). Después: **¿decide algo serio sobre personas?** El que rankea CVs sí (empleo =
Annex III, alto riesgo). El chatbot y el generador de video **no deciden**: interactúan o
generan → transparencia (Art. 50). El filtro de spam interno no toca a personas externas ni
genera contenido → mínimo. Para el alcance, pregúntate literalmente "¿algún usuario o cliente
en la UE recibe la salida?". Revisa "Los cuatro tiers" y "Alcance extraterritorial" de la
lección antes de mirar la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/clasifica-y-gobierna/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no la mires antes de
intentarlo de verdad. (Los tiers tienen veredicto correcto; en los artefactos hay varias
respuestas defendibles: el corrector evalúa tu **justificación**, no que coincidas palabra
por palabra.)
