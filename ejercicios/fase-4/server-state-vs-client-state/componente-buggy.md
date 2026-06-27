# Componente a diagnosticar — `PanelTareas`

> Este componente "funciona" en la demo del tutorial. Tu trabajo es ver **por qué no
> sobrevive a producción** y diseñar su reemplazo. No lo ejecutes: analízalo leyendo.

```tsx
import { useEffect, useState } from "react";

interface Tarea {
  id: string;
  titulo: string;
  hecha: boolean;
}

function PanelTareas({ usuarioId }: { usuarioId: string }) {
  // --- datos de la lista ---
  const [tareas, setTareas] = useState<Tarea[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // --- estado del formulario de "nueva tarea" ---
  const [titulo, setTitulo] = useState("");
  const [prioridad, setPrioridad] = useState<"baja" | "media" | "alta">("media");
  const [errorTitulo, setErrorTitulo] = useState<string | null>(null);

  // --- estado de la UI ---
  const [filaExpandida, setFilaExpandida] = useState<string | null>(null);
  const [modalAbierto, setModalAbierto] = useState(false);

  // Trae las tareas del usuario.
  useEffect(() => {
    setCargando(true);
    fetch(`/api/tareas?usuario=${usuarioId}`)
      .then((r) => r.json())
      .then((data) => setTareas(data))
      .catch((e) => setError(String(e)))
      .finally(() => setCargando(false));
  }, [usuarioId]);

  // Crea una tarea y la agrega a la lista local.
  async function crear() {
    if (titulo.trim() === "") {
      setErrorTitulo("El título es obligatorio");
      return;
    }
    const res = await fetch("/api/tareas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ titulo, prioridad, usuarioId }),
    });
    const nueva = await res.json();
    setTareas([...tareas, nueva]); // ¿y si el servidor calculó algún campo?
    setTitulo("");
  }

  // Marca/desmarca una tarea.
  async function toggle(id: string) {
    await fetch(`/api/tareas/${id}/toggle`, { method: "PATCH" });
    setTareas(tareas.map((t) => (t.id === id ? { ...t, hecha: !t.hecha } : t)));
  }

  if (cargando) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;
  // ...render de la lista, el formulario y el modal...
  return null;
}
```

## Síntomas observados en producción (pistas para tu diagnóstico)

- Al volver a la pestaña tras un rato, la lista muestra tareas que otro dispositivo ya completó (datos viejos).
- Si la red parpadea durante la carga inicial, el panel queda en "Error" para siempre.
- Otra pantalla de la app también muestra el conteo de tareas, pero no se entera cuando aquí se crea una.
- Al cambiar de usuario muy rápido, a veces aparece la lista del usuario anterior.
- Marcar una tarea "se siente con lag": tarda en reflejarse.
