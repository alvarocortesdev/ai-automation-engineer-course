# SPEC de despliegue — <tu proyecto>

> Escribe esto **ANTES** de montar el pipeline (lección §4 paso 3). Una spec de deploy seria
> responde "¿y si esto falla a las 3am?" antes de que falle. Borra las pistas y completa.

## Qué se despliega
<!-- TODO: ¿solo la API F3? ¿también el frontend F4? ¿la base de datos es managed o un contenedor? -->

## Dónde corre
<!-- TODO: VPS + Caddy / homelab + Cloudflare Tunnel / Vercel (frontend) / mixto. Por qué. -->

## Topología
<!-- TODO: un diagrama (Mermaid o ASCII) cliente → proxy/HTTPS → app → DB, y dónde sale la telemetría. -->

## Config por ambiente (12-factor)
<!-- TODO: tabla de claves (de .env.example): cuáles cambian por ambiente, cuáles son secreto,
     dónde viven en CI (secrets de Actions) y en runtime (secrets-manager). -->

## Cómo se promueve un cambio
<!-- TODO: PR → CI (lint/test/gates) → merge a main → deploy.yml → verificación /health. -->

## Rollback
<!-- TODO: ¿cómo vuelves a la versión anterior? ¿qué imagen/tag? ¿cuánto tarda? Esto va también al RUNBOOK. -->

## Costo estimado (5.8)
<!-- TODO: costo mensual aproximado del deploy (compute + DB + dominio + tráfico). Aunque sea ≈0. -->

## Estados de fallo previstos
<!-- TODO: DB caída, deploy fallido, certificado expirado, pico de tráfico. Qué pasa y cómo lo detectas. -->
