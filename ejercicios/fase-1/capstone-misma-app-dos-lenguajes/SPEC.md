# Mini-spec — API de despensa (complétala ANTES de codear)

> El hilo **spec-driven** de la Fase 0: piensa el problema en palabras antes de
> escribir una línea. Esto te evita descubrir los casos borde a mitad del código.
> Borra las pistas entre paréntesis al completar cada sección.

## 1. Problema en una frase

(Una API para gestionar los ítems de una despensa: agregar, listar, ver y borrar.)

## 2. Entradas y salidas

- **Entrada de `POST /items`:** (¿qué campos?, ¿qué tipos?)
- **Salida de `POST /items`:** (¿qué devuelve?, ¿con qué status?)
- **Entrada/salida de `GET /items`:** (…)
- **Entrada/salida de `GET /items/{id}`:** (…)
- **Entrada/salida de `DELETE /items/{id}`:** (…)

## 3. Reglas de validación

- `name`: (…)
- `quantity`: (…)
- `unit`: (…)

## 4. Casos borde (¿qué pasa si…?)

| Situación | Respuesta esperada |
|---|---|
| `quantity` es `0` o negativo | (…) |
| falta un campo en el body | (…) |
| el body no es JSON parseable | (…) |
| el `{id}` de la URL no es un número | (…) |
| el `{id}` no existe en la despensa | (…) |
| la despensa está vacía y pido `GET /items` | (…) |

## 5. Persistencia

- ¿Dónde vive el estado? (…)
- ¿Qué pasa con los datos si reinicio el servidor? (…)

## 6. Fuera de alcance (lo que NO hago aquí)

(Ej.: autenticación, base de datos real, edición de ítems, paginación… llegan en
fases posteriores.)
