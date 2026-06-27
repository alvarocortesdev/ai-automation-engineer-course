---
ejercicio_id: fase-4/filtro-buscable-react
fase: fase-4
sub_unidad: "4.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Filtro buscable tipado

## Respuesta canónica

```tsx
import { useState } from "react";

export interface FiltroBuscableProps {
  items: string[];
  placeholder?: string;
}

export function FiltroBuscable({ items, placeholder }: FiltroBuscableProps) {
  const [query, setQuery] = useState<string>("");

  // Estado DERIVADO: se calcula en el render. Sin useEffect, sin segundo useState.
  const q = query.toLowerCase();
  const visibles = items.filter((item) => item.toLowerCase().includes(q));

  return (
    <div>
      <input
        type="text"
        value={query}
        placeholder={placeholder}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
      />
      {visibles.length === 0 ? (
        <p>Sin resultados</p>
      ) : (
        <ul>
          {visibles.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Razonamiento paso a paso
- **Props tipadas:** la `interface` documenta el contrato; `placeholder?` es opcional y se reenvía tal cual al `<input>`.
- **Input controlado:** `value={query}` + `onChange` que llama a `setQuery`. React es la única fuente de verdad del texto. Sin el `onChange`, el input quedaría de solo lectura.
- **Estado derivado (el punto del ejercicio):** `visibles` es una **constante calculada en el render**, no estado. Cuando `setQuery` agenda un re-render, la función del componente se vuelve a ejecutar entera y `visibles` se recalcula con la consulta nueva. Por eso **no hace falta `useEffect` ni un segundo `useState`**: el cálculo nunca queda desfasado. Un efecto aquí solo añadiría un render extra y una segunda fuente de verdad.
- **Lista y keys:** `key={item}` es estable y único (los items del test no se repiten). El índice sería mala key si la lista se reordenara.
- **"Sin resultados":** render condicional sobre `visibles.length === 0`. Cuando no hay match, no se renderiza ningún `<li>` (el test verifica `listitem` con largo 0).

## Puntos resbalosos (donde el corrector debe mirar)
1. **El antipatrón que pasa los tests:** un alumno puede resolverlo con `const [filtrados, setFiltrados] = useState(items)` + `useEffect(() => setFiltrados(...), [query, items])`. **Los tests pasan en verde igual.** Eso NO es competente en C3: es exactamente lo que la lección combate. Hay que abrir el `.tsx` y verificar que no haya efecto ni estado redundante.
2. **Input no controlado:** leer el valor con un `ref` en vez de `value`/`onChange`. Rompe O1 aunque "funcione".
3. **Case-sensitive:** olvidar `.toLowerCase()` en un lado. El test `filtra por substring sin distinguir mayúsculas` lo atrapa.
4. **`key={index}`:** los tests no lo detectan (no reordenan), pero es observación válida de C2; React tampoco advierte si las keys son únicas.
5. **Marcadores/firma:** si cambió el nombre del export o la `interface`, los tests fallan al importar; pídele restaurar la firma antes de evaluar el resto.

## Rango de soluciones aceptables
- `<div>` o un fragmento `<>...</>` como contenedor: ambos válidos.
- Filtrar con `includes`, `startsWith`, o `RegExp`: válido mientras sea case-insensitive y por substring (el test usa substring).
- Mostrar "Sin resultados" con `&&` o con ternario: ambos válidos mientras no renderice `<li>`.
- Calcular `q = query.toLowerCase()` una vez o inline en cada item: equivalente (la versión una-vez es marginalmente mejor; no es criterio de nota).
- Envolver el filtro en `useMemo(() => items.filter(...), [items, query])`: **aceptable** (no rompe el ejercicio), pero el corrector debe notar que aquí es innecesario para una lista chica y mencionar el React Compiler; lo importante es que **no** haya `useEffect`/estado redundante.
- Tipar el evento explícito o dejar que se infiera: ambos válidos; tiparlo suma en C1-excelente.
