# Ejercicio 3.13b — Blinda un fetch saliente contra SSRF

> **Modalidad: código (Python, sin IA).** Implementas el guardia que un agente de IA debe llamar **antes** de cada `fetch` saliente. Es la defensa contra SSRF (A10 del OWASP Top 10), el vector estrella de la era agéntica: si tu servidor pide una URL que el usuario eligió, puede terminar leyendo tu red interna o las credenciales de la nube.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.13` OWASP Top 10 web hands-on
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar `validar_destino(url, *, resolver=...)` en `guardia_ssrf.py` para que `pytest` quede en verde. Debe:

1. Aceptar **solo** los esquemas `http`/`https` (bloquea `file://`, `ftp://`, etc.).
2. **Resolver el DNS** del host y revisar la **IP real**, no el string del host.
3. Rechazar **toda** IP privada, loopback, link-local (metadatos de la nube), reservada, multicast o no especificada.
4. Revisar **todas** las IPs resueltas: si **alguna** es peligrosa, bloquear (defensa contra DNS rebinding).
5. Lanzar `DestinoBloqueado` al rechazar; devolver la URL cuando sea segura.

## 📋 Contexto

Una lista negra de strings ("si la URL contiene `localhost`, bloquéala") no sirve: el atacante usa `127.0.0.1`, `0.0.0.0`, `[::1]`, la forma decimal de la IP, o un **dominio que resuelve** a una IP privada. La defensa correcta resuelve el nombre y valida la IP de destino contra los rangos peligrosos. En la Fase 6/7 vas a darle a un agente herramientas que navegan; este guardia es lo que impide que una URL envenenada (por el usuario o por *prompt injection*) convierta a tu agente en un atacante interno.

## ⚙️ Requisitos

```bash
uv add pytest      # o:  pip install pytest
```

No necesitas red: los tests usan IPs literales (sin DNS) o un resolver simulado.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Corre el test y mira fallar cada caso.
2. Solo entonces, consulta la **documentación oficial** (`urllib.parse.urlparse`, `ipaddress`, `socket.getaddrinfo`) y la lección (sección 4.4).
3. **Solo al final**, usa IA para *revisar* — no para generar.
4. Mañana, reescribe de memoria el orden de los chequeos (esquema → host → resolver → todas las IPs).

## 🛠️ Instrucciones

1. Abre `guardia_ssrf.py`. `ESQUEMAS_PERMITIDOS`, `DestinoBloqueado` y `_es_ip_peligrosa` ya están dados. **No los modifiques.**
2. Implementa `validar_destino` siguiendo los 5 pasos del TODO en la docstring.
3. La IP de cada entrada de `getaddrinfo` está en `info[4][0]` (el `sockaddr` es `(ip, port, ...)`).
4. Corre el test:

   ```bash
   uv run pytest        # o:  pytest
   ```

5. Escribe `bitacora.md`: ¿por qué una lista negra de strings no basta? ¿por qué hay que revisar **todas** las IPs resueltas? ¿por qué es especialmente peligroso un SSRF dentro de un agente de IA que navega?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: bloquea `file://`, `ftp://`, sin-host, `127.0.0.1`, `169.254.169.254`, `10.0.0.1`, `0.0.0.0` y el caso de rebinding; acepta el host público simulado.
- [ ] Resuelves el DNS y validas la **IP**, no el texto del host.
- [ ] Revisas **todas** las IPs resueltas (no solo la primera).
- [ ] `bitacora.md` responde las tres preguntas del paso 5.
- [ ] Puedes explicar **sin notas** por qué bloquear solo `localhost` no detiene un SSRF.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- Orden: `partes = urlparse(url)` → chequea `partes.scheme` → `host = partes.hostname` → `resolver(host, partes.port or 80)` → itera.
- El bucle:

  ```python
  for info in infos:
      ip = info[4][0]
      if _es_ip_peligrosa(ip):
          raise DestinoBloqueado(f"IP no permitida: {ip}")
  ```

- Envuelve la resolución en `try/except socket.gaierror` y traduce a `DestinoBloqueado` (un host que no resuelve no es confiable).

Repasa la sección 4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `guardia_ssrf.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/blindar-fetch-ssrf.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/blindar-fetch-ssrf.md` — no la mires antes de intentarlo de verdad.
