---
ejercicio_id: track-0/cuando-no-usar-ia
fase: track-0
sub_unidad: "T0.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de
> **diseño/razonamiento**: la defensa de cada alumno será distinta. Lo que se mide es el **criterio**
> (romper la dicotomía con evidencia + defender el cuándo-NO con costos reales), no la redacción exacta.

# Solución de referencia — Defiende el cuándo-NO

## 1. Respuesta hablada de referencia (≤8 frases)

> *"Las dos cosas, y esa de hecho es la habilidad: dirijo IA, pero respondo por cada línea —te lo muestro
> con el repo abierto ahora mismo. Aquí, en este capstone, el spec lo escribí yo antes de la primera línea
> de código, y los tests también, en rojo, definiendo qué significaba 'funciona'. Recién entonces dejé que
> el agente propusiera la implementación, y la revisé contra esos tests; en este ADR rechacé algo que
> sugirió porque se rompía con varios workers. Para la parte de IA del proyecto no me fío de que 'se vea
> bien': la mido con un set de casos y un gate en CI. Y soy el primero en apagarla: cuando estoy aprendiendo
> algo nuevo lo hago a mano, porque si delego el pensamiento después no puedo verificar lo que la IA
> produce. La uso para multiplicar, no para pensar por mí —por eso puedo defender este código contigo, sin
> la IA al lado, ahora."*

Por qué funciona: **rompe la dicotomía** en la primera frase (no se defiende ni se disculpa); **ancla en
evidencia abrible** (spec, tests, ADR, evals) aprovechando que la reclutadora tiene el repo abierto;
**toma su honestidad como aliada** ("te lo muestro ahora"); y **cierra con Primero-Sin-IA**. No sobrevende
(no hay "10x") ni se esconde.

## 2. Lista cuándo-NO de referencia

| # | Situación donde NO uso IA | Porqué de ingeniería (costo real) |
|---|---|---|
| 1 | Cuando estoy **aprendiendo** un concepto o lenguaje nuevo. | Delegar el pensamiento me deja sin el fundamento que necesito para luego *poder verificar* el output de la IA; la deuda se paga en la próxima entrevista (live coding en blanco) y en el primer bug que no sé diagnosticar. Es la regla Primero-Sin-IA. |
| 2 | **Debugging** de un sistema cuyo modelo mental aún no tengo. | Pedirle el fix a la IA sin entender el sistema me da una corazonada disfrazada de respuesta; puede "arreglar" el síntoma y dejar la causa. Primero construyo el modelo mental; después, quizá, acelero con IA. |
| 3 | **Código crítico / de seguridad** (auth, manejo de dinero, borrado de datos). | El costo de un error es altísimo y revisar a fondo el output de la IA suele costar más que escribirlo yo; delegar ahí traslada el riesgo, no lo elimina. Lo escribo a mano y lo cubro con tests. |
| 4 | Cuando **revisar costaría más que escribir**. | Si voy a leer 200 líneas generadas con la misma atención con que las habría escrito, no gané tiempo: solo moví el trabajo y agregué el riesgo de aceptar un error sutil. |

## 3. Trade-off de referencia (situación 3: código de pagos)

**Situación:** la lógica de cobro de un sistema de pagos.

**Qué GANO al no usar IA:** control total y revisión a fondo línea por línea; entiendo cada rama y cada
caso borde, así que puedo defenderla y mantenerla; reduzco el riesgo de un error sutil que la IA introduzca
y yo acepte por confiar en que "se ve bien".

**Qué PIERDO:** velocidad —tardo más que si delegara el primer borrador.

Por qué aquí el trade vale la pena: en pagos, un error le cuesta **dinero al cliente y confianza al
equipo**; el tiempo extra es barato comparado con ese riesgo. En un script interno de un solo uso, el saldo
sería al revés y sí delegaría. **Saber distinguir las dos situaciones es el criterio** —no es una regla
dogmática "nunca/siempre".

## 4. Línea anti-sobreventa de referencia

**Frase prohibida:** *"La verdad es que la IA me hace como 10x, ya casi no escribo código a mano."*

**Por qué hunde:** confirma exactamente el miedo de la reclutadora (el candidato que pega lo que no
entiende); es **indefendible** en el live coding sin asistente que viene a continuación; y vende velocidad
en vez de criterio, que es lo opuesto a lo que un rol semi-senior busca. (La frase prohibida del otro
extremo —*"no, yo no uso IA para nada"*— también hunde: o miente con el repo abierto, o suena a purista
lento.)

## Puntos donde el corrector debe mirar
1. **Primera frase.** ¿Rompe la dicotomía o se defiende/disculpa? "Sí uso bastante, pero…" ya es defensiva.
2. **Evidencia abrible.** ¿Apunta a un artefacto específico (spec/tests/ADR/evals) o habla en abstracto?
3. **Porqués con costo.** Cada cuándo-NO debe tener un costo de ingeniería real, no una preferencia.
4. **Trade-off de dos lados.** Debe nombrar ganancia **y** pérdida, y por qué el saldo es a favor *ahí*.
5. **Cierre Primero-Sin-IA.** La mejor defensa termina conectando con "la uso para multiplicar, no para
   pensar".

## Rango de soluciones aceptables
- Cualquier respuesta es válida si rompe la dicotomía, ancla en evidencia y no sobrevende ni oculta; la
  redacción y el artefacto citado son libres.
- La lista cuándo-NO puede traer situaciones distintas (datos sensibles/PII, prototipos vs. producción,
  decisiones de arquitectura) mientras cada una tenga un **costo de ingeniería** real y sean **≥3 y
  distintas**.
- El trade-off puede elegir cualquier situación de la lista; lo no válido es presentar el no-usar-IA como
  gratis (sin costo) o como puro sacrificio (sin ganancia).
- La línea anti-sobreventa puede ser la versión vibe-coder **o** la purista; ambas son aceptables si el
  porqué de por qué hunde es correcto.
- Conectar explícitamente con Primero-Sin-IA y cuantificar costos son bonus de Excelente, no obligatorios
  para Competente.
- Entregar/decir la defensa en inglés suma el bonus del hilo; en español es aceptable.
