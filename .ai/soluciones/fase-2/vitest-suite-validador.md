---
ejercicio_id: fase-2/vitest-suite-validador
fase: fase-2
sub_unidad: "2.6"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Suite Vitest para un validador

## Suite canónica (`solucion.test.ts`)

```ts
import { describe, it, expect, vi } from "vitest";
import { esEmailValido, registrar } from "./solucion";

describe("esEmailValido", () => {
  it.each([
    // válidos (recuerda: normaliza trim + lowercase ANTES de validar)
    { entrada: "ana@correo.com", esperado: true },
    { entrada: " A@B.com ", esperado: true },   // espacios + mayúsculas
    { entrada: "u@sub.dominio.cl", esperado: true },
    // inválidos
    { entrada: "sin-arroba", esperado: false },  // no hay @
    { entrada: "@dominio.com", esperado: false },// parte local vacía
    { entrada: "a@b", esperado: false },         // dominio sin punto
    { entrada: "a@b.", esperado: false },        // dominio termina en punto
  ])("$entrada -> $esperado", ({ entrada, esperado }) => {
    expect(esEmailValido(entrada)).toBe(esperado);
  });
});

describe("registrar", () => {
  it("normaliza y NO avisa cuando el email es válido", () => {
    const logger = { warn: vi.fn() };
    const resultado = registrar(" A@B.com ", logger);
    expect(resultado).toBe("a@b.com");
    expect(logger.warn).not.toHaveBeenCalled();
  });

  it("devuelve null y avisa cuando el email es inválido", () => {
    const logger = { warn: vi.fn() };
    const resultado = registrar("sin-arroba", logger);
    expect(resultado).toBeNull();
    expect(logger.warn).toHaveBeenCalledWith("email inválido: sin-arroba");
  });
});
```

Se corre con `pnpm install` (una vez) y `pnpm test` (`vitest run`).

## Tabla de comportamiento del SUT (para verificar los `esperado`)

| entrada | normaliza a | `esEmailValido` | por qué |
|---|---|---|---|
| `"ana@correo.com"` | `ana@correo.com` | true | `@` interno, dominio con punto |
| `" A@B.com "` | `a@b.com` | true | trim + lowercase **antes** de validar |
| `"u@sub.dominio.cl"` | igual | true | dominio con puntos |
| `"sin-arroba"` | igual | false | `indexOf("@") === -1` → `at <= 0` |
| `"@dominio.com"` | igual | false | `at === 0` → parte local vacía |
| `"a@b"` | igual | false | dominio sin `.` |
| `"a@b."` | igual | false | dominio termina en `.` |

## Por qué se mockea `logger` y NO el validador
- `logger.warn` es la **frontera**: en producción escribiría a un archivo o a un servicio de observabilidad (logs/trazas). Mockeado con `vi.fn()`, el test es aislado y puede **afirmar la interacción** (avisó / no avisó).
- `esEmailValido` y `normalizarEmail` son **lógica pura**: son lo que el test verifica de verdad. Mockearlas sería sobre-mockeo y dejaría el comportamiento real sin probar.

## Mapa de equivalencias pytest ↔ Vitest (el corrector puede usarlo para feedback)
| pytest | Vitest |
|---|---|
| `@pytest.mark.parametrize` | `it.each` / `test.each` |
| `unittest.mock.Mock()` | `vi.fn()` |
| `mock.assert_called_once_with(x)` | `expect(fn).toHaveBeenCalledWith(x)` |
| `mock.assert_not_called()` | `expect(fn).not.toHaveBeenCalled()` |
| `pytest.raises(Err)` | `expect(() => ...).toThrow(Err)` |

## Puntos resbalosos
1. **La normalización**: el error #1 es marcar `" A@B.COM "` como inválido. Verificar que el alumno entendió que se normaliza antes de validar.
2. **`toBeNull()` vs `toBe(null)`**: ambos válidos.
3. **Camino feliz del logger**: el `not.toHaveBeenCalled` del caso válido es fácil de olvidar y es justo el que garantiza que un email correcto no genera ruido.
4. **`vi.mock` innecesario**: si automockeó el módulo entero con `vi.mock('./solucion')`, sobra y delata receta pegada; el ejercicio se resuelve inyectando el doble del logger.
5. **pnpm, no npm**: regla del curso.

## Rango de soluciones aceptables
- **Más o distintos bordes** mientras cumpla ≥3 válidos y ≥3 inválidos con bordes reales.
- **`toHaveBeenCalled()` sin `With`** en el caso inválido: aceptable; con el mensaje exacto es más estricto y mejor.
- **`describe` único** o dos `describe`: indistinto.
- **Tabla con arrays `[entrada, esperado]`** en vez de objetos: válido; los objetos dan nombres de caso más legibles con `$entrada`.
