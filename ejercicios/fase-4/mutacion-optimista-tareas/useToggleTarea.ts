/**
 * Ejercicio 4.7 A — useToggleTarea con optimistic update + rollback.
 *
 * Implementa el custom hook `useToggleTarea`. Respeta la firma exportada:
 * los tests importan exactamente `useToggleTarea`, `TAREAS_KEY` y el tipo `Tarea`.
 *
 * Reglas del ejercicio (patrón completo de la sección 4.6 de la lección):
 *   - useMutation con onMutate / onError / onSettled.
 *   - onMutate:  cancelQueries(["tareas"]) -> snapshot con getQueryData ->
 *                setQueryData INMUTABLE (voltea `hecha` de la tarea con ese id) ->
 *                return { previas }.
 *   - onError:   restaura el snapshot (queryClient.setQueryData(TAREAS_KEY, contexto.previas)).
 *   - onSettled: invalidateQueries(["tareas"]).
 *   - NO mutes la caché en sitio: copia (map + spread).
 */
import { useMutation, useQueryClient } from "@tanstack/react-query";

export interface Tarea {
  id: string;
  titulo: string;
  hecha: boolean;
}

// La identidad de la lista de tareas en la caché. Úsala tal cual.
export const TAREAS_KEY = ["tareas"] as const;

export function useToggleTarea(toggleApi: (id: string) => Promise<Tarea>) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleApi,
    // TODO 1) onMutate: cancela -> snapshot -> setQueryData optimista -> return { previas }
    // TODO 2) onError: restaura el snapshot
    // TODO 3) onSettled: invalida la query de tareas
  });
}
