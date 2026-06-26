---
ejercicio_id: fase-0/anatomia-de-una-url
fase: fase-0
sub_unidad: "0.4"
version: 1
---

> 🚫 **SPOILER — material para el CORRECTOR, no para el alumno.** No pegues ni parafrasees de forma reconstruible. Úsalo para detectar el error, nombrar la misconception y graduar pistas. El alumno solo debe leerlo tras cerrar su intento.

# Solución de referencia — Anatomía de una URL y su viaje

## Respuesta canónica

El ejercicio es **abierto** (cada alumno elige su URL), así que no hay un único valor "correcto". Lo correcto es el **patrón**. Usamos como vara esta URL de ejemplo:

```
https://example.com:443/tienda/productos?categoria=audio&orden=precio#resenas
```

### Tabla de descomposición (vara)

| Parte | Valor | Qué hace |
|---|---|---|
| esquema | `https` | protocolo HTTP **sobre TLS** (cifrado). Implica puerto 443 si no se especifica. |
| host | `example.com` | nombre de dominio; se traduce a IP vía DNS. |
| puerto efectivo | `443` | explícito aquí; si faltara, sería 443 **por el esquema `https`** (80 para `http`). |
| ruta (path) | `/tienda/productos` | recurso solicitado dentro del servidor. |
| query string | `categoria=audio&orden=precio` | pares `clave=valor` unidos por `&`; **viaja** al servidor para filtrar/ordenar. |
| fragmento | `resenas` | ancla **dentro** de la página; **no se envía**; lo usa el navegador para hacer scroll. |

### Recorrido (vara, orden canónico)

1. **Parse de la URL** → el navegador separa las partes de arriba.
2. **DNS** → traduce `example.com` a una IP (ej. `93.184.216.34`); usa cachés (navegador/SO/router/resolver) con su `TTL`.
3. **TCP** → handshake (SYN/SYN-ACK/ACK) hacia `IP:443`; abre un canal confiable y ordenado.
4. **TLS** → solo porque es `https`: el servidor presenta certificado, se acuerdan claves, el resto viaja cifrado.
5. **HTTP request** → `GET /tienda/productos?categoria=audio&orden=precio HTTP/1.1` + header `Host: example.com`. El fragmento **no** se incluye.
6. **HTTP response** → línea de estado (`200 OK`), headers (`Content-Type`, `Content-Length`, `Cache-Control`), y body (HTML).
7. **Render** → parse del HTML → DOM; se piden subrecursos (CSS/JS/imágenes, **repitiendo 4–6 por cada uno**); el motor JS ejecuta; layout + paint; salto a `#resenas`.

### Qué NO viaja al servidor
El **fragmento** (`#resenas`). Razón: identifica una sección **dentro** de la página que el navegador ya tiene; no cambia qué pide al servidor, así que se omite de la request. Contraste clave: la **query sí viaja** (el servidor la necesita para decidir la respuesta).

## Razonamiento paso a paso (para que el corrector explique, no solo marque)

La columna vertebral del ejercicio es la **cadena de dependencias causales**, no la lista de siglas:

- DNS va primero porque TCP necesita una **IP**, y la URL solo trae un **nombre**.
- TCP va antes que TLS porque el cifrado se monta **sobre** un canal ya abierto.
- TLS va antes que HTTP **solo en `https`**; en `http` ese paso desaparece (buena pregunta de verificación).
- HTTP request precede a la response (obvio), y el render dispara **más** ciclos request/response → de ahí el costo de **latencia** acumulada.

Si el alumno puede regenerar este orden razonando "qué necesito tener antes de hacer el siguiente paso", interiorizó el modelo. Si solo lo recita, se cae al cambiar `https`→`http` o al preguntarle por qué TLS no va primero.

## Puntos resbalosos / variantes
- **Puerto implícito:** muchos no escriben `:443`; lo correcto es deducirlo del esquema, no dejarlo en blanco.
- **`http://` vs `https://`:** quitar el paso TLS y notar las consecuencias (canal en claro; APIs sensibles y cámara/clipboard exigen HTTPS).
- **Subdominio vs ruta:** `api.example.com/v1` (subdominio, distinto host DNS) ≠ `example.com/api/v1` (misma host, otra ruta). Un alumno avanzado lo distingue.
- **Query codificada:** espacios y acentos van *percent-encoded* (`%20`, `%C3%A9`); no es obligatorio para "competente" pero suma.

## Rango de soluciones aceptables
- Cualquier URL real con esquema/host/ruta/query (fragmento ideal pero no obligatorio) es válida.
- Se acepta granularidad distinta en el recorrido (5 a 8 pasos) **siempre que** el orden causal se respete y las piezas (DNS, IP, TCP, TLS, método HTTP, render) aparezcan donde corresponde.
- No penalizar omitir el detalle de subresursos si el alumno al menos menciona que el render pide más cosas.
- **Penalizar** solo: orden causal roto, puerto sin justificar, o afirmar que el fragmento viaja al servidor.
