---
ejercicio_id: fase-1/js-pipeline-inmutable
fase: fase-1
sub_unidad: "1.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Pipeline de pedidos inmutable

## Respuesta canónica

```javascript
export function pagados(pedidos) {
  return pedidos.filter((p) => p.pagado);
}

export function conIva(pedidos, tasa) {
  // spread copia los campos viejos y agrega el nuevo: NO muta `p`.
  return pedidos.map((p) => ({ ...p, totalConIva: p.total * (1 + tasa) }));
}

export function totalRecaudado(pedidos) {
  return pedidos
    .filter((p) => p.pagado)
    .reduce((acc, p) => acc + p.total, 0); // valor inicial 0: obligatorio en la práctica
}
```

## Razonamiento paso a paso

1. **`pagados` es un `filter` directo.** El predicado `p => p.pagado` ya devuelve un booleano, no hace
   falta `=== true`. `filter` produce un **array nuevo**; el original no se toca.
2. **`conIva` es un `map` con spread.** Cada elemento se transforma en un objeto **nuevo**
   `{ ...p, totalConIva }`. El spread es la clave de la inmutabilidad: copia los campos de `p` y añade
   `totalConIva` sin tocar `p`. Hacer `p.totalConIva = ...` adentro de un `map`/`forEach` "funciona"
   visualmente pero **muta** el objeto original — el bug que el test de no-mutación caza.
3. **`totalRecaudado` compone `filter` + `reduce`.** Primero descarta los no pagados, luego colapsa a
   un número. El **valor inicial `0`** no es decorativo: sin él, `reduce` sobre una lista vacía lanza
   `TypeError: Reduce of empty array with no initial value`. El test de lista vacía lo verifica.

## Por qué la inmutabilidad (lo que de verdad enseña el ejercicio)

Mutar datos de entrada siembra bugs "a distancia": una función cambia un objeto y otra, tres llamadas
después, recibe algo distinto de lo que esperaba, sin rastro de quién lo cambió. Devolver datos nuevos
(`{ ...viejo, cambio }`, `filter`/`map` que no mutan) hace el flujo **predecible**: nadie te cambia un
objeto a tus espaldas. Es el mismo principio que sostiene el modelo de estado de React (F4) y que hace
los tests confiables. El corrector debe verificar que el alumno **entiende** esto, no solo que pasó.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`forEach` que muta.** `pedidos.forEach(p => p.totalConIva = ...)` muta los objetos originales y
   además devuelve `undefined`. Cazar: el test `"conIva NO muta los objetos originales"` falla.
2. **`reduce` sin `0`.** Pasa los tests con datos no vacíos pero revienta en `totalRecaudado([])`.
3. **`totalRecaudado` que olvida `filter`.** Suma también los no pagados → 3500 en vez de 2700.
4. **`push` a un array externo** en vez de `map`/`filter`: estilo no idiomático, marca C3.

## Rango de soluciones aceptables
- **Encadenar vs separar pasos:** `filter(...).reduce(...)` en una expresión o en dos variables
  intermedias es igual de válido.
- **`=== true` explícito** en el predicado de `pagados` es innecesario pero no incorrecto.
- **`conIva` con `Object.assign({}, p, { totalConIva })`** en vez de spread: equivalente y correcto
  (mismo efecto inmutable); spread es lo idiomático en 2026.
- **`totalRecaudado` con `reduce` que filtra dentro** (`(acc, p) => p.pagado ? acc + p.total : acc`)
  sin `filter` previo: válido y hasta más eficiente; `excelente` si lo justifica.
- **Mutar la entrada de cualquier forma:** no es aceptable, baja a `incompleto` en C2 aunque el
  resultado numérico sea correcto — es justo lo que el ejercicio prohíbe.
