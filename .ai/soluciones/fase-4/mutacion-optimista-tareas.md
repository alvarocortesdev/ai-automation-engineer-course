---
ejercicio_id: fase-4/mutacion-optimista-tareas
fase: fase-4
sub_unidad: "4.7"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — useToggleTarea con optimistic update y rollback

## Respuesta canónica

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

export interface Tarea {
  id: string;
  titulo: string;
  hecha: boolean;
}

export const TAREAS_KEY = ["tareas"] as const;

export function useToggleTarea(toggleApi: (id: string) => Promise<Tarea>) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleApi,
    // 1) ANTES del servidor: cancelar, snapshot, update optimista, retornar contexto.
    onMutate: async (id: string) => {
      await queryClient.cancelQueries({ queryKey: [...TAREAS_KEY] });
      const previas = queryClient.getQueryData<Tarea[]>([...TAREAS_KEY]);
      queryClient.setQueryData<Tarea[]>([...TAREAS_KEY], (viejas) =>
        (viejas ?? []).map((t) => (t.id === id ? { ...t, hecha: !t.hecha } : t)),
      );
      return { previas };
    },
    // 2) Si falla: restaurar el snapshot.
    onError: (_err, _id, contexto) => {
      if (contexto?.previas) {
        queryClient.setQueryData([...TAREAS_KEY], contexto.previas);
      }
    },
    // 3) Pase lo que pase: invalidar para reconciliar con el servidor.
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: [...TAREAS_KEY] });
    },
  });
}
```

## Razonamiento paso a paso
- **`useQueryClient()` dentro del hook:** da acceso a la caché para cancelar, leer, escribir e invalidar.
- **`onMutate` (el corazón optimista):** el orden es deliberado.
  1. `cancelQueries` detiene refetches en vuelo de `["tareas"]`; sin esto, una respuesta vieja podría aterrizar **después** del update optimista y deshacerlo en pantalla (race).
  2. `getQueryData` toma el **snapshot** del estado actual **antes** de modificarlo. Si lo tomaras después de `setQueryData`, guardarías el valor ya cambiado y el rollback no serviría.
  3. `setQueryData` actualiza la caché de forma **inmutable** (`.map` crea un array nuevo, `{ ...t }` crea un objeto nuevo): solo voltea `hecha` de la tarea con ese `id`. Mutar en sitio rompería la detección de cambios de React.
  4. `return { previas }` pasa el snapshot como `contexto` a `onError`/`onSettled`.
- **`onError`:** restaura `contexto.previas`. La guarda `if (contexto?.previas)` evita reventar si `onMutate` no alcanzó a retornar. Es lo que hace que, ante un `PATCH` fallido, la UI vuelva exactamente al estado anterior.
- **`onSettled`:** invalida la query siempre (éxito o error). En éxito, reconcilia la suposición optimista con la verdad del servidor; en error, asegura que la UI termine sincronizada. Es la red de seguridad final.

## Por qué los tests pasan (y qué NO prueban)
- **Test de éxito:** tras `mutate("1")`, `onMutate` voltea la tarea 1 en la caché. No hay `useQuery` montada que observe `["tareas"]`, así que `invalidateQueries` marca la key como stale **pero no refetchea** (no hay observador activo) y el valor optimista persiste. Por eso la caché final muestra `hecha: true`.
- **Test de rollback:** `toggleApi` rechaza; con `retry: false`, `onError` corre y restaura `previas`. La caché vuelve a `TAREAS_INICIALES`.
- Los tests **no** pueden ver si usaste `cancelQueries` ni si mutaste en sitio. Eso lo revisa el corrector abriendo el `.tsx` (C2). Un alumno podría omitir `cancelQueries` y aun así pasar los dos tests: **no es competente en C2**; hay que marcarlo.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Update en `onSuccess` en vez de `onMutate`:** los tests de éxito podrían pasar igual (la caché termina volteada), pero **no es optimista** (la UI esperaría al servidor) y el test de rollback no aplicaría. Márcalo en C1/C2: el espíritu del ejercicio es el optimismo.
2. **Snapshot tarde:** tomar `getQueryData` después de `setQueryData` → rollback inútil. El test de rollback lo atrapa (restauraría el valor ya modificado).
3. **Mutación en sitio:** `viejas.push(...)` o `t.hecha = !t.hecha` sobre el objeto original. Los tests podrían pasar por casualidad, pero rompe la inmutabilidad; obsérvalo.
4. **`onError` sin guarda:** `queryClient.setQueryData(KEY, contexto.previas)` sin `if (contexto?.previas)` revienta si `onMutate` falló antes de retornar.
5. **Invalidar solo en `onSuccess`:** tras un error la caché no se reconcilia. Debe ir en `onSettled`.

## Rango de soluciones aceptables
- `["tareas"]` literal o `[...TAREAS_KEY]`: equivalentes (el spread evita pasar el `readonly` tuple a APIs que esperan `unknown[]`; ambos funcionan).
- Tipar el `contexto` (`onMutate` retorna `{ previas: Tarea[] | undefined }`) o dejar que se infiera: ambos válidos; tiparlo suma en C1-excelente.
- Firmas de callback de 3 args (`onError(err, vars, contexto)`) o las nuevas de 4 args de la última v5 (`onError(err, vars, onMutateResult, context)`): **ambas aceptables** mientras el rollback funcione. Lo importante es que use el snapshot, no la aridad exacta.
- Usar `cancelQueries` con `{ queryKey }` (correcto). Omitirlo "funciona" en el test pero NO es competente (C2).
- Manejar el caso `viejas === undefined` con `?? []` o asumir que siempre hay datos: el `?? []` es más robusto y preferible.
