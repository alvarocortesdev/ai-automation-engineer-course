---
ejercicio_id: fase-5/exponer-homelab-cloudflare-tunnel
fase: fase-5
sub_unidad: "5.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es el `docker-compose.yml` de
> referencia: úsalo para detectar qué le falta y graduar pistas, **nunca** para entregárselo. Los
> nombres de imagen y hostname son ilustrativos; lo que importa es el patrón de seguridad.

# Solución de referencia — `docker-compose.yml`

```yaml
services:
  api:
    # El backend de tu app. Solo el túnel debe llegarle: por eso 'expose' (red interna de Docker),
    # NO 'ports'. Así desde internet no se alcanza la api directo, solo a través del conector.
    image: ghcr.io/donpelusa/api-produccion:latest
    env_file: .env            # config inyectada (12-factor), nunca horneada en la imagen
    expose:
      - "8000"                # visible SOLO entre contenedores; no se publica al host
    restart: unless-stopped   # sobrevive a reinicios del homelab

  cloudflared:
    # Conector del túnel: abre una conexión SALIENTE a Cloudflare, por eso NO necesita abrir
    # ningún puerto del router. El TLS se termina en el edge de Cloudflare (no en el origen).
    image: cloudflare/cloudflared:latest
    command: tunnel --no-autoupdate run --token ${CF_TUNNEL_TOKEN}  # token desde el .env, nunca literal
    restart: unless-stopped
```

Con `.env` (ignorado por git) conteniendo `CF_TUNNEL_TOKEN=...` y un `.env.example` que documenta la
clave sin valor.

## Por qué cada decisión (lo que el corrector verifica)

1. **`expose` y NO `ports` en `api`.** `expose` deja el puerto `8000` visible solo dentro de la red
   de Docker; `ports` lo publicaría al host y a internet. El único que debe alcanzar la api es el
   túnel, por la red interna. Es el gemelo del mínimo-privilegio de la 5.5: mínima exposición.
2. **Ningún `ports:` en todo el archivo.** El túnel es una conexión **saliente** (de tu casa hacia
   Cloudflare). No hay nada que escuchar en un puerto de entrada → no se abre ninguno. Si el alumno
   puso `ports` en cualquier servicio, sobra.
3. **Token por entorno.** `${CF_TUNNEL_TOKEN}` se interpola desde el `.env`. Un token literal en el
   `command` sería un secreto en el repo: comprometido para siempre aunque se borre después.
4. **`--no-autoupdate`.** Buena práctica en contenedores: la imagen se actualiza recreando el
   contenedor (CI/CD), no con un auto-update dentro del proceso. No es obligatorio para el lint.
5. **`restart: unless-stopped` en ambos.** El homelab se reinicia (corte de luz, update); la app y el
   túnel deben volver solos.

## Variantes aceptables
- **Forma gestionada localmente** (en vez de token): un servicio `cloudflared` que monte un
  `config.yml` con `ingress` y el archivo de credenciales, corriendo `tunnel run <nombre>`. Es válida
  y más versionable; el ejercicio pide la de token por ser la de menor fricción con Docker. (Si el
  alumno la usó, los tests de token no aplican: evalúa el patrón a mano —credenciales fuera del repo,
  ingress con catch-all `http_status:404`, backend solo interno.)
- **Imagen pineada por digest/tag** (`cloudflare/cloudflared:2026.x.x`) en vez de `:latest`: mejor
  reproducibilidad; cuenta como `excelente`.
- **`api` con `env_file` o con `environment:`**: ambas válidas mientras el secreto no quede en el repo.
- **Una red nombrada explícita** entre `api` y `cloudflared`: innecesaria (comparten la red default de
  compose) pero no es un error.

## Cómo correr de verdad (opcional, requiere cuenta Cloudflare)
1. En el dashboard: Zero Trust → Networks → Tunnels → crear túnel → copiar el token.
2. En el dashboard, mapear el hostname público a `http://api:8000` (nombre del servicio) o
   `http://localhost:8000` según la red.
3. `CF_TUNNEL_TOKEN=... docker compose up -d`. El hostname queda servido con HTTPS válido, sin abrir
   un solo puerto del router.
