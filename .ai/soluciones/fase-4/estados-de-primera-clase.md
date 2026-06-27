---
ejercicio_id: fase-4/estados-de-primera-clase
fase: fase-4
sub_unidad: "4.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). No hay una única respuesta correcta:
> otro render es igualmente `excelente` si pasa el test, modela los cuatro estados con una máquina de
> estados y mantiene el empty dentro del éxito.

# Solución de referencia — Los cuatro estados de primera clase

## Respuesta canónica (ejemplo de entrega "excelente")

### `BandejaTareas.tsx` (solo la parte que el alumno completa)

```tsx
import { useEffect, useState } from "react";

export interface Tarea {
  id: string;
  titulo: string;
}

export interface BandejaTareasProps {
  cargar: () => Promise<Tarea[]>;
}

type Estado =
  | { fase: "cargando" }
  | { fase: "error"; mensaje: string }
  | { fase: "listo"; tareas: Tarea[] };

export function BandejaTareas({ cargar }: BandejaTareasProps) {
  const [estado, setEstado] = useState<Estado>({ fase: "cargando" });

  function ejecutarCarga() {
    setEstado({ fase: "cargando" });
    cargar()
      .then((tareas) => setEstado({ fase: "listo", tareas }))
      .catch((e: unknown) =>
        setEstado({
          fase: "error",
          mensaje: e instanceof Error ? e.message : "Error desconocido",
        }),
      );
  }

  useEffect(() => {
    ejecutarCarga();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  switch (estado.fase) {
    // 1) LOADING — anunciado a lectores de pantalla.
    case "cargando":
      return <p role="status">Cargando tus tareas…</p>;

    // 2) ERROR — anunciado + salida (reintentar). Mensaje humano, no el detalle crudo del backend.
    case "error":
      return (
        <div role="alert">
          <p>No pudimos cargar tus tareas. Revisa tu conexión e inténtalo otra vez.</p>
          <button type="button" onClick={ejecutarCarga}>
            Reintentar
          </button>
        </div>
      );

    // 3) EMPTY — éxito sin datos: dentro de "listo", accionable.
    case "listo":
      if (estado.tareas.length === 0) {
        return (
          <div>
            <p>Aún no tienes tareas. Empieza creando la primera.</p>
            <button type="button">Crear tarea</button>
          </div>
        );
      }
      // 4) SUCCESS — la lista, con key estable.
      return (
        <ul>
          {estado.tareas.map((t) => (
            <li key={t.id}>{t.titulo}</li>
          ))}
        </ul>
      );
  }
}
```

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **El estado se modela como datos.** La unión `cargando | error | listo` hace imposibles los estados
   imposibles (no existe "cargando y con error a la vez"). Tres booleanos sueltos sí permiten esas
   contradicciones; por eso se prefiere la máquina de estados.
2. **El empty NO es una fase de la carga.** La petición salió bien (`fase: "listo"`); el vacío es
   `tareas.length === 0`. Se chequea **dentro** del éxito, antes de renderizar la lista. Es exactamente lo
   que TanStack Query (4.7) deja en tus manos: `status === "success"` con `data.length === 0`.
3. **Cada estado tiene una salida.** Error → reintentar (vuelve a `cargando` y reintenta). Vacío → CTA para
   avanzar. Nunca un callejón sin salida (heurística 3 de Nielsen: control y libertad).
4. **Accesibilidad de los estados.** `role="status"` (loading) y `role="alert"` (error) hacen que un lector
   de pantalla anuncie el cambio sin que el usuario tenga que buscarlo (WCAG SC 4.1.3, cruce con 4.4).
5. **No tragarse el error.** El `.catch` pone `fase: "error"`, no `tareas: []`. Disfrazar un fallo de vacío
   hace que la UI mienta.

## Puntos resbalosos (donde el corrector debe mirar)
- **`<ul>` vacío:** olvidó el `if (length === 0)` → cae en el `.map` sobre cero elementos. Pasa a medias el
  test (la lista vacía no tiene `<li>`, pero tampoco el botón del empty), así que el test de empty falla.
- **Empty como `role="alert"`:** confunde "sin datos" con "error". El test de empty exige que NO haya alert.
- **Reintento decorativo:** botón sin `onClick={ejecutarCarga}` (no recarga). El test lo detecta (espera 2
  llamadas a `cargar`).
- **Estado redundante:** guarda `tareas` en otro `useState` "para tenerlas a mano" → dos fuentes de verdad.
- **Mensaje de error filtrando el backend:** mostrar `estado.mensaje` crudo si trae detalles sensibles; un
  excelente muestra un texto humano y deja el detalle para logs.

## Rango de soluciones aceptables
- El render puede ser un `switch` o una cadena de `if` con returns tempranos; ambos valen si son exhaustivos.
- El loading puede ser un texto con `role="status"` o un skeleton (mejor); el empty puede ser un mensaje +
  cualquier `<button>` que invite a crear (el test acepta varios nombres: crear/nueva/agregar/empezar/añadir).
- Un `useReducer` en vez de `useState` es aceptable si el alumno lo justifica; no es necesario para este tamaño.
- Los textos exactos no importan: importa que los cuatro estados existan, sean distintos, accesibles y con salida.
