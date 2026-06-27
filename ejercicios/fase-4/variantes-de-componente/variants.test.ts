/**
 * Tests del ejercicio 4.9 A — Motor de variantes (mini-cva) con Vitest.
 *
 * Verifican el COMPORTAMIENTO: base siempre presente y primero, defaults
 * aplicados, override por props, orden de ejes, fallback ante opción
 * inexistente/undefined, y limpieza de espacios. Lo que los tests NO miden
 * (que sepas explicar qué añade el cva real) lo revisa el corrector.
 *
 * Ejecuta:   pnpm test
 */

import { describe, it, expect } from "vitest";
import { variants } from "./variants";

// Un "componente" de prueba con dos ejes y defaults.
const button = variants({
  base: "btn",
  variants: {
    variant: { default: "bg-primary", outline: "border", ghost: "" },
    size: { sm: "h-9", default: "h-10", lg: "h-11" },
  },
  defaultVariants: { variant: "default", size: "default" },
});

describe("base y defaults", () => {
  it("sin props aplica los defaults, con la base primero", () => {
    expect(button()).toBe("btn bg-primary h-10");
  });

  it("la base siempre va primero", () => {
    expect(button({ size: "lg" }).startsWith("btn ")).toBe(true);
  });
});

describe("override por props", () => {
  it("cambia un solo eje", () => {
    expect(button({ size: "lg" })).toBe("btn bg-primary h-11");
  });

  it("cambia ambos ejes y respeta el orden de declaración (variant antes que size)", () => {
    expect(button({ variant: "outline", size: "sm" })).toBe("btn border h-9");
  });
});

describe("fallback robusto", () => {
  it("una opción inexistente cae al default del eje (no rompe, no añade undefined)", () => {
    expect(button({ size: "xl" })).toBe("btn bg-primary h-10");
  });

  it("undefined cae al default del eje", () => {
    expect(button({ variant: undefined })).toBe("btn bg-primary h-10");
  });
});

describe("limpieza de espacios", () => {
  it("una opción con clases vacías no deja espacios dobles", () => {
    expect(button({ variant: "ghost" })).toBe("btn h-10");
    expect(button({ variant: "ghost" })).not.toMatch(/\s{2,}/);
  });

  it("nunca deja espacio al inicio o al final", () => {
    const r = button({ variant: "outline" });
    expect(r).toBe(r.trim());
  });
});

describe("configuraciones mínimas", () => {
  it("funciona sin base (solo clases de variante)", () => {
    const badge = variants({
      variants: { tono: { a: "x", b: "y" } },
      defaultVariants: { tono: "a" },
    });
    expect(badge()).toBe("x");
    expect(badge({ tono: "b" })).toBe("y");
  });

  it("un eje sin default no aporta nada si la prop no se pasa", () => {
    const c = variants({ base: "c", variants: { extra: { on: "is-on" } } });
    expect(c()).toBe("c");
    expect(c({ extra: "on" })).toBe("c is-on");
  });
});

// 👉 Agrega aquí al menos un test tuyo (caso borde: tres ejes, default que
//    apunta a una opción inexistente, props con clave que no es un eje, ...).
