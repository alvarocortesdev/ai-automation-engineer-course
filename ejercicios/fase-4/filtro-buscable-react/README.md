# Ejercicio 4.5 A — Filtro buscable tipado (sin un solo useEffect)

**Fase:** Fase 4 — Frontend + UI/UX · **Lección:** `4.5` React + TypeScript
**Ruta:** crítica · **Modalidad:** código · **Timebox:** 40 min

## 🎯 Objetivo

Implementar un componente `FiltroBuscable` en **React 19 + TypeScript** con **props tipadas**, un **input controlado** y una lista filtrada en vivo (sin distinguir mayúsculas), donde el resultado filtrado es **estado derivado** —se calcula en el render—. La trampa que este ejercicio te obliga a evitar: **no debe haber ningún `useEffect` ni un segundo `useState` para la lista filtrada**.

## 📋 Contexto

Este es el patrón base de la interfaz de chat del **Capstone F4** (frontend de una app de IA): un input controlado + una lista que reacciona al estado. Si lo dominas sin caer en el antipatrón del efecto que "sincroniza" estado, tienes el músculo central de toda app de React.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea feo y lento.
2. Solo entonces, consulta la **documentación oficial** de React: <https://react.dev/learn> y <https://react.dev/learn/you-might-not-need-an-effect>.
3. **Solo al final**, usa IA para *revisar y explicar* —no para *generar* el componente.
4. Mañana, **reconstrúyelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `FiltroBuscable.tsx`. Implementa el componente respetando la firma exportada (no cambies el nombre ni la `interface`).
2. Instala dependencias y corre los tests:

   ```bash
   pnpm install
   pnpm test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un test propio** en `FiltroBuscable.test.tsx` (un caso borde que se te ocurra: acentos, espacios, lista vacía...).

> El test valida el **comportamiento** (filtrado, placeholder, "Sin resultados"), no la estética. Pero el espíritu del ejercicio es el **método**: si lo resuelves con un `useEffect`, los tests podrían pasar y aun así estaría mal. La corrección con IA revisa que NO uses efecto.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Props tipadas con la `interface FiltroBuscableProps` (`items: string[]`, `placeholder?: string`).
- [ ] Un input **controlado**: su `value` viene del estado y su `onChange` lo actualiza; el placeholder viene de la prop.
- [ ] La lista filtrada se **calcula en el render** (substring, *case-insensitive* contra la consulta).
- [ ] Se renderiza como `<ul>` de `<li>` con `key` **estable** (el propio string del item).
- [ ] Cuando ningún item coincide, se muestra un elemento con el texto exacto `Sin resultados` y ningún `<li>`.
- [ ] **Cero `useEffect`** y **cero estado redundante** para la lista filtrada.
- [ ] Todos los tests pasan y agregaste un test propio.
- [ ] Puedes **explicar sin notas** por qué este componente no necesita `useEffect`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El esqueleto: un `useState<string>("")` para la consulta; una constante calculada en el cuerpo del
componente, `const visibles = items.filter(i => i.toLowerCase().includes(query.toLowerCase()))`;
y el JSX que mapea `visibles` a `<li key={i}>{i}</li>`. El "Sin resultados" es
`{visibles.length === 0 && <p>Sin resultados</p>}`. La idea central: `visibles` se recalcula en
cada render **automáticamente**, porque el componente vuelve a ejecutarse cuando cambia el estado.
Por eso no hace falta un efecto ni un segundo estado. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-4/filtro-buscable-react/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

La **solución de referencia** vive en `.ai/soluciones/fase-4/filtro-buscable-react.md` — no la mires antes de intentarlo de verdad.
