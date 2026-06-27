# Componente a diagnosticar — `ChatIA` (con defectos)

Este es un componente de chat de IA que "funciona" en una demo feliz pero falla en
casi todo lo que importa en una app real. Tu trabajo (en `diseno-chat.md`) es
diagnosticarlo: nombrar cada defecto y decir qué patrón de la lección lo arregla.
**No lo arregles en código** — es un ejercicio de razonamiento.

```tsx
"use client";
import { useState } from "react";

export function ChatIA() {
  const [historial, setHistorial] = useState<string[]>([]);
  const [input, setInput] = useState("");

  async function enviar() {
    // 1) Se manda el texto y se espera la respuesta COMPLETA del modelo.
    const res = await fetch("/api/chat", {
      method: "POST",
      body: JSON.stringify({ texto: input }),
    });
    const data = await res.json(); // se queda aquí varios segundos
    // 2) Recién ahora se agrega algo al historial: la respuesta del modelo.
    //    El mensaje que escribió el usuario nunca se muestra como tal.
    setHistorial((h) => [...h, data.html]);
    setInput("");
  }

  return (
    <div>
      {historial.map((item, i) => (
        // 3) Se renderiza la salida del modelo como HTML crudo.
        <div key={i} dangerouslySetInnerHTML={{ __html: item }} />
      ))}

      {/* 4) No hay indicador de "pensando", ni de "escribiendo",
             ni botón para detener, ni manejo de error, ni estado vacío. */}
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={enviar}>Enviar</button>
    </div>
  );
}
```

## Notas del comportamiento observado

- Al apretar "Enviar", la pantalla se queda igual unos 4 segundos y de golpe
  aparece un bloque de texto. El usuario no sabe si la app está pensando o se colgó.
- El mensaje que el propio usuario escribió no se ve en ninguna parte.
- Si la red falla, no pasa nada visible: el botón queda "muerto".
- No hay forma de cancelar una respuesta larga a mitad de camino.
- Un compañero de seguridad marcó el componente como "riesgo de XSS" en la revisión.
- Un lector de pantalla no anuncia la respuesta cuando llega.
