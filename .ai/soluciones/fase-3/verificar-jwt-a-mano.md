---
ejercicio_id: fase-3/verificar-jwt-a-mano
fase: fase-3
sub_unidad: "3.12"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Verifica un JWT a mano

## Implementación canónica (`verificador.py`)

```python
def verificar_jwt(token: str, secret: str, ahora: int) -> dict:
    # 1) Estructura: exactamente 3 partes que decodifiquen.
    partes = token.split(".")
    if len(partes) != 3:
        raise TokenMalformado(f"esperaba 3 partes, llegaron {len(partes)}")
    h_b64, p_b64, s_b64 = partes
    try:
        header = json.loads(_b64url_decode(h_b64))
        claims = json.loads(_b64url_decode(p_b64))
        firma_recibida = _b64url_decode(s_b64)
    except (ValueError, TypeError) as e:   # binascii.Error y JSONDecodeError son ValueError
        raise TokenMalformado("no se pudo decodificar base64url/JSON") from e

    # 2) Algoritmo: lo fija el verificador, NO el token. Mata el ataque alg:none.
    if not isinstance(header, dict) or header.get("alg") != "HS256":
        alg = header.get("alg") if isinstance(header, dict) else header
        raise AlgoritmoNoPermitido(f"alg no permitido: {alg!r}")

    # 3) Firma: recalcular sobre el TEXTO base64 (no el JSON decodificado) y comparar
    #    en tiempo constante. ANTES de mirar cualquier claim.
    signing_input = f"{h_b64}.{p_b64}".encode("ascii")
    firma_esperada = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(firma_esperada, firma_recibida):
        raise FirmaInvalida("la firma no corresponde al contenido + secreto")

    # 4) Expiración: solo ahora que la firma es confiable.
    exp = claims.get("exp") if isinstance(claims, dict) else None
    if exp is not None and ahora >= exp:
        raise TokenExpirado(f"exp={exp}, ahora={ahora}")

    return claims
```

Verificado contra `test_verificador.py`: **9 passed**.

## Por qué cada decisión

- **El orden importa (defensa en capas).** Estructura → algoritmo → firma → exp. No se mira `exp` antes de validar la firma: `exp` es un claim *dentro* del token, y un token aún no autenticado no es de fiar. Confiar en un claim antes de verificar la firma es el error conceptual central.
- **`alg` fijado por el verificador.** Se exige `header["alg"] == "HS256"` y se rechaza todo lo demás (incluido `"none"`). El token **no decide** cómo se verifica a sí mismo. Esto, hecho *antes* de la firma, neutraliza el ataque `alg: none` y la confusión de algoritmos.
- **`signing_input` es el texto base64, no el JSON decodificado.** La firma se calcula sobre `f"{h_b64}.{p_b64}"` exactamente como llegó. Si el alumno decodifica el payload y lo re-serializa con `json.dumps`, los separadores/orden cambian y la firma jamás cuadra (bug sutil y frecuente).
- **`hmac.compare_digest` y no `==`.** La comparación byte a byte con `==` corta en el primer byte distinto, lo que filtra (por timing) cuántos bytes acertó un atacante. `compare_digest` compara en tiempo constante.
- **`isinstance(..., dict)`** defiende contra un payload/header que decodifica a algo que no es un objeto JSON (p. ej. `123` o `"texto"`), evitando un `AttributeError` y devolviendo el error correcto.

## Variantes aceptables
- Definir un set `ALGORITMOS_PERMITIDOS = {"HS256"}` y chequear pertenencia: equivalente y hasta más limpio.
- Capturar `Exception` en el bloque de decodificación es aceptable si re-lanza `TokenMalformado` (aunque `(ValueError, TypeError)` es más preciso).
- Devolver una copia de `claims` en vez del dict directo: válido, irrelevante para los tests.
- Validar también `iat`/`nbf` (no exigidos): suma, no resta.

## No aceptable como competente
- ❌ Comparar la firma con `==` (aunque pasen los tests: el timing-leak es el punto del ejercicio).
- ❌ Usar el `alg` del token para seleccionar el algoritmo de verificación.
- ❌ Validar `exp` antes que la firma.
- ❌ Importar PyJWT o cualquier librería de terceros: la consigna pide stdlib.
- ⚠️ Re-serializar el JSON para firmar: si por casualidad pasa (no debería), márcalo: es frágil y rompe con cualquier token externo real.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Padding base64url.** Quien implemente su propio decode debe re-agregar el `=`. Los helpers ya lo hacen; si el alumno los reescribe, revisa el `relleno = "=" * (-len(t) % 4)`.
2. **Frontera de expiración.** `ahora >= exp` (la igualdad cuenta como expirado). Un `>` estricto deja pasar el token justo en el segundo de expiración: marca el off-by-one.
3. **`exp` ausente.** Sin claim `exp`, no expira: `claims.get("exp")` es `None` y se salta el chequeo. El test lo verifica.
4. **`bitacora.md`** debe responder: firma-antes-de-exp (no confiar en claims no autenticados), alg fijado por el verificador (alg:none), y `compare_digest` vs `==` (timing).
