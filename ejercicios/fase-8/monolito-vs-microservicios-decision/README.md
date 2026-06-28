# Ejercicio 8.3a — Decisor: ¿monolito modular o microservicios?

> **Modalidad: a mano (razonamiento, sin IA).** Este ejercicio entrena el **juicio** de arquitectura:
> decidir con la restricción dominante en vez de con la moda. No hay código de producción; hay
> decisiones defendidas. Es exactamente el tipo de pregunta que cae en una entrevista de system design.

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.3` Monolito modular vs microservicios
**Ruta:** opcional / profundización · **Timebox:** 30–40 min

## 🎯 Objetivo

- **O1** — Decidir, ante un escenario, entre **monolito modular** y **microservicios**, nombrando la
  **restricción dominante** que manda la decisión.
- **O2** — Para cada elección, nombrar al menos **un costo asumido** (microservicios) o un **gatillo de
  extracción futura** (monolito), reconociendo cuándo los microservicios son **prematuros**.

## 📋 Contexto

La decisión "monolito o microservicios" es la que más plata quema si se toma por reflejo. Este ejercicio
te obliga a separar las **cuatro razones reales** que justifican microservicios (equipos que se pisan,
escala desigual, tech divergente, aislar fallas) de los motivos especulativos ("para que quede bien").
Alimenta directo el capstone de la fase, donde decides la arquitectura de tres sistemas y la justificas
en un ADR.

## 📏 Primero-Sin-IA

1. Resuelve los cinco escenarios **solo**, a mano, dentro del timebox. Está bien dudar en el ambiguo.
2. Solo entonces consulta la lección (sección 4.4 y las misconceptions de la sección 5).
3. **Solo al final**, usa IA para *revisar y corregir* tu razonamiento — no para *generarlo*.
4. Mañana, vuelve a decidir el caso ambiguo de memoria y ve si llegas a la misma defensa.

## 🛠️ Instrucciones

Resuelve los **cinco escenarios** en `decisiones.md` (hay una plantilla en este directorio). Para **cada
uno**, escribe: (a) tu decisión (monolito modular / microservicios), (b) la **restricción dominante** que
la justifica, (c) un **costo asumido** si eliges microservicios, o un **gatillo de extracción** observable
si eliges monolito, y (d) en el caso ambiguo, el **trade-off explícito** que rompe el empate.

### Los escenarios

1. **MVP de equipo chico.** Una startup de tres ingenieros lanza un MVP de e-commerce. Tráfico bajo, el
   dominio todavía no está claro (van a iterar mucho el modelo de datos).
2. **Organización grande que se pisa.** Una empresa con ~200 ingenieros en 15 equipos; cada release del
   monolito actual tarda dos semanas de coordinación entre equipos.
3. **Componente caliente.** Un módulo de "transcodificación de video" satura CPU y necesita ~50 máquinas
   para su carga; el resto del sistema corre cómodo en una. El equipo es mediano (~12 personas).
4. **Arquitectura por estética.** Un equipo de cuatro propone "partamos en microservicios desde el día 1
   para que quede bien arquitecturado y escalable a futuro". El producto recién arranca.
5. **Caso ambiguo (decídelo y defiéndelo).** Una empresa de ~30 ingenieros en 4 equipos tiene un monolito
   que funciona, tráfico parejo (sin componente caliente), mismo stack tecnológico. Los equipos **a veces**
   se pisan en los despliegues (un par de conflictos al mes), pero nadie está bloqueado de forma crítica.
   ¿Monolito modular bien gobernado, o empezar a extraer servicios? No hay respuesta obvia: elige una y
   defiéndela contra la otra.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Cada decisión nombra la **restricción dominante** (no "es más limpio" ni "está de moda" ni
      "escala mejor" sin contexto).
- [ ] Cada decisión de **microservicios** nombra al menos **un costo** que asume (latencia/falla de red,
      saga/consistencia distribuida, carga operacional de N despliegues).
- [ ] Cada decisión de **monolito** incluye un **gatillo concreto y observable** que te haría extraer un
      servicio en el futuro (no "cuando sea grande").
- [ ] El **caso 5** se resuelve con un **trade-off explícito** (una fuerza a favor y una en contra), no
      esquivándolo.
- [ ] Puedes **defender tus cinco decisiones sin notas** (check de dominio).

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-8/monolito-vs-microservicios-decision/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará tu **razonamiento** (la restricción dominante y el trade-off), no si coincidiste con
una respuesta única — el caso 5 admite ambas decisiones bien defendidas.
