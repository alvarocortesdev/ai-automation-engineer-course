/**
 * Tests del ejercicio 4.10 A — Los cuatro estados de primera clase (Vitest + React Testing Library).
 *
 * Verifican el COMPORTAMIENTO de las cuatro ramas: loading anunciado, error anunciado + reintento,
 * empty distinto y accionable, y success con la lista. NO pueden ver cómo modelaste el estado por
 * dentro (eso lo revisa el corrector con la rúbrica): el espíritu es una máquina de estados.
 *
 * Ejecuta:   pnpm test
 */

import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { BandejaTareas, type Tarea } from "./BandejaTareas";

const TAREAS: Tarea[] = [
  { id: "1", titulo: "Revisar PR" },
  { id: "2", titulo: "Desplegar la API" },
];

/** Una promesa que controlamos a mano (para fijar el estado de carga). */
function diferido<T>() {
  let resolver!: (valor: T) => void;
  let rechazar!: (error: unknown) => void;
  const promesa = new Promise<T>((res, rej) => {
    resolver = res;
    rechazar = rej;
  });
  return { promesa, resolver, rechazar };
}

describe("estado LOADING", () => {
  it("muestra un indicador anunciado (role='status') mientras la carga está pendiente", () => {
    const { promesa } = diferido<Tarea[]>();
    render(<BandejaTareas cargar={() => promesa} />);
    expect(
      screen.getByRole("status"),
      "Mientras carga debe haber un indicador con role='status' (para lectores de pantalla).",
    ).toBeInTheDocument();
    // No hay lista ni error todavía.
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("estado SUCCESS", () => {
  it("muestra la lista cuando la carga resuelve con tareas", async () => {
    render(<BandejaTareas cargar={() => Promise.resolve(TAREAS)} />);
    expect(await screen.findByText("Revisar PR")).toBeInTheDocument();
    expect(screen.getByText("Desplegar la API")).toBeInTheDocument();
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });
});

describe("estado EMPTY", () => {
  it("es distinto del éxito y del error, y es accionable (tiene un CTA)", async () => {
    render(<BandejaTareas cargar={() => Promise.resolve([])} />);
    // Un CTA que invite a crear la primera tarea.
    expect(
      await screen.findByRole("button", { name: /crear|nueva|agregar|empezar|añadir/i }),
      "El estado vacío debe ofrecer una acción (un <button> CTA), no ser una caja en blanco.",
    ).toBeInTheDocument();
    // NO debe haber lista ni alerta de error.
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("estado ERROR", () => {
  it("anuncia el error (role='alert') y ofrece reintentar; al reintentar, carga de nuevo", async () => {
    const cargar = vi
      .fn()
      .mockRejectedValueOnce(new Error("HTTP 500"))
      .mockResolvedValueOnce(TAREAS);

    render(<BandejaTareas cargar={cargar} />);

    // El error se anuncia.
    expect(await screen.findByRole("alert")).toBeInTheDocument();
    // No se muestra una lista vacía haciéndose pasar por "no hay datos".
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);

    // Hay una salida: el botón de reintento.
    const reintentar = screen.getByRole("button", { name: /reintentar|volver a intentar|reintento/i });
    fireEvent.click(reintentar);

    // Tras reintentar (segundo intento exitoso), aparece la lista.
    expect(await screen.findByText("Revisar PR")).toBeInTheDocument();
    expect(cargar).toHaveBeenCalledTimes(2);
  });
});

// 👉 Agrega aquí al menos un test tuyo (caso borde: una sola tarea, títulos repetidos, etc.).
