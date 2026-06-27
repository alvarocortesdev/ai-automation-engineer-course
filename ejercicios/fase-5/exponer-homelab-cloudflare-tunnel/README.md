# Ejercicio 5.9 — Expón tu API del homelab con Cloudflare Tunnel (sin abrir puertos)

> **Modalidad: código (un `docker-compose.yml`).** Escribes el Compose que pone tu API online
> **sin publicar ningún puerto del backend** y **sin abrir puertos del router**, usando un conector
> `cloudflared`. **No necesitas una cuenta de Cloudflare:** los tests **revisan tu Compose como
> texto** (un "lint" de seguridad), no lo ejecutan. Si tienes una cuenta, puedes correrlo de verdad.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.9` Despliegue
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

- **O1** — Exponer un servicio del homelab a internet con **Cloudflare Tunnel**, **sin abrir puertos** del router (conexión saliente).
- **O2** — Mantener el backend con **exposición mínima**: visible solo en la red interna de Docker (`expose`), nunca publicado al host (`ports`).
- **O3** — Inyectar el **token del túnel desde el entorno** (`${CF_TUNNEL_TOKEN}`), sin secretos hardcodeados ni commiteados.

## 📋 Contexto

Es la ruta concreta para poner tu backend online cumpliendo el "dominio + ≥3 usuarios" del capstone
de la fase **sin pagar un cloud ni exponer tu red de casa** — el caso real de un homelab tras CGNAT.

## 📏 Primero-Sin-IA (en este orden, timebox 45 min)

1. Escríbelo **solo**, a mano. Apóyate en la sección 4.4 de la lección, pero **no copies** sin entender: cada decisión (`expose` vs `ports`, token por entorno) tiene un porqué de seguridad.
2. Solo entonces, consulta la **documentación oficial** (sección 9 de la lección).
3. **Solo al final**, usa IA para *revisar* tu Compose —no para generarlo.
4. Mañana, reescríbelo de memoria.

## 🛠️ Instrucciones

1. Abre `docker-compose.yml` y completa los `# TODO`. Tu Compose debe:
   - definir el servicio **`api`** (tu imagen) expuesto **solo en la red interna** (`expose`, **no** `ports`);
   - definir el servicio **`cloudflared`** con la imagen `cloudflare/cloudflared`, que corre `tunnel --no-autoupdate run --token ...`;
   - tomar el token de la variable de entorno **`${CF_TUNNEL_TOKEN}`** (nunca un literal);
   - usar `restart: unless-stopped` en **ambos** servicios;
   - **no publicar ningún puerto al host** (el túnel es saliente: no hace falta `ports:` en ninguno).
2. Añade **un comentario por servicio** explicando *por qué* (no solo qué).
3. El `.env.example` (ya incluido) documenta `CF_TUNNEL_TOKEN`; el `.gitignore` (ya incluido) excluye `.env`. No los borres.
4. Corre los tests:

   ```bash
   pytest
   ```

5. Itera hasta que **todas las verificaciones pasen en verde**.

> Los tests solo necesitan Python + pytest (no instalan ni llaman a Cloudflare). Validan que tu
> Compose tome las decisiones de seguridad correctas, no que el túnel real funcione.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa en verde (todas las verificaciones).
- [ ] Existen los servicios `api` y `cloudflared` (imagen `cloudflare/cloudflared`, corriendo `tunnel ... run --token`).
- [ ] El backend usa `expose` y **no** `ports`; **ningún** servicio publica puertos al host.
- [ ] El token sale de `${CF_TUNNEL_TOKEN}`, no hay literal hardcodeado.
- [ ] Ambos servicios tienen `restart: unless-stopped`.
- [ ] Hay un comentario de *por qué* por servicio.
- [ ] Puedes **explicar sin notas** por qué el túnel es más seguro que abrir el `443` del router.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Dos ideas llevan toda la seguridad. (1) **`expose` vs `ports`:** `expose` deja el puerto visible
solo entre contenedores; `ports` lo publica al host/internet. El backend va con `expose` —solo el
túnel debe llegarle—, y como el túnel es **saliente**, en este diseño **ningún** servicio necesita
`ports:`. (2) **El token es un secreto:** va por variable de entorno (`${CF_TUNNEL_TOKEN}`) que se
lee del `.env` (ignorado por git), nunca escrito en el archivo. El comando del conector es
`tunnel --no-autoupdate run --token ${CF_TUNNEL_TOKEN}`. Revisa la sección 4.4 de la lección antes
de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-5/exponer-homelab-cloudflare-tunnel.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/exponer-homelab-cloudflare-tunnel.md` —
no la mires antes de intentarlo de verdad.
