---
ejercicio_id: fase-7/verificar-webhook-firmado
fase: fase-7
sub_unidad: "7.2"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Verifica un webhook firmado (HMAC + anti-replay)

## Respuesta canónica

```python
import hashlib
import hmac


def verificar_webhook(payload, header_firma, secreto, ahora, tolerancia_seg=300):
    # (1) parseo defensivo de la cabecera -> MALFORMADO si no se puede
    try:
        partes = dict(p.split("=", 1) for p in header_firma.split(","))
        t = int(partes["t"])
        firma_recibida = partes["v1"]
    except (ValueError, KeyError):
        return "MALFORMADO"

    # (2) recomputo el HMAC sobre "<t>.<payload>" con el secreto compartido
    base = f"{t}.".encode() + payload
    esperada = hmac.new(secreto.encode(), base, hashlib.sha256).hexdigest()

    # (3) comparación en tiempo constante (NUNCA '==')
    if not hmac.compare_digest(esperada, firma_recibida):
        return "FIRMA_INVALIDA"

    # (4) anti-replay: la firma es válida, ahora reviso la frescura
    if abs(ahora - t) > tolerancia_seg:
        return "EXPIRADO"

    return "VALIDO"
```

## Razonamiento paso a paso

1. **Parseo defensivo primero.** `dict(p.split("=", 1) for p in header.split(","))` convierte `"t=...,v1=..."` en un dict. Si falta `t`/`v1` (`KeyError`) o `t` no es entero (`ValueError`), se devuelve `MALFORMADO`. El `maxsplit=1` en `split("=", 1)` es importante: una firma hex no tiene `=`, pero protege ante valores con `=`.
2. **HMAC sobre `t.payload` en bytes.** `f"{t}.".encode() + payload` produce `b"1718900000." + <body crudo>`. Firmar el timestamp **dentro** del HMAC es lo que ata la firma a un instante y habilita el anti-replay. El `payload` ya es `bytes`: no se re-serializa nada.
3. **`hmac.compare_digest`.** Comparación en tiempo constante. Devuelve el mismo tiempo coincidan 0 o N caracteres iniciales, cerrando el timing attack que `==` abriría.
4. **Frescura después de la firma.** Solo si la firma es auténtica tiene sentido confiar en `t`. `abs(ahora - t)` cubre tanto el pasado (replay) como un futuro improbable (reloj manipulado). Más viejo/lejano que la tolerancia → `EXPIRADO`.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Body crudo vs. re-serializado.** El error #1. Si el alumno acepta un dict o hace `json.dumps`, la firma jamás coincide con un emisor real (aunque sus propios tests, si se los construyera mal, podrían pasar). Los tests dados firman sobre `bytes`, así que un `json.dumps` fallaría — bien.
2. **`==` en vez de `compare_digest`.** Pasa todos los tests funcionales (el resultado es correcto), pero es **inseguro**. El corrector debe marcarlo aunque los tests estén verdes: es exactamente el caso "verde pero mal" donde la rúbrica pesa la comprensión por encima del test.
3. **Orden firma → frescura.** Si comprueba la frescura antes y devuelve `EXPIRADO`/`VALIDO` sin validar el HMAC, confía en un `t` que un atacante inventó. El test `test_timestamp_viejo_con_firma_valida_es_expirado` usa una firma **válida** justamente para no poder distinguir un orden del otro por el resultado — el corrector lo detecta leyendo el código, no el output.

## Rango de soluciones aceptables

- Parsear la cabecera con regex o con un bucle manual es válido si maneja los tres casos de `MALFORMADO`.
- Devolver `EXPIRADO` solo para el pasado (`ahora - t > tol`) en vez de `abs(...)` es aceptable como `competente`; usar `abs` (cubrir relojes adelantados) es un detalle de `excelente`.
- Cualquier separador equivalente para construir `base` (`b".".join([str(t).encode(), payload])`) cuenta, siempre que produzca `b"<t>." + payload`.
- El orden firma-antes-de-frescura es **innegociable** para `competente`+ en C2: invertirlo es una falla de seguridad real, no un detalle de estilo.
