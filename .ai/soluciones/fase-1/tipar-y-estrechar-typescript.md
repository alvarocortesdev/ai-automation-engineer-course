---
ejercicio_id: fase-1/tipar-y-estrechar-typescript
fase: fase-1
sub_unidad: "1.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Tipar y estrechar un módulo TypeScript

## Respuesta canónica

```ts
export interface Producto {
  id: number;
  nombre: string;
  stock: number;
  categoria: "fresco" | "seco" | "congelado";
}

export type EventoStock =
  | { kind: "add"; cantidad: number }
  | { kind: "remove"; cantidad: number }
  | { kind: "set"; valor: number };

export function aplicarEvento(stockActual: number, evento: EventoStock): number {
  switch (evento.kind) {
    case "add":
      return stockActual + evento.cantidad;
    case "remove":
      return Math.max(0, stockActual - evento.cantidad);
    case "set":
      return evento.valor;
    default: {
      const _exhaustivo: never = evento; // si se agrega un kind sin case, tsc falla aquí
      return _exhaustivo;
    }
  }
}

export function crearProducto(datos: Omit<Producto, "id">, id: number): Producto {
  return { id, ...datos };
}

export function esEventoSet(
  evento: EventoStock,
): evento is Extract<EventoStock, { kind: "set" }> {
  return evento.kind === "set";
}
```

Con esto, `npm run typecheck` reporta 0 errores y pasan los tests.

## Razonamiento paso a paso

1. **`Producto` como `interface`** con `categoria` modelada como **unión de literales** (`"fresco" | "seco" | "congelado"`), no como `string`: así `tsc` rechaza una categoría inventada y la sección 5 (no usar `enum`) se respeta.
2. **`EventoStock` como unión discriminada.** Cada variante lleva el discriminante `kind` con un literal distinto. Eso permite el narrowing: dentro de `case "add"`, TypeScript sabe que `evento` tiene `cantidad`; dentro de `case "set"`, que tiene `valor` (y no `cantidad`).
3. **`aplicarEvento` con `switch` + `never`.** El `switch (evento.kind)` estrecha en cada rama **sin `as`**. En `remove`, `Math.max(0, ...)` cumple la regla de no bajar de 0. El `default` con `const _exhaustivo: never = evento` es la red de exhaustividad: cuando los tres `kind` están manejados, `evento` es `never` ahí (compila); si se agrega un `kind` y falta su `case`, `evento` deja de ser `never` y `tsc` falla justo en esa línea.
4. **`crearProducto` con `Omit`.** `Omit<Producto, "id">` deriva el tipo de entrada de la fuente de verdad (`Producto`) sin re-escribir los campos. `return { id, ...datos }` arma el producto completo.
5. **`esEventoSet` como type guard.** La firma `evento is Extract<EventoStock, { kind: "set" }>` convierte la función en un predicado de tipo: quien la use estrecha `evento` a la variante `set` en la rama `true`. Con `: boolean` filtraría en runtime pero no estrecharía.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Acceder a `evento.valor`/`evento.cantidad` con `as`** en vez de estrechar por `kind`: pasa los tests, anula el objetivo. Mirar que use `switch`/`if` sobre `evento.kind` y nada de `as`.
2. **Falta el chequeo `never`**: el `switch` puede funcionar con solo los tres `case`; sin el `default` con `never` no hay exhaustividad. Marcar siempre.
3. **`crearProducto` re-declarando campos** (`datos: { nombre: string; stock: number; categoria: ... }`): funciona pero duplica; el objetivo pide `Omit`.
4. **`esEventoSet` con retorno `boolean`**: no es type guard. Verificar la firma `evento is ...`.
5. **`any` residual** en cualquier parte: incumple el criterio explícito.

## Rango de soluciones aceptables
- **Narrowing**: aceptar `if/else if` sobre `evento.kind` en vez de `switch`, siempre que haya exhaustividad equivalente (un `else` con `const _: never = evento`). El `switch` es lo idiomático.
- **Type guard**: aceptar repetir el tipo literal de la variante (`evento is { kind: "set"; valor: number }`) en vez de `Extract<...>`. `Extract` es `excelente` por no duplicar.
- **`remove` sin bajar de 0**: `Math.max(0, ...)` o un `if (stock - cantidad < 0) return 0;`. Ambos válidos.
- **`crearProducto`**: aceptar `{ id, nombre: datos.nombre, ... }` explícito, pero señalar que el spread es más limpio; lo no aceptable es duplicar el **tipo** (debe ser `Omit`).
- **`categoria`**: si la modela como un `type Categoria = "fresco" | "seco" | "congelado"` aparte y lo reutiliza, es **mejor** (excelente).
- No aceptable: `// @ts-ignore`, `as any`, o `enum` sin justificar.
