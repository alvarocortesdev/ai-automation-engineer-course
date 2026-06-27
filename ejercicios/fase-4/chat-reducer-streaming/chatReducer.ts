/**
 * Ejercicio 4.11 A — chatReducer: la máquina de estados de un chat de IA.
 *
 * Implementa el reducer PURO `chatReducer`. Respeta las firmas y tipos exportados:
 * los tests importan exactamente `chatReducer`, `estadoInicial` y los tipos
 * `ChatState`, `Accion`, `Mensaje`.
 *
 * Esto es, en esencia, lo que `useChat` del Vercel AI SDK hace por dentro
 * (sección 4.5 de la lección). Reglas del contrato:
 *
 *   ENVIAR    -> añade DOS mensajes: el del usuario (con su texto) y uno de
 *                asistente VACÍO (texto: ""). Pasa a "enviando", limpia error.
 *   CHUNK     -> concatena `delta` al ÚLTIMO mensaje (el del asistente) de forma
 *                INMUTABLE (copia array y objeto). Pasa a "streaming".
 *                Si no hay mensajes o el último no es del asistente: devuelve el
 *                estado SIN cambios.
 *   COMPLETAR -> vuelve a "idle".
 *   ERROR     -> pasa a "error" y guarda el mensaje en `error`. NO borres el
 *                texto parcial del asistente.
 *   CANCELAR  -> vuelve a "idle" CONSERVANDO el texto parcial.
 *
 * NO mutes el `state` de entrada (inmutabilidad): copia, no muta.
 */

export type Rol = "user" | "assistant";

export interface Mensaje {
  id: string;
  rol: Rol;
  texto: string;
}

export type Estado = "idle" | "enviando" | "streaming" | "error";

export interface ChatState {
  mensajes: Mensaje[];
  estado: Estado;
  error: string | null;
}

export type Accion =
  | { tipo: "ENVIAR"; idUsuario: string; idAsistente: string; texto: string }
  | { tipo: "CHUNK"; delta: string }
  | { tipo: "COMPLETAR" }
  | { tipo: "ERROR"; mensaje: string }
  | { tipo: "CANCELAR" };

export const estadoInicial: ChatState = {
  mensajes: [],
  estado: "idle",
  error: null,
};

export function chatReducer(_state: ChatState, _accion: Accion): ChatState {
  // TODO: implementa el reducer a mano, sin IA (ver contrato arriba y la
  // sección 4.5 de la lección). Recuerda: PURO e INMUTABLE.
  throw new Error("No implementado: implementa chatReducer a mano, sin IA.");
}
