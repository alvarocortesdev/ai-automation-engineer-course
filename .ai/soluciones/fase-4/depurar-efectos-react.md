---
ejercicio_id: fase-4/depurar-efectos-react
fase: fase-4
sub_unidad: "4.5"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Depura un panel lleno de useEffect

## Tabla de veredictos (la respuesta corta)

| Efecto | Veredicto | Antipatrón |
|---|---|---|
| **EFECTO 1** (`setConteo(mensajes.length)`) | ❌ mal | Estado derivado disfrazado de efecto |
| **EFECTO 2** (socket de `modelo`, deps `[]`) | ❌ mal | Dependencia faltante (`modelo`) |
| **EFECTO 3** (`cargarInfoModelo(modelo)`) | ❌ mal | Falta cleanup → race condition |
| **EFECTO 4** (`document.title`, deps `[modelo, conteo]`) | ✅ **bien** | (uso legítimo de efecto) |
| **EFECTO 5** (analytics si `enviado`) | ❌ mal | Debió ser event handler |

## Diagnóstico detallado

### EFECTO 1 — estado derivado
- **Consecuencia:** `conteo` es siempre `mensajes.length`. Guardarlo en estado + sincronizarlo con un efecto provoca un **render extra** por cada cambio de `mensajes` (primero se pinta con el conteo viejo, luego el efecto corre y dispara otro render) y crea una segunda fuente de verdad que puede desincronizarse.
- **Arreglo (mínimo):** borrar el `useState` de `conteo` y este efecto; derivar en el render:
  ```tsx
  const conteo = mensajes.length;
  ```

### EFECTO 2 — dependencia faltante
- **Consecuencia:** el efecto **sí** limpia bien (`socket.close()`), pero como las deps son `[]`, solo conecta **una vez** con el `modelo` inicial. Si el prop `modelo` cambia de "gpt" a "claude", el componente sigue escuchando el socket de "gpt" (valor *stale* capturado en el closure); "claude" nunca se conecta.
- **Arreglo (mínimo):** declarar la dependencia para que se reconecte al cambiar el modelo:
  ```tsx
  }, [modelo]);
  ```

### EFECTO 3 — falta cleanup (race condition)
- **Consecuencia:** sin cleanup, si el usuario cambia de modelo rápido se disparan dos `cargarInfoModelo`; la respuesta del modelo **viejo** puede llegar **después** y pisar la del nuevo (`setInfo` con datos equivocados). Además puede hacer `setState` tras desmontar.
- **Arreglo (mínimo):** flag `ignorar` + cleanup (no se puede hacer el callback de `useEffect` `async` directo):
  ```tsx
  useEffect(() => {
    let ignorar = false;
    cargarInfoModelo(modelo).then((data) => {
      if (!ignorar) setInfo(data);
    });
    return () => { ignorar = true; };
  }, [modelo]);
  ```

### EFECTO 4 — CORRECTO
- **Por qué está bien:** sincroniza el componente con `document.title`, que es un **sistema externo a React** (el caso de uso real de `useEffect`). Lee `modelo` y `conteo`, y **ambos** están en las deps. No necesita cleanup porque asignar un string no es una suscripción ni reserva recursos (a lo sumo se podría restaurar el título al desmontar, pero su ausencia no es un bug). Este es el efecto que el alumno debe reconocer como legítimo.

### EFECTO 5 — debió ser event handler
- **Consecuencia:** registrar analytics es una **respuesta a una interacción** (el clic en "Enviar"), no una sincronización con un sistema externo. Resolverlo con una bandera `enviado` + efecto añade un render de más, acopla el analytics a un ciclo de render, y en `<StrictMode>` (dev) puede **disparar dos veces**. El "setEnviado(false)" delata el parche.
- **Arreglo (mínimo):** mover la llamada al handler y borrar el estado `enviado` y este efecto:
  ```tsx
  function enviar() {
    setMensajes((prev) => [...prev, { id: crypto.randomUUID(), texto: "hola" }]);
    registrarAnalytics("mensaje_enviado", modelo);
  }
  ```

## Regla general (la frase que debe poder decir el alumno)
> `useEffect` es **solo** para sincronizar el componente con un sistema externo (DOM imperativo, subscripciones, red). Lo que se puede **calcular** de props/estado va en el render (estado derivado). Lo que ocurre **en respuesta a una interacción** va en el event handler.

## Cómo calificar
- **Competente** exige: los 5 veredictos correctos + los 4 antipatrones nombrados con el término correcto + EFECTO 4 justificado como legítimo.
- Acepta sinónimos razonables: "dependencia faltante" ≈ "stale closure / deps incompletas"; "debió ser handler" ≈ "no es un efecto, es un evento".
- **No** aceptes "EFECTO 1 = bucle infinito" (es render de más) ni "EFECTO 2 = falta cleanup" (sí lo tiene; el bug es la dep). Esos dos son los errores de comprensión más reveladores: márcalos y pide la verificación de la rúbrica.
- Si marca EFECTO 4 como roto, es el error más importante a corregir: confunde "tocar document en un efecto" (legítimo) con un antipatrón.
