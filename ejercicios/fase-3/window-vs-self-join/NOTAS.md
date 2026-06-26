# NOTAS — window functions vs self-join

> Completa estas 4–6 líneas con tus propias palabras (no copies la lección). El corrector
> evalúa que el razonamiento calce con tu SQL.

## La versión "obvia" de (B) — self-join / subquery correlacionada

<!-- Pega aquí la versión obvia que pensaste primero (la que re-escanea por fila). -->

## Por qué la versión ROW_NUMBER reemplaza al self-join

<!--
Responde en concreto:
- ¿Cuántas veces recorre la tabla la versión correlacionada vs la versión window?
- ¿Con qué bucle de DSA se parece el self-join? (pista: O(n²))
- ¿Por qué `WHERE rn = 1` debe ir en una subquery/CTE y no en el SELECT que calcula `rn`?
-->
