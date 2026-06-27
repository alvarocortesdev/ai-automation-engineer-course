/**
 * Tests del ejercicio 4.7 A — useToggleTarea (Vitest + React Testing Library).
 *
 * Verifican el COMPORTAMIENTO del hook sobre la caché de TanStack Query:
 *   - éxito  → la tarea queda volteada en la caché (lo hizo onMutate);
 *   - fallo  → la caché vuelve al snapshot previo (lo hizo onError = rollback).
 *
 * Sembramos la caché con setQueryData (como si una useQuery ya hubiera traído
 * las tareas) y montamos el hook con un wrapper que provee el QueryClient.
 *
 * Ejecuta:   pnpm test
 */
import { describe, it, expect } from "vitest";
import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { useToggleTarea, TAREAS_KEY, type Tarea } from "./useToggleTarea";

const TAREAS_INICIALES: Tarea[] = [
  { id: "1", titulo: "Escribir spec", hecha: false },
  { id: "2", titulo: "Tests verdes", hecha: true },
];

function crearEntorno() {
  const queryClient = new QueryClient({
    // En tests no queremos reintentos: el fallo debe fallar rápido.
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  // Sembramos la caché como si una useQuery ya hubiera traído las tareas.
  queryClient.setQueryData<Tarea[]>([...TAREAS_KEY], TAREAS_INICIALES);
  const wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
  return { queryClient, wrapper };
}

describe("useToggleTarea — éxito", () => {
  it("voltea `hecha` de la tarea indicada en la caché, sin tocar las demás", async () => {
    const { queryClient, wrapper } = crearEntorno();
    const toggleApi = async (id: string): Promise<Tarea> => {
      const t = TAREAS_INICIALES.find((x) => x.id === id)!;
      return { ...t, hecha: !t.hecha };
    };

    const { result } = renderHook(() => useToggleTarea(toggleApi), { wrapper });
    act(() => result.current.mutate("1"));
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    const cache = queryClient.getQueryData<Tarea[]>([...TAREAS_KEY])!;
    expect(cache.find((t) => t.id === "1")!.hecha).toBe(true); // se volteó
    expect(cache.find((t) => t.id === "2")!.hecha).toBe(true); // intacta
  });
});

describe("useToggleTarea — rollback ante error", () => {
  it("restaura la caché al snapshot previo si la API falla", async () => {
    const { queryClient, wrapper } = crearEntorno();
    const toggleApi = async (): Promise<Tarea> => {
      throw new Error("HTTP 500");
    };

    const { result } = renderHook(() => useToggleTarea(toggleApi), { wrapper });
    act(() => result.current.mutate("1"));
    await waitFor(() => expect(result.current.isError).toBe(true));

    const cache = queryClient.getQueryData<Tarea[]>([...TAREAS_KEY])!;
    // La tarea 1 NO quedó marcada: el rollback devolvió el estado original.
    expect(cache).toEqual(TAREAS_INICIALES);
  });
});

// 👉 Agrega aquí al menos un test tuyo. Idea: usa una promesa CONTROLADA
//    (que resuelves tú) para verificar que, ANTES de que la API responda,
//    la caché ya muestra el cambio optimista.
