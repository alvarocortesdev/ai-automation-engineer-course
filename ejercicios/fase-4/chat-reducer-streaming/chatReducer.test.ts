/**
 * Tests del ejercicio 4.11 A — chatReducer (Vitest, TypeScript puro).
 *
 * Verifican el COMPORTAMIENTO de la máquina de estados:
 *   - ENVIAR    -> optimistic UI (mensaje de usuario YA) + asistente vacío;
 *   - CHUNK     -> acumula en el último mensaje, inmutable;
 *   - COMPLETAR -> idle;
 *   - ERROR     -> error + estado "error", sin perder el parcial;
 *   - CANCELAR  -> idle conservando el parcial.
 *
 * Ejecuta:   pnpm test
 */
import { describe, it, expect } from "vitest";
import {
  chatReducer,
  estadoInicial,
  type ChatState,
} from "./chatReducer";

describe("chatReducer — ENVIAR (optimistic UI)", () => {
  it("añade el mensaje del usuario YA y un mensaje de asistente vacío", () => {
    const s = chatReducer(estadoInicial, {
      tipo: "ENVIAR",
      idUsuario: "u1",
      idAsistente: "a1",
      texto: "Hola",
    });
    expect(s.mensajes).toEqual([
      { id: "u1", rol: "user", texto: "Hola" },
      { id: "a1", rol: "assistant", texto: "" },
    ]);
    expect(s.estado).toBe("enviando");
    expect(s.error).toBeNull();
  });
});

describe("chatReducer — CHUNK (acumulación con streaming)", () => {
  it("concatena el delta en el último mensaje (el del asistente) y pasa a streaming", () => {
    let s = chatReducer(estadoInicial, {
      tipo: "ENVIAR",
      idUsuario: "u1",
      idAsistente: "a1",
      texto: "Hola",
    });
    s = chatReducer(s, { tipo: "CHUNK", delta: "Bue" });
    s = chatReducer(s, { tipo: "CHUNK", delta: "nas" });

    expect(s.estado).toBe("streaming");
    expect(s.mensajes[1]).toEqual({ id: "a1", rol: "assistant", texto: "Buenas" });
    // El mensaje del usuario queda intacto:
    expect(s.mensajes[0]).toEqual({ id: "u1", rol: "user", texto: "Hola" });
  });

  it("devuelve el estado sin cambios si no hay mensajes", () => {
    const s = chatReducer(estadoInicial, { tipo: "CHUNK", delta: "x" });
    expect(s).toEqual(estadoInicial);
  });
});

describe("chatReducer — COMPLETAR", () => {
  it("vuelve a idle", () => {
    let s = chatReducer(estadoInicial, {
      tipo: "ENVIAR",
      idUsuario: "u1",
      idAsistente: "a1",
      texto: "Hola",
    });
    s = chatReducer(s, { tipo: "CHUNK", delta: "Listo" });
    s = chatReducer(s, { tipo: "COMPLETAR" });
    expect(s.estado).toBe("idle");
    expect(s.mensajes[1].texto).toBe("Listo");
  });
});

describe("chatReducer — ERROR (sin perder el parcial)", () => {
  it("pasa a estado error, guarda el mensaje y CONSERVA el texto parcial", () => {
    let s = chatReducer(estadoInicial, {
      tipo: "ENVIAR",
      idUsuario: "u1",
      idAsistente: "a1",
      texto: "Hola",
    });
    s = chatReducer(s, { tipo: "CHUNK", delta: "respuesta a med" });
    s = chatReducer(s, { tipo: "ERROR", mensaje: "Se cortó la red" });

    expect(s.estado).toBe("error");
    expect(s.error).toBe("Se cortó la red");
    expect(s.mensajes[1].texto).toBe("respuesta a med"); // el parcial sigue ahí
  });
});

describe("chatReducer — CANCELAR (conserva el parcial)", () => {
  it("vuelve a idle conservando el texto parcial", () => {
    let s = chatReducer(estadoInicial, {
      tipo: "ENVIAR",
      idUsuario: "u1",
      idAsistente: "a1",
      texto: "Hola",
    });
    s = chatReducer(s, { tipo: "CHUNK", delta: "lo que alcanzó" });
    s = chatReducer(s, { tipo: "CANCELAR" });

    expect(s.estado).toBe("idle");
    expect(s.mensajes[1].texto).toBe("lo que alcanzó");
  });
});

describe("chatReducer — inmutabilidad", () => {
  it("no muta el estado de entrada", () => {
    const previo: ChatState = {
      mensajes: [
        { id: "u1", rol: "user", texto: "Hola" },
        { id: "a1", rol: "assistant", texto: "Bue" },
      ],
      estado: "streaming",
      error: null,
    };
    const copia = structuredClone(previo);
    chatReducer(previo, { tipo: "CHUNK", delta: "nas" });
    expect(previo).toEqual(copia); // el reducer no tocó el objeto original
  });
});

// 👉 Agrega aquí al menos un test tuyo. Idea: enviar dos preguntas seguidas
//    (ENVIAR -> CHUNK -> COMPLETAR -> ENVIAR de nuevo) y verificar que el
//    historial acumula los cuatro mensajes en orden.
