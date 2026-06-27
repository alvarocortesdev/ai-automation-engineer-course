# Write-up — razonamiento del pipeline

> Responde a mano, sin IA, en prosa breve y defendible (2–5 frases por punto).
> Esto es lo que ninguna IA puede hacer por ti: justificar tus decisiones. El
> corrector evalúa el razonamiento, no si "acertaste una respuesta única".

## (a) `needs: build` + `if:` en el job deploy

¿Por qué el `deploy` lleva **ambos**? ¿Qué controla cada uno y por qué son ortogonales
(no redundantes)?

> _Tu respuesta:_

## (b) Secret de repo vs secret de environment `production`

¿En qué se diferencia un secret guardado a nivel de repositorio de uno guardado en el
environment `production`? ¿Cuándo usarías cada uno? (pista: piensa en staging vs prod, y
en quién/qué puede leer cada secret).

> _Tu respuesta:_

## (c) El gate de PR real

Tu workflow muestra rojo cuando los tests fallan. ¿Qué tienes que configurar **fuera del
YAML** para que un PR con CI en rojo **no se pueda mergear**? Nómbralo con precisión (el
mecanismo exacto y dónde vive).

> _Tu respuesta:_

## (d) Trade-off de la matriz

La matriz de 3 versiones cuesta 3× los minutos de CI. ¿En qué caso concreto lo justificas?
¿En cuál sería desperdicio? Da un ejemplo de cada uno.

> _Tu respuesta:_
</content>
