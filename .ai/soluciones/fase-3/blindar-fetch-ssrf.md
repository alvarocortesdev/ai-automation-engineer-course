---
ejercicio_id: fase-3/blindar-fetch-ssrf
fase: fase-3
sub_unidad: "3.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Blinda un fetch saliente contra SSRF

## Implementación canónica (`validar_destino` en `guardia_ssrf.py`)

```python
def validar_destino(url: str, *, resolver=socket.getaddrinfo) -> str:
    partes = urlparse(url)

    # 1. lista blanca de esquemas (bloquea file://, ftp://, gopher://...)
    if partes.scheme not in ESQUEMAS_PERMITIDOS:
        raise DestinoBloqueado(f"esquema no permitido: {partes.scheme!r}")

    # 2. host obligatorio
    host = partes.hostname
    if not host:
        raise DestinoBloqueado("URL sin host")

    # 3. resolver el DNS (un host que no resuelve no es confiable)
    try:
        infos = resolver(host, partes.port or 80)
    except socket.gaierror as exc:
        raise DestinoBloqueado(f"no resuelve: {host}") from exc

    # 4. revisar TODAS las IPs resueltas (defensa contra DNS rebinding)
    for info in infos:
        ip = info[4][0]                  # sockaddr -> (ip, port, ...)
        if _es_ip_peligrosa(ip):
            raise DestinoBloqueado(f"IP no permitida: {ip}")

    # 5. seguro
    return url
```

Verificado contra `test_guardia_ssrf.py`: **10 passed**.

## Por qué cada decisión

- **Lista blanca de esquemas, no negra** — solo `http`/`https`. Esto solo ya cierra `file://` (leer archivos locales), `ftp://`, `gopher://` (clásico para hablar con servicios internos). Una lista negra siempre olvida un esquema.
- **Resolver el DNS y validar la IP, no el string** — el ataque sofisticado no escribe `localhost`: usa un dominio que **resuelve** a `10.0.0.5`, o formas alternativas de 127.0.0.1 (`0.0.0.0`, `2130706433` decimal, `[::1]`). Por eso se resuelve y se mira la IP real con `ipaddress`.
- **Revisar TODAS las IPs** — un atacante que controla el DNS puede devolver una IP pública (pasa una validación ingenua) y una privada (la que se conecta de verdad): *DNS rebinding*. Si **cualquiera** es peligrosa, se bloquea.
- **`169.254.0.0/16` (link-local) es el objetivo estrella** — `http://169.254.169.254/...` es el endpoint de metadatos de AWS/GCP/Azure que devuelve credenciales temporales de la instancia. `_es_ip_peligrosa` lo captura vía `is_link_local`.
- **`gaierror` → bloqueo** — si el host no resuelve, no se puede afirmar que sea seguro: se rechaza.
- **`resolver` inyectable** — permite testear sin red y, en producción, reusar el resultado de la resolución para conectar a la misma IP validada.

## Variantes aceptables
- Recoger todas las IPs en una lista y validar después; o usar un `any(...)`: equivalente al bucle con `raise`.
- Normalizar el host a minúsculas o quitar corchetes de IPv6 antes de resolver: correcto, no necesario para los tests.
- Mensajes de error distintos: el test solo verifica que se lance `DestinoBloqueado`, no el texto.
- Añadir defensas extra (rechazar puertos raros, exigir `https`): aceptable si no rompe el test del host público en `https`.

## No aceptable como competente
- ❌ Lista negra de strings (`if "localhost" in url or "127.0.0.1" in url`): se evade trivialmente; falla `test_host_que_resuelve_a_privada_bloqueado`.
- ❌ Validar solo `infos[0]`: falla `test_dns_rebinding_una_privada_basta_para_bloquear`.
- ❌ No bloquear esquemas distintos de http/https: falla `test_file_scheme_bloqueado`.
- ❌ Hacer el fetch y luego "limpiar" la respuesta: la petición interna ya ocurrió.

## Puntos resbalosos (donde el corrector debe mirar)
1. **El bucle sobre todas las IPs.** Es lo que separa "lo bloquea en el caso fácil" de una defensa real. Verifica que el rebinding test pase.
2. **El orden.** Esquema antes de resolver (no malgastes una resolución en `file://`); host antes de resolver (None rompe `getaddrinfo`).
3. **`info[4][0]`.** El `sockaddr` es `(ip, port)` en IPv4 y `(ip, port, flow, scope)` en IPv6; en ambos la IP es el índice 0.
4. **`bitacora.md`** debe explicar: por qué la lista negra de strings falla, por qué revisar todas las IPs, y el riesgo en un agente de IA (una URL envenenada por prompt injection dispara el fetch interno; el guardia va ANTES del fetch).
