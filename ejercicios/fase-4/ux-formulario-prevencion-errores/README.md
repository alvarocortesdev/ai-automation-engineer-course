# Ejercicio 4.10 C — Rediseña la UX de un formulario hostil

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.10` Usabilidad + estados de primera clase
**Ruta:** crítica · **Modalidad:** a mano (razonamiento / diseño, sin código) · **Timebox:** 30–35 min

> **Sin código.** El formulario es donde más fricción sufre el usuario. Vas a **rediseñar su UX por escrito**:
> mensajes de error, *timing* de validación, prevención, *affordances* y feedback. La parte de implementarlo
> en React Hook Form + zod ya la viste en [4.7]; aquí entrenas el **criterio** que decide *qué* implementar.

## 🎯 Objetivo

- **O1** — Reescribir cada mensaje de error con la estructura **qué / por qué / cómo**, sin culpar al
  usuario, y decidir el **timing de validación** de cada campo (onBlur / en vivo tras fallo / submit).
- **O2** — Aplicar **prevención de errores (H5)**, *affordances* y feedback, modelando el **envío** como una
  máquina de estados (loading / error / success).
- **O3** — Conectar al menos **tres** decisiones con la **accesibilidad** (la lección `4.4` Accesibilidad WCAG 2.2).

## 📋 Contexto

El formulario actual está descrito en `formulario-actual.md`: es el "Conectar fuente de datos" de una app
de IA (el usuario pega una API key y una URL para que la app lea sus datos). Funciona, pero es hostil.
Rediseñar su UX es exactamente lo que harás con el input del prompt y los ajustes de tu capstone.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Apóyate en la sección 4.4 de la lección (UX de formularios).
2. Documentación oficial permitida (NN/g error-message guidelines, MDN Forms, WCAG).
3. **Solo al final**, usa IA para *contrastar* tu rediseño — no para *generarlo*.
4. Mañana, toma un formulario que uses a diario y repite el ejercicio de memoria sobre un campo.

## 🛠️ Instrucciones

Lee `formulario-actual.md` y escribe tu rediseño en `rediseno-ux.md` con estas cuatro partes:

1. **Mensajes de error reescritos:** una tabla `mensaje actual → mensaje nuevo` para cada error, aplicando
   qué/por qué/cómo y eliminando la culpa.
2. **Timing de validación por campo:** para cada campo, cuándo validas (onBlur la primera vez / en vivo solo
   tras el primer fallo / al enviar) y por qué.
3. **Prevención, affordances y feedback:** al menos **dos** medidas de prevención (H5), cómo se ve un campo
   válido/inválido/deshabilitado, y los **estados del envío** (botón "Enviando…" deshabilitado; éxito;
   error).
4. **Accesibilidad:** al menos **tres** decisiones atadas a la a11y (errores con `role="alert"`, `<label>`
   asociados, foco al primer campo con error, contraste del estado de error).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] **Cada mensaje de error reescrito** con qué/por qué/cómo y sin culpar al usuario (con ejemplo de
      formato cuando aplique).
- [ ] **Timing de validación decidido por campo** y justificado (nada de validar en cada tecla desde la
      primera letra).
- [ ] **Al menos dos medidas de prevención (H5)**: constraints de input, formato de ejemplo, valor por
      defecto, selector en vez de texto libre, confirmación/deshacer para lo destructivo.
- [ ] **El envío tiene sus propios estados** (loading/error/success), no solo "se manda y ya".
- [ ] **Al menos tres conexiones con la a11y** explícitas.
- [ ] Puedes **defender tus decisiones sin notas** (check de dominio).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Para los mensajes: la plantilla es **qué** falló + **por qué** + **cómo** se arregla, con un ejemplo entre
paréntesis. "API key inválida" → "La API key debe empezar con `sk-` y tener 40+ caracteres (revísala en tu
panel del proveedor)". Para el timing, la regla es "no castigues al que aún escribe": valida al salir del
campo, y solo en vivo si ese campo ya falló una vez. Para prevención, por cada error posible pregúntate
"¿podía evitarlo?" (un `type="url"`, un placeholder de formato, ocultar/mostrar la key con un toggle en vez
de pegarla a ciegas). Para el envío, recuerda que es una **carga**: tiene loading/error/success igual que
cualquier fetch (es la misma máquina de estados de la lección). Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/ux-formulario-prevencion-errores/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **criterio de UX** (mensajes, timing, prevención, a11y), no si coincides palabra
por palabra con la referencia. La **solución de referencia** vive en
`.ai/soluciones/fase-4/ux-formulario-prevencion-errores.md` — no la mires antes de intentarlo de verdad.
