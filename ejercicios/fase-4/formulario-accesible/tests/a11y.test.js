import { describe, it, expect, beforeAll } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

// El HTML del alumno es la ÚNICA fuente de verdad: el test lo parsea con jsdom
// y audita la accesibilidad MECÁNICA, igual que un linter de a11y en un proyecto
// real. Lo que un linter NO puede juzgar (foco visible, prueba con lector de
// pantalla, calidad del texto alternativo) lo evalúa la rúbrica.

const htmlPath = fileURLToPath(new URL("../formulario.html", import.meta.url));

let doc;
beforeAll(() => {
  const html = readFileSync(htmlPath, "utf8");
  doc = new JSDOM(html).window.document;
});

/** Controles de formulario que requieren un nombre accesible. */
function controles() {
  const sel =
    "input:not([type=hidden]):not([type=submit]):not([type=button]):not([type=reset]):not([type=image])," +
    "select,textarea";
  return [...doc.querySelectorAll(sel)];
}

/**
 * ¿El control tiene NOMBRE ACCESIBLE? Cuenta: <label for>/<label> envolvente,
 * aria-label o aria-labelledby. NO cuenta el placeholder ni el title.
 */
function tieneNombreAccesible(el) {
  const ariaLabel = el.getAttribute("aria-label");
  if (ariaLabel && ariaLabel.trim()) return true;

  const labelledby = el.getAttribute("aria-labelledby");
  if (labelledby) {
    const refOk = labelledby
      .split(/\s+/)
      .filter(Boolean)
      .some((id) => doc.getElementById(id));
    if (refOk) return true;
  }

  const id = el.getAttribute("id");
  if (id) {
    const asociado = [...doc.querySelectorAll("label")].some(
      (l) => l.getAttribute("for") === id,
    );
    if (asociado) return true;
  }

  if (el.closest("label")) return true;

  return false;
}

describe("Accesibilidad del formulario — WCAG 2.2", () => {
  it("tiene un landmark <main> para que el lector de pantalla salte al contenido (SC 1.3.1)", () => {
    expect(doc.querySelector("main, [role='main']")).not.toBeNull();
  });

  it("tiene al menos un encabezado (h1–h6) que titule la región (SC 1.3.1 / 2.4.6)", () => {
    expect(doc.querySelector("h1,h2,h3,h4,h5,h6")).not.toBeNull();
  });

  it("cada campo tiene un nombre accesible — el placeholder NO cuenta (SC 1.3.1, 4.1.2)", () => {
    const sinNombre = controles().filter((el) => !tieneNombreAccesible(el));
    const detalle = sinNombre
      .map((el) => el.outerHTML.replace(/\s+/g, " ").slice(0, 80))
      .join("\n  ");
    expect(
      sinNombre.length,
      `Estos controles no tienen <label> asociado ni aria-label:\n  ${detalle}`,
    ).toBe(0);
  });

  it("no usa tabindex positivo: el orden de foco lo da el DOM (antipatrón)", () => {
    const positivos = [...doc.querySelectorAll("[tabindex]")].filter(
      (el) => Number(el.getAttribute("tabindex")) > 0,
    );
    expect(positivos.length).toBe(0);
  });

  it("la acción 'Aprobar' es un <button> real, no un <div onclick> (SC 2.1.1, 4.1.2)", () => {
    const botones = doc.querySelectorAll(
      "button, input[type='submit'], input[type='button']",
    );
    const falsos = doc.querySelectorAll(
      "div[onclick], span[onclick], a[onclick]:not([href])",
    );
    expect(botones.length).toBeGreaterThanOrEqual(1);
    expect(falsos.length).toBe(0);
  });

  it("cada <img> declara alt (informativo) o alt='' si es decorativa (SC 1.1.1)", () => {
    const sinAlt = [...doc.querySelectorAll("img")].filter(
      (img) => img.getAttribute("alt") === null,
    );
    expect(sinAlt.length).toBe(0);
  });

  it("el error está enlazado por aria-describedby a un elemento con role='alert' (SC 4.1.2, 4.1.3)", () => {
    const alertas = [...doc.querySelectorAll("[role='alert'], [aria-live]")];
    const conId = alertas.filter((el) => el.id);
    expect(
      conId.length,
      "El mensaje de error debe tener role='alert' (o aria-live) y un id.",
    ).toBeGreaterThanOrEqual(1);

    const ids = conId.map((el) => el.id);
    const enlazado = [...doc.querySelectorAll("[aria-describedby]")].some((el) =>
      el
        .getAttribute("aria-describedby")
        .split(/\s+/)
        .some((ref) => ids.includes(ref)),
    );
    expect(
      enlazado,
      "Ningún campo apunta con aria-describedby al id del mensaje de error.",
    ).toBe(true);
  });
});
