// Ejercicio 2.10 — Page Object (ESQUELETO). Complétalo.
//
// Un Page Object encapsula DÓNDE están las cosas (locators) y CÓMO se interactúa
// (métodos). El test usará esta clase y NO contendrá selectores crudos.
//
// La aserción se queda en el TEST (es el corazón de la prueba); las interacciones
// (llenar campos, hacer clic) viven AQUÍ.

import { type Page, type Locator } from "@playwright/test";
import { pathToFileURL } from "node:url";
import path from "node:path";

const APP_URL = pathToFileURL(path.join(__dirname, "app.html")).href;

export class GastosPage {
  readonly page: Page;
  // TODO: declara los locators que vas a necesitar, por ejemplo:
  //   readonly descripcion: Locator;
  //   readonly monto: Locator;
  //   readonly agregar: Locator;
  //   readonly mensajeExito: Locator;
  //   readonly error: Locator;
  //   readonly items: Locator;

  constructor(page: Page) {
    this.page = page;
    // TODO: inicializa los locators con getByLabel / getByRole / getByText.
    //   Pista: el botón es getByRole("button", { name: "Agregar" });
    //          los campos, getByLabel("Descripción") y getByLabel("Monto");
    //          el error, getByRole("alert").
  }

  async goto() {
    await this.page.goto(APP_URL);
  }

  // TODO: método agregar(descripcion: string, monto: string) que rellena los
  // campos y hace clic en "Agregar". No pongas aserciones aquí.
}
