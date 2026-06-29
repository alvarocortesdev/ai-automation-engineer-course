# T0.4 — Historia de falla en producción: instrumentar, romper, post-mortem público

> **Modalidad: mixto (instrumentación + escritura, sin tests automáticos).** Este
> ejercicio no se "corre": se _hace_ y se _escribe_. Produces la pieza de
> portafolio más difícil de falsificar —un post-mortem real— y la historia STAR
> que sale de ella. La parte que más cuesta —admitir que el usuario te avisó antes
> que tu alerta— es justo la que más te enseña.

**Fase:** Track 0 — Empleabilidad, marca e inglés · **Lección:** `T0.4` Historia de falla en producción
**Ruta:** crítica · **Timebox:** 45 min (lo escrito; instrumentar y conseguir usuarios reales viven en el tiempo real de tu proyecto)

## 🎯 Objetivo

Instrumentar una app con **usuarios reales**, dejar que algo **falle de verdad**, y
escribir un **post-mortem público y blameless** (7 secciones, causa raíz por 5
whys, cierre con una métrica/alerta/SLO nueva). Luego destilar el incidente en una
**historia STAR** en inglés para tu banco.

## 📋 Contexto

El 90% de quien aprende solo nunca pone su código frente a un usuario real, así que
nunca puede contar cómo se comporta **cuando algo se cae con gente esperando**. Esa
es la narrativa de semi-senior que te diferencia. No necesitas mil usuarios:
necesitas **tres reales** (tu pareja, un amigo, un familiar) y un fallo **honesto**.
Un incidente de juguete se detecta al instante; uno real, contado sin culpar a
nadie y cerrado con una alerta nueva, genera más confianza que diez features que
"nunca fallan".

## 📏 Primero-Sin-IA

1. Escribe los tres artefactos **a mano, sin IA** (timebox 45 min para lo escrito).
2. El incidente debe ser **real** (tu app con usuarios, o un fallo real de tu pasado
   que afectó a una persona real). **No inventes** usuarios ni números.
3. **Solo al final**, usa IA para que te _corrija_ con el framework de `.ai/` — no
   para que escriba tu post-mortem.
4. Mañana, sin mirar, recita las 7 secciones del post-mortem y explica por qué "fui
   descuidado" no es una causa raíz. Si no puedes, repásalo.

## 🛠️ Instrucciones

Completa los tres archivos starter de esta carpeta (traen la estructura y un ejemplo
ilustrativo que debes **reemplazar** por lo tuyo):

1. **`instrumentacion.md`** — la evidencia de que tu app está **observada**: qué app
   es, **quiénes son tus usuarios reales** (mínimo 3), el formato de tu **log
   estructurado** (línea JSON con `request_id`), y la **alerta** activa. Si aún no
   tienes alerta o usuarios, escribe el **plan concreto** para tenerlos esta semana
   (sin fingir que ya los tienes).
2. **`postmortem.md`** — el post-mortem **público y blameless**, **en inglés**, de un
   incidente **real**, con las **7 secciones**: Summary, Impact (usuario real +
   número), Timeline (con horas), Detection (qué alertó y **qué no**), Root cause (5
   whys hasta lo **sistémico**), Remediation, Action items (con **dueño y fecha**) +
   la **métrica/alerta/SLO nueva** que cierra el loop.
3. **`star-falla.md`** — el incidente como **una** historia STAR en inglés (formato de
   T0.3), con _Result_ apuntando a la alerta/SLO que agregaste, y debajo **≥3
   preguntas behavioral** que cubre.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `instrumentacion.md` nombra **usuarios reales** (o un plan creíble) y muestra un **log estructurado** + una **alerta** concreta.
- [ ] El post-mortem es de un incidente **real** (no de juguete) y tiene las **7 secciones** completas.
- [ ] La sección _Detection_ dice explícitamente **qué NO alertó** (el hueco de detección).
- [ ] La causa raíz es **sistémica** vía 5 whys, **no** "una persona se equivocó" (cero nombres como causa).
- [ ] Hay **action items con dueño y fecha** y una **métrica/alerta/SLO nueva** que cerraría el loop.
- [ ] (Hilo transversal — testing) Al menos un _action item_ es un **test de regresión** que reproduce el fallo.
- [ ] La historia STAR está en inglés, con _Result_ medible, y mapea a ≥3 preguntas behavioral.
- [ ] Puedes **explicar sin notas** por qué "me avisó el usuario" es una falla de detección.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Dos caminos honestos, ninguno inventa nada. **(A)** Si ya tienes una app que alguien
usa, el primer paso es la **instrumentación** (un log JSON por request + una alerta
de tasa de errores); el incidente llega solo en días —es paciencia, no ficción.
**(B)** Si no tienes app con usuarios, usa un incidente **real de tu pasado** (un bug
que un cliente o compañero sufrió de verdad). Reconstruye su timeline, aplícale los
5 whys y la sección de detección. Lo prohibido es inventar usuarios y números que
nunca existieron. Para la causa raíz: cada "por qué" te aleja del bug puntual
(trigger) y te acerca a lo sistémico (qué test/alerta/review faltaba). Cierra
**siempre** con la señal nueva que detectaría el fallo la próxima vez.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: los 3 `.md`),
- la **rúbrica**: `.ai/rubricas/track-0/historia-falla-produccion.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

> "Corrige `ejercicios/track-0/historia-falla-produccion/` usando el framework de
> `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en
`.ai/soluciones/track-0/historia-falla-produccion/` — no la mires antes de
intentarlo. El corrector revisará tu **proceso** (¿el incidente es real? ¿la causa
raíz es blameless y sistémica? ¿cerraste el loop con una señal nueva?), no si tu
incidente es "espectacular".
