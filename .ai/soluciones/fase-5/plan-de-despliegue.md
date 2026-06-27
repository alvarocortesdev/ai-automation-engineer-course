---
ejercicio_id: fase-5/plan-de-despliegue
fase: fase-5
sub_unidad: "5.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es **un** plan defendible, no el
> único. Úsalo como vara para evaluar si el plan del alumno está justificado por restricciones,
> **nunca** para dictárselo. Otro plan distinto puede ser igual de válido si lo defiende bien.

# Solución de referencia — Plan de despliegue

## `plan.md` (referencia)

| Pieza | Opción | Justificación (restricción que manda) | Trade-off descartado |
|---|---|---|---|
| **Frontend (Next.js)** | **Vercel** | Plataforma hecha para Next.js: deploy por `git push`, *previews* por PR, CDN y TLS gratis, $0 para proyecto personal. La restricción que manda: es un frontend de un framework con plataforma dedicada. | Dockerizarlo y ponerlo en el VPS: más trabajo, pierdo previews/CDN, gano nada. |
| **Backend (FastAPI)** | **Homelab + Cloudflare Tunnel** | Presupuesto ~$0 y ya tengo el homelab; está tras CGNAT (sin IP pública), así que un túnel saliente lo expone sin abrir puertos. | VPS + Caddy (cuesta ~$5/mes, innecesario teniendo homelab); managed cloud (más caro, cero-ops que no necesito a esta escala). |
| **Base de datos (Postgres)** | **Contenedor en el mismo homelab** (con backups a object storage) **o** managed pequeño | A 3 usuarios, un Postgres en contenedor con volumen + backups cubre; managed si quiero cero-ops de backups/parches. | Managed grande: sobra para 3 usuarios y suma costo. |

> ADR ejemplo: *"Frontend en Vercel y backend en homelab+túnel (no todo junto en un cloud) porque el presupuesto es ~$0, ya tengo homelab, y está tras CGNAT; descarté abrir el router (expone IP de casa) y un VPS pagado (innecesario)."*

## `https.md` (referencia)

| Pieza | Fuente del certificado | Dónde se termina el TLS | Por qué |
|---|---|---|---|
| Frontend (Vercel) | Vercel (gestionado) | Edge de Vercel | No administro certs; la plataforma los emite y renueva. |
| Backend (homelab + túnel) | **Cloudflare (edge)** | Edge de Cloudflare; el origen habla HTTP plano | No tengo IP pública: no puedo hacer HTTP-01 en el origen, y no hace falta —el túnel lleva el tráfico ya descifrado por la red interna. |
| Backend (variante VPS público) | **Let's Encrypt vía Caddy** | En el origen (Caddy) | Tengo IP pública y puerto 80 → HTTP-01 automático. Si no pudiera abrir el 80 o quisiera `*.midominio.com`, usaría **DNS-01**. |

Punto clave que el corrector verifica: **el homelab por túnel NO necesita Let's Encrypt en el
origen** (error típico). El TLS lo pone Cloudflare en el edge.

## `entornos.md` (referencia)

| Variable | dev | staging | prod | ¿Secreto? | Dónde vive |
|---|---|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | `https://api-staging.midominio.com` | `https://api.midominio.com` | **No (pública)** | Vercel por ambiente; se hornea en el bundle del navegador |
| `DATABASE_URL` | local | staging | prod | **Sí** | Solo backend (`.env` del homelab / secret manager); jamás con `NEXT_PUBLIC_` |
| `OPENAI_API_KEY` (u otra) | key dev | key staging | key prod | **Sí** | Solo servidor; nunca en el cliente |

Una línea esperada: *"`NEXT_PUBLIC_*` se incrusta en el JavaScript que descarga el navegador, así que
es pública por diseño; un secreto ahí queda visible en las DevTools de cualquiera."*

## `no-kubernetes.md` (referencia)

Argumento esperado (por restricciones, no por dificultad): *"Kubernetes resuelve **orquestar muchos
servicios**, **auto-escalar** ante carga variable y **self-healing** para equipos/escala grandes.
Mi app tiene un backend, una DB y 3 usuarios: ninguna de esas restricciones existe. Un VPS o el
homelab con `docker compose` y un reverse proxy/túnel cubre el caso con una fracción de la carga
operacional (YAGNI). El **punto de quiebre** donde reconsideraría: muchos servicios independientes,
necesidad de auto-escalar ante picos reales, o un equipo que requiera despliegues self-service —
ahí un managed cloud (Cloud Run / Container Apps) suele ganarle a k8s crudo antes que k8s."*

## Qué cuenta como excelente
- Contrastar dos opciones viables para el backend (túnel vs. VPS+Caddy) y elegir por una restricción concreta.
- Nombrar el punto de quiebre de "no Kubernetes" con una condición medible.
- ADRs de una línea por decisión grande.
- Acertar que el TLS del túnel se termina en el edge (no en el origen).
