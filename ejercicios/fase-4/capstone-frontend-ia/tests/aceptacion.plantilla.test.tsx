/**
 * Plantilla de tests de aceptación para el capstone (Vitest + Testing Library).
 *
 * NO es una solución: es un molde con los PATRONES que tu frontend debe cumplir. Cada test usa `it.skip`
 * con TODOs para que lo adaptes a TUS componentes. Quita el skip cuando lo cablees a tu app. Mídete por lo
 * que los tests DETECTAN, no por coverage%.
 *
 * Requiere (devDependencies): vitest, jsdom, @testing-library/react, @testing-library/jest-dom,
 * @testing-library/user-event, jest-axe. Configura el entorno jsdom y los matchers en tu setup de Vitest.
 */
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
// import userEvent from "@testing-library/user-event";
// import { axe } from "jest-axe";

// TODO: importa tus componentes reales.
// import { ColeccionesList } from "../src/components/ColeccionesList";
// import { MensajeAsistente } from "../src/components/MensajeAsistente";

describe("Estados de primera clase — lista de colecciones (GATE 4.10)", () => {
  it.skip("loading: muestra un skeleton, no una lista vacía ni un spinner mudo", async () => {
    // TODO: renderiza la lista forzando isPending (mockea el queryFn o el cliente de TanStack Query).
    // render(<ColeccionesList />, { wrapper: ProveedorDeTest });
    // expect(screen.getByTestId("skeleton-colecciones")).toBeInTheDocument();
  });

  it.skip("error: muestra un mensaje accionable (leído del detail RFC 9457) y un botón Reintentar", async () => {
    // TODO: fuerza isError con un error que traiga { detail: "..." }.
    // expect(screen.getByRole("alert")).toHaveTextContent(/.../);
    // expect(screen.getByRole("button", { name: /reintentar/i })).toBeInTheDocument();
  });

  it.skip("vacío: cuando data.length === 0, invita a crear la primera colección (call-to-action)", async () => {
    // TODO: fuerza data = [].
    // expect(screen.getByRole("button", { name: /crear.*colecci/i })).toBeInTheDocument();
  });

  it.skip("success: con datos, renderiza un item por colección", async () => {
    // TODO: fuerza data con 2 colecciones.
    // expect(screen.getAllByRole("listitem")).toHaveLength(2);
  });
});

describe("Seguridad — salida del LLM como texto, no HTML (GATE anti-XSS 4.11)", () => {
  it.skip("un texto del modelo con <script> aparece ESCAPADO, no como nodo ejecutable", () => {
    const malicioso = '<img src=x onerror="alert(1)">hola';
    // TODO: renderiza tu componente que pinta el texto del asistente.
    // render(<MensajeAsistente texto={malicioso} />);
    // El texto debe verse literal; NO debe existir un <img> en el DOM.
    expect(screen.queryByText(malicioso)).toBeTruthy(); // el texto literal está visible
    expect(document.querySelector("img")).toBeNull();   // no se inyectó HTML
  });
});

describe("Accesibilidad — chequeo automatizado (parcial; el resto es manual)", () => {
  it.skip("la vista no tiene violaciones detectables por axe", async () => {
    // TODO: renderiza la vista completa.
    // const { container } = render(<Pagina />, { wrapper: ProveedorDeTest });
    // const resultados = await axe(container);
    // expect(resultados).toHaveNoViolations();
    // NOTA: axe NO valida foco de teclado ni orden de lectura. Haz además la pasada manual con el teclado.
  });

  it.skip("el modal de crear colección atrapa el foco y lo devuelve al cerrar", async () => {
    // TODO: abre el modal con el teclado, verifica que el foco entra; ciérralo y verifica que vuelve al disparador.
    // const user = userEvent.setup();
    // ...
  });
});

describe("Máquina de estados del chat (reusa chat-reducer-streaming)", () => {
  it.skip("ENVIAR mete msg de usuario + msg de asistente vacío; CHUNK acumula; ERROR no borra el parcial", () => {
    // TODO: importa tu chatReducer y prueba las transiciones (ver el ejercicio chat-reducer-streaming).
  });
});
