# Ejercicio 4.2 — Criterio: utilidades, componente o `@apply`

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.2` Tailwind CSS
**Ruta:** crítica · **Modalidad:** a mano (razonamiento de diseño) · **Timebox:** 25–35 min

## 🎯 Objetivo

Decidir, para varios casos de utilidades repetidas, **la salida correcta** —dejar las utilidades / extraer un componente / usar `@apply`— y **defender el trade-off**. Es el criterio que separa a quien usa Tailwind de quien lo domina.

## 📋 Contexto

En el [Capstone F4](/fase-4-frontend/proyecto/) vas a tener botones, mensajes y avatares que se repiten. Decidir bien cuándo abstraer (y en qué forma) es lo que evita que tu proyecto termine con una capa de CSS global frágil —justo lo que utility-first vino a eliminar—. Este ejercicio entrena ese juicio **sin escribir UI**: solo razonas.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Sin IA, sin buscar "la respuesta correcta".
2. Si dudas, relee la sección 6 de la lección y la documentación oficial de Tailwind ("Reusing styles").
3. **Solo al final**, usa IA para *cuestionar* tu razonamiento —no para que decida por ti.
4. Al día siguiente, reescribe tu **regla general** de memoria. Si no te sale, no la interiorizaste.

## 🛠️ Instrucciones

Abre `decisiones.md` (ya trae la estructura) y resuelve los **cuatro escenarios**. Para cada uno: **(a)** elige una salida —`utilidades` / `componente` / `@apply`—, y **(b)** justifícala en **una o dos frases** respondiendo las dos preguntas rectoras:

- ¿**Controlo el marcado** (es mi HTML/JSX) o es de un tercero / generado?
- ¿Se repite la **estructura completa** en varios lugares, o es algo de **una sola vez**?

### Los escenarios

1. **Botón repetido.** El mismo `<button>` con la misma tira de clases (`rounded-md bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-700`) aparece en **12 pantallas** de tu app React.
2. **Hero único.** Una sección "hero" de tu landing con un layout particular que usas **una sola vez** en todo el sitio.
3. **Librería de terceros.** Integras un date-picker que renderiza **sus propios** `<div class="dp-cell">` (tú no escribes ese HTML) y necesitas estilarlo para que combine con tu app.
4. **Markdown renderizado.** Tu blog convierte Markdown a HTML (`<h1>`, `<p>`, `<ul>`…) en tiempo de render; necesitas que esos elementos tengan tu estilo, pero **no escribes ese marcado a mano**.

Cierra con una **regla general propia** (una frase) que resuma cuándo extraer componente y cuándo `@apply`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los **cuatro** escenarios tienen una decisión **explícita** y una justificación que menciona si controlas el marcado y si se repite la estructura.
- [ ] El escenario 1 termina en **componente** (no `@apply`) y explicas por qué la extracción de componente le gana.
- [ ] Los escenarios 3 y 4 reconocen que **no controlas el marcado** → `@apply` (o `@variant`) es el caso legítimo.
- [ ] El escenario 2 reconoce que **una sola vez no se abstrae** (dejar utilidades).
- [ ] Tu **regla general** pone "¿controlo el marcado?" como el eje de la decisión.
- [ ] Puedes **defender sin notas** por qué usar `@apply` para "limpiar" HTML propio que se ve cargado es un anti-patrón.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Hazte SIEMPRE las dos preguntas en orden. Primera: *¿es mío el HTML?* Si no (librería, markdown), no hay componente que extraer → `@apply`. Segunda, solo si es tuyo: *¿se repite la estructura completa en varios lugares, o es de una vez?* Repetida → componente; única → déjala. El error clásico (y lo que el ejercicio busca que nombres) es usar `@apply` para "ordenar" HTML propio cargado: eso reintroduce el CSS global y el acoplamiento que Tailwind elimina. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/tailwind-cuando-extraer/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector evaluará tu **criterio** (no si "acertaste la palabra"): la calidad de cada justificación y de tu regla general. La **solución de referencia** vive en `.ai/soluciones/fase-4/tailwind-cuando-extraer.md` — no la mires antes de intentarlo.
