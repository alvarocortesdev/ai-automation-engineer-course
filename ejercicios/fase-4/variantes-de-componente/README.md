# Ejercicio 4.9 A — Reconstruye el motor de variantes (mini-cva)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.9` Design systems
**Ruta:** opcional / profundización · **Modalidad:** código · **Timebox:** 40 min

## 🎯 Objetivo

Implementar `variants()`, una versión mínima de lo que hace `class-variance-authority` (cva) por debajo: un **mapeo de props a clases** basado en tokens, con `base`, `variants` y `defaultVariants`. Entender este motor es entender qué te da shadcn/ui —y dejar de pegar código que no comprendes—.

## 📋 Contexto

En la lección viste que un componente reutilizable de un design system (el `Button` de shadcn) usa `cva` para convertir props (`variant`, `size`) en el string de clases-token correcto. Aquí reconstruyes ese motor a mano. Es pura lógica: nada de React ni DOM. Cuando lo entiendas desde dentro, `cva` deja de ser magia y `npx shadcn add button` deja de ser cargo cult.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** de cva: <https://cva.style/docs>.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el motor.
4. Mañana, **reconstrúyelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `variants.ts`. Implementa la función respetando la firma exportada (no cambies el nombre `variants` ni los tipos).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test propio** en `variants.test.ts` (un caso borde: tres ejes, un default que apunta a una opción inexistente, una prop con una clave que no es un eje, etc.).

> El motor que construyes es deliberadamente mínimo. El `cva` real añade `compoundVariants` (clases que aplican solo ante una **combinación** de variantes), `VariantProps` (derivar los tipos de las props desde la config) e integración con `tailwind-merge`. Parte de la nota "hecho" es que puedas explicar qué añade el real sobre el tuyo.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] La clase `base` aparece **siempre** y **primero**.
- [ ] Sin props, se aplican los `defaultVariants`; con props, ganan las props.
- [ ] Con varios ejes, se concatenan en el **orden de declaración** de `config.variants`.
- [ ] Una opción inexistente o `undefined` **cae al default** del eje (no rompe, no cuela `undefined`).
- [ ] El resultado usa **un solo espacio** y no deja espacios al inicio/fin (pista: `filter(Boolean).join(" ")`).
- [ ] Todos los tests pasan y agregaste un test propio.
- [ ] Puedes **explicar sin notas** cómo este motor hace consistente un componente y qué añade el `cva` real.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`variants` es una *factory*: devuelve una función. Dentro, parte de un arreglo `[config.base]`. Recorre las
claves de `config.variants` (cada eje): la opción elegida es la de las props o, si esa no existe en el eje (o
es `undefined`), la de `config.defaultVariants`. Si la opción existe, empuja su string de clases. Al final,
`arreglo.filter(Boolean).join(" ")` limpia vacíos y `undefined` y une con un espacio. Tiparlo con generics
es opcional para pasar los tests; primero el comportamiento. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/variantes-de-componente/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/variantes-de-componente.md` — no la mires antes de intentarlo de verdad.
