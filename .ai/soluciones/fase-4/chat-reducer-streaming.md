---
ejercicio_id: fase-4/chat-reducer-streaming
fase: fase-4
sub_unidad: "4.11"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — chatReducer: la máquina de estados de un chat de IA

## Respuesta canónica

```ts
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

export function chatReducer(state: ChatState, accion: Accion): ChatState {
  switch (accion.tipo) {
    case "ENVIAR":
      return {
        ...state,
        estado: "enviando",
        error: null,
        mensajes: [
          ...state.mensajes,
          { id: accion.idUsuario, rol: "user", texto: accion.texto },
          { id: accion.idAsistente, rol: "assistant", texto: "" },
        ],
      };

    case "CHUNK": {
      if (state.mensajes.length === 0) return state;
      const ultimo = state.mensajes[state.mensajes.length - 1];
      if (ultimo.rol !== "assistant") return state;
      const actualizado: Mensaje = { ...ultimo, texto: ultimo.texto + accion.delta };
      return {
        ...state,
        estado: "streaming",
        mensajes: [...state.mensajes.slice(0, -1), actualizado],
      };
    }

    case "COMPLETAR":
      return { ...state, estado: "idle" };

    case "ERROR":
      return { ...state, estado: "error", error: accion.mensaje };

    case "CANCELAR":
      return { ...state, estado: "idle" };

    default:
      return state;
  }
}
```

## Razonamiento paso a paso
- **`ENVIAR` (optimistic UI):** empuja **dos** mensajes. El del usuario lleva su texto y se ve al instante (no espera al servidor). El de asistente nace **vacío** porque es el *contenedor* que `CHUNK` va a rellenar token a token. Limpia `error` para que un fallo anterior no quede pegado en la nueva vuelta. Pasa a `"enviando"` (mandé, todavía no llega nada → "pensando" en la UI).
- **`CHUNK` (acumulación inmutable):** dos guards primero (array vacío; último no es del asistente) para no corromper el estado. Luego toma el último mensaje, crea una **copia** con el texto concatenado (`{ ...ultimo, texto: ... }`) y reconstruye el array con `.slice(0, -1)` + la copia. Pasa a `"streaming"`. Mutar `ultimo.texto += ...` rompería la detección de cambios de React (lección 4.5) y haría fallar el test de inmutabilidad.
- **`COMPLETAR` / `CANCELAR`:** vuelven a `"idle"`. `CANCELAR` no toca `mensajes`, así que el texto parcial queda congelado y visible.
- **`ERROR`:** pasa a `"error"` y guarda el mensaje. **No toca `mensajes`** — el parcial que el usuario estaba leyendo se conserva, con el aviso al lado (mejor UX que borrarlo).

## Por qué los tests pasan (y qué NO prueban)
- **ENVIAR:** la caché de `mensajes` queda con dos entradas; el test compara la forma exacta.
- **CHUNK x2:** `"" + "Bue" + "nas" = "Buenas"`; el del usuario queda intacto.
- **ERROR:** el `texto` parcial sobrevive porque el caso no toca `mensajes`.
- **Inmutabilidad:** el test clona el estado previo con `structuredClone` y verifica que el reducer no lo mutó; solo pasa si copias en lugar de mutar.
- Los tests **no** distinguen entre `at(-1)` y `mensajes[length-1]`, ni exigen tipar el `actualizado`. El corrector revisa esos detalles de calidad en el `.ts` (C2/C4).

## Puntos resbalosos (donde el corrector debe mirar)
1. **Asistente nace con texto del usuario:** copiar `texto` a ambos mensajes. El test de ENVIAR lo atrapa (espera `texto: ""` en el de asistente). Márcalo en C1.
2. **Mutación en sitio:** `ultimo.texto += accion.delta`. Puede pasar los tests de CHUNK por casualidad, pero **falla** el de inmutabilidad. C2.
3. **Falta de guards en CHUNK:** sin el `if (length === 0)` revienta con un `CHUNK` antes de `ENVIAR` (lo cubre un test). C2.
4. **`ERROR` que borra el parcial** (`mensajes: []` o recorta el asistente): el test de ERROR verifica que el parcial sobreviva. C3.
5. **Olvidar `error: null` en `ENVIAR`:** no lo atrapa un test directo, pero es un bug real (error viejo pegado). Obsérvalo en el código.

## Rango de soluciones aceptables
- `state.mensajes[state.mensajes.length - 1]` o `state.mensajes.at(-1)`: equivalentes (con `at(-1)` conviene un guard de `undefined`).
- Tipar `actualizado` como `Mensaje` o dejar que se infiera: ambos válidos; tiparlo suma en C2-excelente.
- Manejar `CHUNK` sobre un último mensaje que no es del asistente devolviendo `state` (recomendado) o lanzando: el contrato pide devolver sin cambios; lanzar es defendible si lo justifica, pero menos robusto.
- Unificar `COMPLETAR`/`CANCELAR` en una rama o separarlas: ambas válidas mientras dejen `idle` sin tocar `mensajes`.
