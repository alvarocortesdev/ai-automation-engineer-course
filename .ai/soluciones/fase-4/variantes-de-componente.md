---
ejercicio_id: fase-4/variantes-de-componente
fase: fase-4
sub_unidad: "4.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Motor de variantes (mini-cva)

## Respuesta canónica

```ts
export type VariantDefs = Record<string, Record<string, string>>;

export interface VariantsConfig {
  base?: string;
  variants?: VariantDefs;
  defaultVariants?: Record<string, string>;
}

export type VariantProps = Record<string, string | undefined>;

export function variants(
  config: VariantsConfig,
): (props?: VariantProps) => string {
  const { base, variants: defs = {}, defaultVariants = {} } = config;

  return (props = {}) => {
    const out: (string | undefined)[] = [base];

    for (const axis of Object.keys(defs)) {
      const options = defs[axis];
      // Opción de las props; si no existe en el eje o es undefined, cae al default.
      let chosen = props[axis];
      if (chosen == null || options[chosen] === undefined) {
        chosen = defaultVariants[axis];
      }
      if (chosen != null) out.push(options[chosen]);
    }

    // filter(Boolean) descarta base ausente, "", y undefined; join con un espacio.
    return out.filter(Boolean).join(" ");
  };
}
```

## Razonamiento paso a paso
- **Factory que devuelve función:** `variants(config)` se llama una vez (al definir el componente) y devuelve la función que se invoca en cada render. Es exactamente el patrón de `cva`.
- **`base` primero:** se inicializa el arreglo con `[base]`, así siempre encabeza y `filter(Boolean)` lo quita si es `undefined` (config sin base).
- **Orden de ejes = orden de declaración:** `Object.keys(defs)` recorre las claves en el orden en que se escribieron, por eso `variant` sale antes que `size`.
- **Fallback robusto:** `chosen = props[axis]`; si es `null/undefined` **o** no es una clave del eje (`options[chosen] === undefined`), se reemplaza por `defaultVariants[axis]`. Eso cubre tanto "no pasaron la prop" como "pasaron una opción inexistente (`xl`)".
- **Limpieza:** `out.filter(Boolean).join(" ")` elimina vacíos (`""` de la variante `ghost`), `undefined` (eje sin opción válida ni default) y une con **un** espacio, sin sobrantes.

## Puntos resbalosos (donde el corrector debe mirar)
1. **No descartar `undefined`/vacíos:** un `out.join(" ")` sin `filter(Boolean)` produce `"btn  h-10"` (doble espacio) o cuela `undefined`; el test de limpieza y el de `ghost` lo atrapan.
2. **No hacer fallback ante opción inexistente:** si solo cubre `undefined` con `??` pero no el caso "clave que no existe", `button({ size: "xl" })` daría `"btn bg-primary"` (sin tamaño) en vez de caer a `h-10`. El test `unknown -> default` lo atrapa.
3. **Romper el orden de ejes:** ordenar alfabéticamente o invertir produce `"btn h-9 border"` en vez de `"btn border h-9"`. El test de orden lo atrapa.
4. **Mutar/olvidar la base:** no incluir `base`, o ponerla al final, falla `defaults` y `base first`.
5. **Sobre-ingeniería:** intentar replicar `compoundVariants` o `tailwind-merge` no se pide y suele introducir bugs; el motor mínimo basta. Si el alumno los agregó **bien** y los explica, es C-excelente, no penalizar.

## Rango de soluciones aceptables
- Usar `reduce`/`map` en vez del `for...of`: válido mientras respete orden y limpieza.
- Tipado más estricto con generics (inferir las claves de cada eje y derivar un `VariantProps` tipado): **excelente**, no obligatorio. Los tests pasan con el tipado laxo del starter.
- Implementar el fallback solo con `props[axis] ?? defaultVariants[axis]` **y además** validar `options[chosen]` antes de empujar: equivalente; lo importante es que la opción inexistente no rompa.
- Concatenar con un array y `join`, o construir el string con un acumulador: ambos válidos.
- Que NO se acepta como completo: una versión que solo concatene `base` + lo que venga en props sin defaults ni fallback (es el `if/else` del non-example de la lección con otro nombre).

## Qué premiar
- Que sepa **explicar** que este motor es lo que hace consistente al componente (props tipadas → clases-token fijas, en vez de clases improvisadas) y que nombre qué añade el `cva` real: `compoundVariants`, `VariantProps`, y `tailwind-merge` (vía `cn`) para resolver conflictos de clases.
