/**
 * Tests del ejercicio 4.5 A — Filtro buscable (Vitest + React Testing Library).
 *
 * Verifican el COMPORTAMIENTO del componente: input controlado, placeholder,
 * filtrado case-insensitive y el mensaje "Sin resultados". NO pueden ver si usaste
 * `useEffect` por dentro (eso lo revisa el corrector con la rúbrica): el espíritu del
 * ejercicio es resolverlo con estado derivado, sin efecto.
 *
 * Ejecuta:   pnpm test
 */

import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { FiltroBuscable } from "./FiltroBuscable";

const FRUTAS = ["Manzana", "Banana", "Naranja", "Mandarina", "Pera"];

function escribir(input: HTMLElement, texto: string) {
  fireEvent.change(input, { target: { value: texto } });
}

describe("estructura básica", () => {
  it("renderiza un input de texto", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    expect(
      screen.getByRole("textbox"),
      "No encontré un input de texto. El componente debe renderizar un <input>.",
    ).toBeInTheDocument();
  });

  it("reenvía el placeholder de la prop al input", () => {
    render(<FiltroBuscable items={FRUTAS} placeholder="Buscar fruta" />);
    expect(screen.getByRole("textbox")).toHaveAttribute("placeholder", "Buscar fruta");
  });

  it("con la consulta vacía muestra todos los items", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    expect(screen.getAllByRole("listitem")).toHaveLength(FRUTAS.length);
  });
});

describe("filtrado", () => {
  it("filtra por substring sin distinguir mayúsculas", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    escribir(screen.getByRole("textbox"), "man"); // minúsculas contra items capitalizados
    const visibles = screen.getAllByRole("listitem").map((li) => li.textContent);
    expect(visibles).toEqual(["Manzana", "Mandarina"]);
  });

  it("muestra 'Sin resultados' cuando nada coincide (y ningún <li>)", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    escribir(screen.getByRole("textbox"), "zzz");
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.getByText("Sin resultados")).toBeInTheDocument();
  });

  it("vuelve a mostrar todo al limpiar la consulta", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    const input = screen.getByRole("textbox");
    escribir(input, "man");
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    escribir(input, "");
    expect(screen.getAllByRole("listitem")).toHaveLength(FRUTAS.length);
  });
});

describe("input controlado", () => {
  it("el valor escrito se refleja en el input (value viene del estado)", () => {
    render(<FiltroBuscable items={FRUTAS} />);
    const input = screen.getByRole("textbox") as HTMLInputElement;
    escribir(input, "nar");
    expect(input.value).toBe("nar");
  });
});

// 👉 Agrega aquí al menos un test tuyo (caso borde: acentos, espacios, items=[] ...).
