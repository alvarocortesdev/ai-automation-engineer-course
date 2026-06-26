---
ejercicio_id: fase-1/result-discriminated-union-ts
fase: fase-1
sub_unidad: "1.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — El patrón Result con discriminated unions en TypeScript

## Respuesta canónica

```ts
export type Result<T, E> =
  | { ok: true; value: T }
  | { ok: false; error: E };

export type Gasto = { comercio: string; monto: number; categoria: string };

export type ParseError =
  | { tipo: "formato"; mensaje: string }
  | { tipo: "monto"; mensaje: string };

export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });

export function parseGasto(linea: string): Result<Gasto, ParseError> {
  const partes = linea.split(";").map((p) => p.trim());
  if (partes.length !== 3) {
    return err({ tipo: "formato", mensaje: `esperaba 3 campos, llegaron ${partes.length}` });
  }

  const [comercio, montoRaw, categoria] = partes;
  if (comercio.length === 0 || categoria.length === 0) {
    return err({ tipo: "formato", mensaje: "comercio y categoría no pueden ser vacíos" });
  }

  const monto = Number(montoRaw);
  if (!Number.isInteger(monto) || monto <= 0) {
    return err({ tipo: "monto", mensaje: `monto inválido: ${montoRaw}` });
  }

  return ok({ comercio, monto, categoria });
}

export function safeJsonParse(raw: string): Result<unknown, Error> {
  try {
    return ok(JSON.parse(raw));
  } catch (e) {
    return err(e instanceof Error ? e : new Error(String(e)));
  }
}
```

Llamador idiomático (no lo piden los tests, pero es lo que distingue a un `excelente`):

```ts
const r = parseGasto(linea);
if (r.ok) {
  registrar(r.value);                 // TS sabe: r.value es Gasto
} else {
  switch (r.error.tipo) {             // TS sabe: r.error es ParseError
    case "formato": /* ... */ break;
    case "monto":   /* ... */ break;
    default: {
      const _exhaustivo: never = r.error;   // un tipo nuevo sin case => NO compila
      throw new Error(`tipo no manejado: ${JSON.stringify(_exhaustivo)}`);
    }
  }
}
```

## Razonamiento paso a paso

1. **Discriminated union.** `Result<T, E>` tiene un campo común `ok` (el discriminante). Tras
   `if (r.ok)`, TS **estrecha** el tipo: en la rama `true` existe `value: T`; en la `false`, `error: E`.
   No hace falta `as` ni `!`.
2. **Helpers con `never`.** `ok` devuelve `Result<T, never>` y `err` devuelve `Result<never, E>`. Como
   `never` es el tipo vacío (asignable a todo), ambos encajan en cualquier `Result<T, E>`. Esto evita
   fricción de tipos al devolverlos desde una función con `E` concreto.
3. **El error es parte del contrato.** `parseGasto(linea): Result<Gasto, ParseError>` declara el fallo
   en la firma. El llamador **no puede** usar el `Gasto` sin discriminar `ok`. Eso es lo que un `throw`
   nunca logra: en TS (igual que en Python) la firma no dice qué se lanza.
4. **Validación correcta del monto.** `Number(montoRaw)` + `Number.isInteger` + `> 0`. Cuidado con las
   alternativas flojas: `parseInt("12abc")` daría `12`; `Number("")` daría `0` (pero el campo vacío ya
   se atrapó antes por `length === 0`).
5. **Domar el throw (`safeJsonParse`).** `JSON.parse` **sí** lanza. Lo envolvemos en `try/catch` y lo
   convertimos en `Result`. En `strict`, `catch (e)` tipa `e` como `unknown`: hay que estrechar
   (`e instanceof Error`) antes de usarlo, y normalizar el caso no-`Error` con `new Error(String(e))`.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`parseGasto` que lanza** en algún rama → rompe la promesa "nunca lanza" (el punto del patrón).
2. **`catch (e)` asumiendo `Error`** (`e.message` directo) → en strict no compila; señal de no entender `unknown`.
3. **`tipo` cruzado** (devolver `monto` donde corresponde `formato` o viceversa) → fallan los tests del `tipo`.
4. **Aceptar decimales o ≤ 0** (`Number.isFinite` en vez de `isInteger`, u olvidar `> 0`) → `test monto con decimales` / `monto <= 0` fallan.
5. **Helpers sin `never`** → puede compilar, pero genera fricción; señalar como subóptimo, no como error.
6. **Usar `r.value`/`r.error` sin narrowing** y "arreglarlo" con `as`/`!` → apaga la seguridad de tipos.

## Rango de soluciones aceptables
- **Forma de `Result`:** aceptable usar `success`/`failure` en vez de `ok`/`error`, o `kind: "ok"|"err"` como discriminante, siempre que sea una discriminated union consistente. `ok` booleano es lo más limpio.
- **Validación del monto:** `Number(...)` + `Number.isInteger`; aceptable `Number.isFinite` + chequeo de parte decimal si lo justifica. No aceptable `parseInt` a secas (acepta basura).
- **`safeJsonParse`:** aceptable devolver `Result<unknown, Error>` (mejor) o `Result<unknown, unknown>`; lo esencial es que **no propague** el throw y que estreche `e`.
- **Llamador exhaustivo:** el `const _: never` es deseable (`excelente`) pero no exigido por los tests; su ausencia no baja de `competente` si todo lo demás está.
- **Librería (`neverthrow`/`Effect`):** si el alumno la usó, pedir que lo haya hecho **a mano** primero; el ejercicio es entender el patrón, no consumirlo.
- **No aceptable:** `parseGasto` con tipo de retorno `Gasto` que lanza; o un `safeJsonParse` que deja escapar la `SyntaxError`.
