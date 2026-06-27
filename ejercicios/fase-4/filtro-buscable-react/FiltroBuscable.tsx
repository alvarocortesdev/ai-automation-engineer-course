/**
 * Ejercicio 4.5 A — Filtro buscable tipado.
 *
 * Implementa el componente `FiltroBuscable`. Respeta la firma exportada:
 * el corrector y los tests importan exactamente `FiltroBuscable` y `FiltroBuscableProps`.
 *
 * Reglas del ejercicio:
 *   - Input controlado (value + onChange) con el placeholder de la prop.
 *   - La lista filtrada se calcula EN EL RENDER (estado derivado), case-insensitive.
 *   - <ul>/<li> con key estable (el propio string del item).
 *   - "Sin resultados" cuando no hay coincidencias.
 *   - CERO useEffect, CERO estado redundante para la lista filtrada.
 */

export interface FiltroBuscableProps {
  items: string[];
  placeholder?: string;
}

export function FiltroBuscable({ items, placeholder }: FiltroBuscableProps) {
  // TODO: 1) estado para la consulta (input controlado).
  // TODO: 2) calcula la lista filtrada AQUÍ, en el render (no en un useEffect).
  // TODO: 3) renderiza el input + <ul>/<li> + el mensaje "Sin resultados".
  return <p>Reemplázame: implementa FiltroBuscable (placeholder={placeholder}, {items.length} items)</p>;
}
