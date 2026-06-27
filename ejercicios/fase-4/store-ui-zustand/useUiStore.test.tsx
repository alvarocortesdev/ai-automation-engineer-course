/**
 * Tests del ejercicio 4.8 A — Store de UI con Zustand (Vitest + Testing Library).
 *
 * Verifican el COMPORTAMIENTO del store: actions inmutables, lectura con selector
 * atómico desde un componente, y que `persist` con `partialize` guarde SOLO lo que
 * debe durar. Lo que los tests NO pueden ver (si usaste un selector que devuelve un
 * objeto nuevo, o si destructuras el store entero) lo revisa el corrector con la
 * rúbrica. El espíritu del ejercicio es resolverlo con persist + selectores atómicos.
 *
 * Ejecuta:   pnpm test
 */

import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { useUiStore } from "./useUiStore";

// Cada test arranca desde un estado limpio y un storage vacío.
beforeEach(() => {
  localStorage.clear();
  useUiStore.setState({
    modeloActivo: "claude-haiku",
    modelosFavoritos: [],
    tema: "claro",
  });
});

describe("estado inicial y actions", () => {
  it("tiene el estado inicial esperado", () => {
    const s = useUiStore.getState();
    expect(s.modeloActivo).toBe("claude-haiku");
    expect(s.modelosFavoritos).toEqual([]);
    expect(s.tema).toBe("claro");
  });

  it("setModelo cambia el modelo activo", () => {
    useUiStore.getState().setModelo("gpt-4o-mini");
    expect(useUiStore.getState().modeloActivo).toBe("gpt-4o-mini");
  });

  it("alternarTema alterna claro <-> oscuro", () => {
    useUiStore.getState().alternarTema();
    expect(useUiStore.getState().tema).toBe("oscuro");
    useUiStore.getState().alternarTema();
    expect(useUiStore.getState().tema).toBe("claro");
  });

  it("alternarFavorito agrega si no está y quita si está (toggle)", () => {
    useUiStore.getState().alternarFavorito("claude-opus");
    expect(useUiStore.getState().modelosFavoritos).toContain("claude-opus");
    useUiStore.getState().alternarFavorito("claude-opus");
    expect(useUiStore.getState().modelosFavoritos).not.toContain("claude-opus");
  });

  it("alternarFavorito NO muta: crea un arreglo nuevo", () => {
    const antes = useUiStore.getState().modelosFavoritos;
    useUiStore.getState().alternarFavorito("gpt-4o-mini");
    const despues = useUiStore.getState().modelosFavoritos;
    expect(despues).toContain("gpt-4o-mini");
    expect(
      despues,
      "modelosFavoritos debe ser un arreglo NUEVO (inmutabilidad), no el mismo mutado con push",
    ).not.toBe(antes);
  });
});

describe("lectura con selector atómico desde un componente", () => {
  function VistaModelo() {
    const modelo = useUiStore((s) => s.modeloActivo);
    const setModelo = useUiStore((s) => s.setModelo);
    return (
      <div>
        <p>Modelo: {modelo}</p>
        <button onClick={() => setModelo("gpt-4o-mini")}>Cambiar</button>
      </div>
    );
  }

  it("el componente refleja el modelo y se re-renderiza al cambiarlo", () => {
    render(<VistaModelo />);
    expect(screen.getByText("Modelo: claude-haiku")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Cambiar" }));
    expect(screen.getByText("Modelo: gpt-4o-mini")).toBeInTheDocument();
  });
});

describe("persist + partialize", () => {
  it("persiste SOLO tema y modelosFavoritos, no el modelo de sesión", () => {
    useUiStore.getState().setModelo("gpt-4o-mini");
    useUiStore.getState().alternarFavorito("claude-opus");
    useUiStore.getState().alternarTema();

    const crudo = localStorage.getItem("ui-chat-storage");
    expect(
      crudo,
      "persist no escribió en localStorage bajo la clave 'ui-chat-storage' (¿envolviste el store en persist?)",
    ).not.toBeNull();

    const guardado = JSON.parse(crudo as string).state;
    expect(guardado.tema).toBe("oscuro");
    expect(guardado.modelosFavoritos).toEqual(["claude-opus"]);
    expect(
      guardado.modeloActivo,
      "modeloActivo NO debe persistirse: partialize debe excluirlo (es estado de sesión)",
    ).toBeUndefined();
  });
});

// 👉 Agrega aquí al menos un test tuyo (caso borde: alternarFavorito dos modelos
//    distintos, vaciar favoritos, persistir tras varias acciones, ...).
