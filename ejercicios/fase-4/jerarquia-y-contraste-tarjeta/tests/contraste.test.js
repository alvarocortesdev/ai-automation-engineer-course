import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

// El CSS del alumno es la ÚNICA fuente de verdad de la paleta: el test lo lee y
// extrae los tokens de color, igual que harías al auditar contraste en un proyecto real.
const cssPath = fileURLToPath(new URL("../estilos.css", import.meta.url));
const css = readFileSync(cssPath, "utf8");

/** Extrae el valor hex de una custom property `--nombre` declarada en el CSS. */
function leerToken(nombre) {
  const re = new RegExp(`--${nombre}\\s*:\\s*(#[0-9a-fA-F]{3,8})`);
  const m = css.match(re);
  if (!m) {
    throw new Error(
      `No encontré el token --${nombre} con un valor hex en estilos.css. ` +
        `Decláralo en :root, por ejemplo:  --${nombre}: #1a1a1a;`,
    );
  }
  return m[1];
}

/** #rgb | #rrggbb | #rrggbbaa -> {r,g,b} en 0..255 (ignora el canal alpha). */
function hexARgb(hex) {
  let h = hex.replace("#", "");
  if (h.length === 3) {
    h = h
      .split("")
      .map((c) => c + c)
      .join("");
  }
  return {
    r: parseInt(h.slice(0, 2), 16),
    g: parseInt(h.slice(2, 4), 16),
    b: parseInt(h.slice(4, 6), 16),
  };
}

/** Luminancia relativa según WCAG 2.x (linealización sRGB). */
function luminancia({ r, g, b }) {
  const [lr, lg, lb] = [r, g, b].map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb;
}

/** Razón de contraste WCAG entre dos colores hex. Devuelve un número >= 1. */
function contraste(hexA, hexB) {
  const la = luminancia(hexARgb(hexA));
  const lb = luminancia(hexARgb(hexB));
  const claro = Math.max(la, lb);
  const oscuro = Math.min(la, lb);
  return (claro + 0.05) / (oscuro + 0.05);
}

describe("Paleta de la tarjeta — contraste WCAG 2.2 AA", () => {
  const fondo = leerToken("color-fondo");
  const texto = leerToken("color-texto");
  const tenue = leerToken("color-texto-tenue");
  const acento = leerToken("color-acento");
  const sobreAcento = leerToken("color-texto-sobre-acento");

  it("el texto de cuerpo sobre el fondo cumple 4.5:1 (SC 1.4.3 texto normal)", () => {
    expect(contraste(texto, fondo)).toBeGreaterThanOrEqual(4.5);
  });

  it("el texto tenue (metadata) sobre el fondo cumple 4.5:1 — 'tenue' no exime de AA", () => {
    expect(contraste(tenue, fondo)).toBeGreaterThanOrEqual(4.5);
  });

  it("el texto sobre el acento (label del botón) cumple 4.5:1", () => {
    expect(contraste(sobreAcento, acento)).toBeGreaterThanOrEqual(4.5);
  });

  it("el acento se distingue del fondo como componente de UI (3:1, SC 1.4.11)", () => {
    expect(contraste(acento, fondo)).toBeGreaterThanOrEqual(3);
  });
});
