/**
 * Tests del ejercicio 4.2 — Tarjeta responsive con utility-first (Vitest).
 *
 * Estos tests NO miden estética: miden el MÉTODO. Verifican que tu tarjeta usa
 * Tailwind como se debe —utilidades + escala + variantes responsive/estado/dark—
 * y que NO caíste en estilos inline ni en @apply.
 *
 * El test solo evalúa lo que escribes ENTRE los comentarios marcadores
 * "TU TARJETA: empieza" y "TU TARJETA: termina". No borres esos marcadores.
 *
 * Ejecuta:   pnpm test     (o:  pnpm dlx vitest run)
 */

import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const html = readFileSync(
  fileURLToPath(new URL("./tarjeta.html", import.meta.url)),
  "utf8",
);

// Aislamos la región del alumno (entre los marcadores) y quitamos los
// comentarios HTML: los comentarios no son marcado renderizado, así que un
// `<!-- ... style=... @apply ... -->` no debe contar como infracción.
const region = html.match(/TU TARJETA: empieza([\s\S]*?)TU TARJETA: termina/);
const card = (region ? region[1] : "").replace(/<!--[\s\S]*?-->/g, "");

// Junta el contenido de todos los atributos class="..." (o '...') de tu tarjeta.
const clases = [...card.matchAll(/class\s*=\s*["']([^"']*)["']/g)]
  .map((m) => m[1])
  .join(" ");

describe("estructura mínima", () => {
  it("conservaste los comentarios marcadores", () => {
    expect(
      region,
      "No encontré los marcadores 'TU TARJETA: empieza/termina'. No los borres: el test los usa.",
    ).not.toBeNull();
  });

  it("escribiste tu propia tarjeta (no quedó el placeholder)", () => {
    expect(
      card.includes("Reemplázame"),
      "Todavía está el placeholder 'Reemplázame'. Construye tu tarjeta.",
    ).toBe(false);
    expect(
      clases.length,
      "No encontré clases de utilidad en tu tarjeta. Estila con clases de Tailwind.",
    ).toBeGreaterThan(0);
  });
});

describe("utility-first (cero CSS propio)", () => {
  it("no usa estilos inline (style=...)", () => {
    expect(
      /\sstyle\s*=\s*["']/.test(card),
      "Encontré un atributo style inline. Usa utilidades, no CSS inline.",
    ).toBe(false);
  });

  it("no usa @apply", () => {
    expect(
      card.includes("@apply"),
      "Encontré @apply. En este ejercicio el aspecto sale solo de utilidades.",
    ).toBe(false);
  });
});

describe("layout y escala", () => {
  it("usa flexbox o grid", () => {
    expect(
      /(^|\s)(flex|grid|inline-flex|inline-grid)(\s|$)/.test(clases),
      "Usa 'flex' o 'grid' para el layout de la tarjeta.",
    ).toBe(true);
  });

  it("usa la escala de espaciado (gap/padding/margin), no números mágicos", () => {
    expect(
      /(^|\s)(gap-\d|p[xytrbl]?-\d|m[xytrbl]?-\d|space-[xy]-\d)/.test(clases),
      "Usa la escala de espaciado de Tailwind: gap-*, p-*, m-* ...",
    ).toBe(true);
  });
});

describe("variantes", () => {
  it("es responsive (al menos un prefijo sm:/md:/lg:/xl:)", () => {
    expect(
      /(^|\s)(sm|md|lg|xl|2xl):/.test(clases),
      "Añade al menos una utilidad con prefijo responsive (p. ej. md:flex-row).",
    ).toBe(true);
  });

  it("tiene un estado hover:", () => {
    expect(
      /(^|\s)hover:/.test(clases),
      "El botón (o la tarjeta) debe reaccionar con hover: (p. ej. hover:bg-indigo-700).",
    ).toBe(true);
  });

  it("soporta dark mode (al menos una utilidad dark:)", () => {
    expect(
      /(^|\s)dark:/.test(clases),
      "Añade variantes dark: para que el fondo y el texto se adapten al tema oscuro.",
    ).toBe(true);
  });
});
