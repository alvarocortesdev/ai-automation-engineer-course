---
ejercicio_id: fase-2/playwright-refactor-robusto
fase: fase-2
sub_unidad: "2.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Estabiliza un e2e flaky (refactor robusto + Page Object)

## Diagnóstico canónico (lo que debe haber en `diagnostico.md`)

| # | Antipatrón en el test de partida | Por qué está mal |
|---|---|---|
| 1 | `page.locator("#desc")`, `"#monto"`, `".btn-add"`, `".toast"` | Selectores acoplados a la **implementación** (ids y clases CSS). Un rediseño que renombre la clase o mueva un `div` rompe el test **sin que haya bug**. |
| 2 | `await page.waitForTimeout(1000)` | Un `sleep`. La app muestra el mensaje tras una latencia **variable** (~150–450 ms): 1000 ms es a la vez **lento** (regala ~600–850 ms en cada corrida) y **frágil** (si un día la app tarda más, falla). No hay número correcto. |
| 3 | `const t = await page.locator(".toast").textContent(); expect(t).toContain(...)` | Toma una **foto inmediata** del texto; si el mensaje aún no llegó, `t` es `""`/`null`. No espera ni reintenta. |

Causa raíz común: **afirmar antes de que el estado esté listo**. La cura no es esperar "más", es esperar "lo correcto" con una web-first assertion.

## `gastos.page.ts` de referencia

```ts
import { type Page, type Locator } from "@playwright/test";
import { pathToFileURL } from "node:url";
import path from "node:path";

const APP_URL = pathToFileURL(path.join(__dirname, "app.html")).href;

export class GastosPage {
  readonly page: Page;
  readonly descripcion: Locator;
  readonly monto: Locator;
  readonly agregar: Locator;
  readonly mensajeExito: Locator;
  readonly error: Locator;
  readonly items: Locator;

  constructor(page: Page) {
    this.page = page;
    this.descripcion = page.getByLabel("Descripción");
    this.monto = page.getByLabel("Monto");
    this.agregar = page.getByRole("button", { name: "Agregar" });
    this.mensajeExito = page.getByText("Gasto agregado");
    this.error = page.getByRole("alert");
    this.items = page.getByRole("listitem");
  }

  async goto() {
    await this.page.goto(APP_URL);
  }

  async agregarGasto(descripcion: string, monto: string) {
    await this.descripcion.fill(descripcion);
    await this.monto.fill(monto);
    await this.agregar.click();
  }
}
```

## `gastos.spec.ts` de referencia

```ts
import { test, expect } from "@playwright/test";
import { GastosPage } from "./gastos.page";

test("agrega un gasto válido y aparece en la lista", async ({ page }) => {
  const gastos = new GastosPage(page);
  await gastos.goto();
  await gastos.agregarGasto("Almuerzo", "5000");

  // web-first assertions: auto-esperan la latencia variable, sin sleeps
  await expect(gastos.mensajeExito).toHaveText("Gasto agregado: Almuerzo");
  await expect(gastos.items).toHaveCount(1);
  await expect(gastos.items.first()).toHaveText("Almuerzo: $5000");
});

test("rechaza un monto inválido y no agrega nada", async ({ page }) => {
  const gastos = new GastosPage(page);
  await gastos.goto();
  await gastos.agregarGasto("Café", "abc");

  await expect(gastos.error).toHaveText("Monto inválido");
  await expect(gastos.items).toHaveCount(0);
});
```

`pnpm exec playwright test` queda **verde y determinista** (sin sleeps, sin retries necesarios). El mensaje de éxito y el error se afirman con assertions que reintentan solas.

## Razonamiento paso a paso
- La latencia del mensaje de éxito es justo el detalle que rompe a `textContent()` y obliga al sleep en la versión frágil. `toHaveText`/`toBeVisible` lo resuelven porque **observan y reintentan** hasta el default de timeout (~5 s), siguiendo apenas la condición se cumple.
- El error de validación es **síncrono** (se setea en el mismo `click`), así que `toHaveText("Monto inválido")` pasa de inmediato; igual conviene la web-first assertion por consistencia.
- El Page Object deja las **interacciones** (`agregarGasto`) encapsuladas y las **aserciones** en el test. Si mañana el label "Descripción" cambia a "Detalle", se edita **un** lugar.

## Puntos resbalosos (donde el corrector debe mirar)
1. **`getByText("Gasto agregado")` vs `toHaveText("Gasto agregado: Almuerzo")`.** Está bien usar el substring para *localizar* y el texto completo para *afirmar*. Cualquiera de las dos formas (substring en `toContainText`, o texto completo en `toHaveText`) es válida.
2. **El error con `role="alert"` existe vacío en el DOM.** `getByRole("alert")` lo encuentra siempre; lo que cambia es su texto. Un alumno que use `toBeVisible()` sobre un `<div>` vacío puede tener resultados raros: lo correcto aquí es `toHaveText("Monto inválido")` (o `getByText("Monto inválido")` + `toBeVisible`).
3. **Determinismo.** El ejercicio exige `retries: 0` en la config provista. Si el alumno "estabiliza" subiendo `retries`, no cumplió: el test debe ser verde sin reintentos.
4. **No tocar `app.html`.** Si el alumno modificó el SUT (p. ej. para quitar la latencia), invalida el ejercicio; la gracia es manejar la latencia desde el test.

## Rango de soluciones aceptables
- `getByLabel`, `getByRole`, `getByText`, `getByTestId` (este último justificado) son todos válidos según el caso. No exigir una forma única.
- El método del Page Object puede llamarse distinto (`agregar`, `registrarGasto`); lo que importa es que encapsule la interacción y no contenga aserciones.
- Aserciones extra (total con `getByText("Total: $5000")`) son bienvenidas, no obligatorias.
- Si el alumno prefirió usar `baseURL` + un `goto` relativo en vez del helper `pathToFileURL`, es válido siempre que el test corra verde.
- Tres tests (válido, inválido, y p. ej. descripción vacía) está sobre lo pedido y es excelente; dos (válido + inválido) cumple.
