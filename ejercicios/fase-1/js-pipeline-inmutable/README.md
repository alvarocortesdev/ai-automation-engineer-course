# 1.7 — Pipeline de pedidos inmutable

> **Modalidad: código (JavaScript, sin IA).** Entrena los array methods (`filter`/`map`/`reduce`),
> destructuring y spread, con una regla innegociable: **no mutar** los datos de entrada. La
> inmutabilidad no es un capricho — es lo que hace tu código predecible y testeable.

**Fase:** Fase 1 — Lenguajes núcleo · **Lección:** `1.7` JavaScript moderno (ES6+)
**Ruta:** crítica · **Timebox:** 30–40 min

## 🎯 Objetivo

Implementar tres funciones **puras** que transforman una lista de pedidos sin mutar la original ni
sus objetos, usando `filter`/`map`/`reduce` y spread, y explicar por qué la inmutabilidad evita bugs.

## 📋 Contexto

Mover y transformar listas de objetos es el 80% del trabajo diario en JS/TS: filtras, mapeas, resumes.
Hacerlo **sin mutar** el original es el hábito que después hace tu código React (F4) y tus pipelines
predecibles. Este ejercicio es el cimiento del lado JavaScript del **Capstone F1**.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta **documentación oficial** (MDN: Array).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `solucion.js` y completa las tres funciones (`pagados`, `conIva`, `totalRecaudado`). **No
   cambies las firmas.**
2. Corre los tests con el runner integrado de Node (no necesitas instalar nada):

   ```bash
   node --test
   ```

3. Itera hasta que **todos los tests pasen en verde**.
4. Añade al menos **un caso borde tuyo** en `solucion.test.js` (p. ej. ningún pedido pagado, o `tasa = 0`).

### Forma de un pedido

```js
{ id: 1, cliente: "ada", total: 1200, pagado: true }
```

### Contrato de las funciones

- `pagados(pedidos)` → array **nuevo** solo con los pedidos `pagado: true`.
- `conIva(pedidos, tasa)` → array **nuevo**; cada pedido con un campo extra
  `totalConIva = total * (1 + tasa)`, **sin mutar** los objetos originales.
- `totalRecaudado(pedidos)` → un **número**: la suma del `total` de los pedidos pagados (con `reduce`).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Las tres funciones devuelven datos nuevos; `pedidos` y sus objetos quedan **intactos** (el test lo verifica).
- [ ] Usas `filter`/`map`/`reduce`, **no** bucles `for` con `.push()` a una variable externa.
- [ ] `conIva` usa spread (`{ ...p, totalConIva: ... }`) en vez de mutar `p`.
- [ ] Todos los tests pasan y agregaste al menos uno propio.
- [ ] Puedes **explicar sin notas** por qué la inmutabilidad evita bugs.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Piensa cada función como una **transformación pura**: entra un array, sale uno nuevo, nada de afuera
se toca. `pagados` es un `filter` directo. `conIva` es un `map` que devuelve
`{ ...p, totalConIva: p.total * (1 + tasa) }` — el spread copia los campos viejos y agrega el nuevo,
sin tocar `p`. `totalRecaudado` combina: `filter` los pagados y luego
`reduce((acc, p) => acc + p.total, 0)`; recuerda el **valor inicial `0`**. Revisa las secciones 4.3 y
4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-1/js-pipeline-inmutable.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-1/js-pipeline-inmutable.md` — no la mires
antes de intentarlo de verdad.
