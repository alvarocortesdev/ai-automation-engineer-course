# Write-up — Pipeline a producción de <tu proyecto>

> El write-up de trade-offs es parte del Definition of Done (DoD 8). Honesto: qué elegiste,
> qué mediste, qué falló. Borra las pistas y completa. (El README público va en inglés; este
> write-up puede ir en tu idioma de trabajo.)

## Decisiones y trade-offs
<!-- TODO: dónde corre y por qué; qué gates de seguridad pusiste y qué ataque previene cada uno;
     pin a SHA vs. estar al día; qué exporter de telemetría y por qué. Liga a tus ADRs. -->

## Qué medí
<!-- TODO: costo mensual estimado; latencia/tamaño de imagen; tiempo de deploy; tiempo de rollback. -->

## Usuarios reales (≥3)
<!-- TODO: quiénes (sin datos sensibles), qué hicieron, en qué fechas. Tráfico real, no sintético. -->

## La falla (la historia que importa)
<!-- TODO: ¿algo se rompió con usuarios reales? Qué, cómo lo detectaste (¿correlation ID? ¿traza?),
     cómo lo arreglaste, qué cambiaste para que no se repita. Esta es la semilla de tu post-mortem
     público de Track-0. Si NADA se rompió aún, di qué fallo provocarías a propósito para probar
     tu observabilidad y tu rollback. -->

## Qué haría distinto / siguiente paso
<!-- TODO: límites conocidos; qué endurecerías con más tiempo. -->
