// Ejercicio 2.10 — VERSIÓN FRÁGIL de partida. TU TRABAJO ES REESCRIBIRLA.
//
// Este test "pasa hoy", pero es frágil, lento y flaky. Tiene tres antipatrones que
// debes eliminar (los diagnosticas primero en diagnostico.md):
//   1) Selectores acoplados a la implementación (#id, .clase CSS).
//   2) waitForTimeout (un sleep): frágil si es muy corto, lento si es muy largo.
//   3) textContent() + expect manual: toma una foto inmediata en vez de auto-esperar.
//
// Además: solo cubre el camino feliz. Debes agregar el camino de validación
// (monto inválido -> aparece un error con role="alert").
//
// Reescribe ESTE archivo usando:
//   - getByLabel / getByRole / getByText (selectores user-facing),
//   - web-first assertions (await expect(locator).toBeVisible() / toHaveText() / toHaveCount()),
//   - un Page Object (gastos.page.ts) para sacar los selectores del test.
//
// NO modifiques app.html.

import { test, expect } from "@playwright/test";
import { pathToFileURL } from "node:url";
import path from "node:path";

const APP_URL = pathToFileURL(path.join(__dirname, "app.html")).href;

test("agregar gasto", async ({ page }) => {
  await page.goto(APP_URL);
  await page.locator("#desc").fill("Almuerzo");
  await page.locator("#monto").fill("5000");
  await page.locator(".btn-add").click();
  await page.waitForTimeout(1000); // "espero a que aparezca el mensaje"
  const t = await page.locator(".toast").textContent();
  expect(t).toContain("Gasto agregado");
});
