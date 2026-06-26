---
ejercicio_id: fase-3/cuando-cachear-decision
fase: fase-3
sub_unidad: "3.15"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — ¿Cachear o no? Decide y elige la estructura

## Respuesta canónica (por escenario)

**Escenario A — Catálogo.**
**Primero el índice, no la cache.** El patrón de acceso (lee mucho / cambia 1×día) *favorece* cachear, pero el cuello de botella concreto es un `seq scan` por falta de índice: agregarlo es un arreglo permanente, barato y **sin** staleness. Recién después de medir con el índice puesto, si aún hay costo, una cache aporta.
- *Si se cachea (paso 2, opcional):* **string** con el producto serializado como JSON (`producto:{id}`), **o hash** si se editan campos sueltos. **TTL** de minutos a horas (el dato cambia 1×día → tolera bastante). **Invalidación** por `delete` en la carga nocturna.
- *Riesgo:* staleness tolerable (catálogo). Si la clave es muy popular, jitter en el TTL para evitar thundering herd.

**Escenario B — Sesiones.**
**Sí, usar Redis, pero no como "cache de la DB": como store de sesión compartido.** El bug es que las sesiones viven en memoria del proceso y el load balancer reparte entre 3 instancias → cada una ve solo "sus" sesiones. Redis centraliza el estado.
- *Estructura:* **hash** (`sesion:{id}` → `{user_id, rol, ...}`): permite leer/editar un campo sin reescribir todo.
- *TTL:* igual a la duración de la sesión (p. ej. 30 min, renovado en cada request).
- *Riesgo:* ninguno grande de staleness; cuidar que el TTL coincida con la política de expiración y refrescarlo en actividad.

**Escenario C — Precio en vivo.**
**No cachear (o TTL de ~1 s como mucho).** El dato cambia cada segundo y el negocio exige fidelidad al último segundo: una cache con TTL largo sirve precios rancios (incorrecto), y con TTL de 1 s da casi puro MISS (pagas el costo sin beneficio). Mejor ir a la fuente directa, o un TTL ínfimo solo si el negocio acepta 1 s de desfase.
- *Riesgo evitado:* servir un precio falso (staleness inaceptable). Es el caso de manual de "no cachear datos que cambian en cada request".

**Escenario D — Rate limiting distribuido.**
**Sí, usar Redis** como contador compartido entre las 3 instancias (hoy cada una cuenta por su lado → 300/min reales).
- *Estructura:* **string con `INCR` + `EXPIRE`** por ventana fija (`rl:{ip}`), o **sorted set** para una ventana deslizante más justa.
- *TTL:* la ventana (60 s).
- *Riesgo:* la race `incr`/`expire` (clave sin expirar si el proceso muere entre ambos) → pipeline o Lua para atomicidad; la ventana fija permite ráfagas en el borde (de ahí el sorted set deslizante).

## Razonamiento paso a paso

El esqueleto de decisión para cualquier escenario:
1. **¿Cuál es el cuello de botella real?** (A: índice faltante, no falta de cache.)
2. **¿El dato se lee mucho y cambia poco?** Favorece cache (A, parcialmente). Si cambia en cada request (C), la cache es contraproducente.
3. **¿Es realmente "caching" o es otro uso de Redis?** B (sesión compartida) y D (contador distribuido) usan Redis sin ser una cache de la DB. Separarlo es la marca de quien entendió.
4. **Estructura por caso de uso:** hash para datos con campos (sesión), string+INCR para contadores, sorted set para ventanas/ranking.
5. **TTL = tolerancia de staleness del negocio** + riesgo (thundering herd, race) nombrado.

## Puntos resbalosos (donde el corrector debe mirar)
1. **A sin mencionar el índice:** es el error estrella. El patrón de acceso seduce hacia "cachear", pero la causa raíz se arregla mejor con el índice. Aceptar "cachear" como respuesta a A **solo** si reconoce primero el índice.
2. **C cacheado con TTL largo:** error grave de criterio. Debe ser "no cachear" o TTL ≈ 1 s justificado.
3. **B/D etiquetados como "caching":** si el alumno dice "cacheo la sesión", está en lo correcto operativamente pero conviene matizar que es un store de sesión, no una cache de lecturas de DB; lo mismo para el contador.
4. **Estructura mal elegida:** string-JSON para una sesión que se edita campo a campo es subóptimo (hash es mejor); list para un contador es incorrecto.

## Rango de soluciones aceptables
- En A, tanto "índice primero, cache después como paso 2 opcional" como "índice primero, y probablemente con el índice ya no necesito cache" son **excelentes**; lo inaceptable es saltarse el índice.
- En C, "no cachear" y "TTL de 1 s si el negocio tolera 1 s de desfase" son ambas válidas si se argumenta el trade-off.
- En B, usar un **string-JSON** para la sesión (en vez de hash) es **competente** si se justifica; el hash es la elección **excelente**.
- En D, tanto ventana fija (string+INCR+EXPIRE) como ventana deslizante (sorted set) son válidas; mencionar la race `incr`/`expire` o el problema del borde de ventana sube a **excelente**.
- Cualquier riesgo nombrado con precisión (staleness, race, thundering herd, datos volátiles) cuenta; no se exige una lista cerrada.
