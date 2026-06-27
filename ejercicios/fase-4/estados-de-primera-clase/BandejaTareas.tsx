/**
 * Ejercicio 4.10 A — Los cuatro estados de primera clase.
 *
 * Completa el componente `BandejaTareas`. Respeta la firma exportada:
 * el corrector y los tests importan exactamente `BandejaTareas` y el tipo `Tarea`.
 *
 * La carga asíncrona YA está cableada (useState + useEffect + ejecutarCarga).
 * Tu trabajo es dibujar LAS CUATRO RAMAS del render:
 *   1) LOADING  -> indicador anunciado a lectores de pantalla (role="status")
 *   2) ERROR    -> mensaje anunciado (role="alert") + botón "Reintentar" que llame a ejecutarCarga
 *   3) EMPTY    -> SOLO cuando fase==="listo" y tareas.length===0: mensaje + CTA (un <button>)
 *   4) SUCCESS  -> <ul>/<li> con cada titulo (key estable = id)
 *
 * Pista: el estado vacío NO es un error ni una carga; es un éxito que volvió sin datos.
 */

import { useEffect, useState } from "react";

export interface Tarea {
  id: string;
  titulo: string;
}

export interface BandejaTareasProps {
  /** Carga las tareas del servidor. Puede resolver con datos, resolver con [], o rechazar. */
  cargar: () => Promise<Tarea[]>;
}

/** Estado de la carga modelado como datos (máquina de estados). NO lo cambies: ya está listo. */
type Estado =
  | { fase: "cargando" }
  | { fase: "error"; mensaje: string }
  | { fase: "listo"; tareas: Tarea[] };

export function BandejaTareas({ cargar }: BandejaTareasProps) {
  const [estado, setEstado] = useState<Estado>({ fase: "cargando" });

  // Dispara la carga y traduce el resultado a una fase del estado.
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

  // Carga una vez al montar.
  useEffect(() => {
    ejecutarCarga();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // TODO: dibuja los CUATRO estados a partir de `estado` (y usa `ejecutarCarga` para reintentar).
  return <p>Reemplázame: dibuja los cuatro estados de BandejaTareas (fase actual: {estado.fase}).</p>;
}
