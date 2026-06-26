# Ejercicio 3.12a — Verifica un JWT a mano (solo librería estándar)

> **Modalidad: código (Python puro, sin IA, sin PyJWT).** Implementas el verificador de un JWT HS256
> usando únicamente `hmac`, `hashlib`, `base64` y `json`. Es la mejor forma de entender qué protege
> (la firma) y qué NO protege (la confidencialidad) un JWT, y de tocar con las manos el ataque `alg: none`.

**Fase:** Fase 3 — Bases de datos y Backend · **Lección:** `3.12` Autenticación y OAuth2 a fondo
**Ruta:** crítica · **Timebox:** 40–45 min

## 🎯 Objetivo

Implementar `verificar_jwt(token, secret, ahora)` en `verificador.py` de modo que `pytest` quede en verde.
La función debe validar, **en orden de defensa**: estructura → algoritmo → firma → expiración, y devolver
los claims solo si todo pasa. No puedes usar PyJWT ni ninguna librería de terceros.

## 📋 Contexto

En el capstone vas a confiar en PyJWT para validar tokens. Pero antes de confiar en una librería, tienes que
entender **qué hace por dentro**: por qué un payload manipulado se detecta, por qué el `alg` lo fijas tú y no
el token, y por qué la firma se compara en tiempo constante. Quien implementó esto una vez nunca más mete
datos sensibles en un JWT ni cae en `alg: none`.

## ⚙️ Requisitos

```bash
uv add pytest      # o:  pip install pytest
```

(No necesitas nada más: el verificador usa solo la librería estándar.)

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Implementa lo que se te ocurra y **mira los tests fallar**: ver el
   `alg: none` rechazado y el payload manipulado romper la firma es el corazón del aprendizaje.
2. Solo entonces, consulta la **documentación oficial** (`hmac.compare_digest`, `base64.urlsafe_b64decode`).
3. **Solo al final**, usa IA para *revisar* tu solución y tu bitácora — no para generarlas.
4. Mañana, reescribe `verificar_jwt` de memoria.

## 🛠️ Instrucciones

1. Abre `verificador.py`. Lo que **ya viene dado** (no lo modifiques): `firmar_jwt`, los helpers
   `_b64url_encode`/`_b64url_decode` y las cuatro excepciones (`TokenMalformado`, `AlgoritmoNoPermitido`,
   `FirmaInvalida`, `TokenExpirado`).
2. **Implementa `verificar_jwt(token, secret, ahora)`** siguiendo el orden de defensa del docstring:
   - 3 partes que decodifiquen, o `TokenMalformado`.
   - `alg == "HS256"` en el header, o `AlgoritmoNoPermitido` (¡rechaza `"none"`!).
   - Firma HMAC-SHA256 recalculada y comparada con **`hmac.compare_digest`** (no `==`), o `FirmaInvalida`.
   - `exp` presente y `ahora >= exp`, o sigue. Devuelve los claims.
3. Corre los tests:

   ```bash
   uv run pytest        # o:  pytest
   ```

4. Escribe `bitacora.md`: ¿por qué verificas la **firma antes** de leer `exp`? ¿Por qué el algoritmo lo
   decides tú (`algorithms=["HS256"]`) y no el token? ¿Por qué `hmac.compare_digest` y no `==`?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en **verde**: los 9 tests pasan (válido, firma mala, payload manipulado, expirado, frontera,
      `alg: none`, estructura malformada, base64 inválido, sin `exp`).
- [ ] Comparas firmas con `hmac.compare_digest`, no con `==`.
- [ ] Verificas la firma **antes** de confiar en cualquier claim (incluido `exp`).
- [ ] Rechazas explícitamente cualquier `alg` que no sea `HS256` (incluido `none`).
- [ ] Añadiste **al menos un caso de prueba tuyo** en `test_verificador.py`.
- [ ] `bitacora.md` responde las tres preguntas del paso 4.
- [ ] Puedes explicar **sin notas** por qué un atacante no puede falsificar un token sin el secreto.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

- **Estructura:** `partes = token.split("."); if len(partes) != 3: raise TokenMalformado`. Decodifica header
  y payload dentro de un `try/except (ValueError, TypeError)` y re-lanza `TokenMalformado` si falla.
- **Algoritmo:** `if header.get("alg") != "HS256": raise AlgoritmoNoPermitido`. Esto, **antes** de la firma,
  es lo que mata el ataque `alg: none`.
- **Firma:** el `signing_input` es exactamente `f"{h_b64}.{p_b64}"` (las cadenas base64, sin decodificar).
  `firma_esperada = hmac.new(secret.encode(), signing_input.encode(), hashlib.sha256).digest()`, y luego
  `if not hmac.compare_digest(firma_esperada, firma_recibida): raise FirmaInvalida`.
- **Expiración:** `exp = claims.get("exp"); if exp is not None and ahora >= exp: raise TokenExpirado`.

Repasa las secciones 4.4 de la lección antes de mirar la solución de referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `verificador.py` + `bitacora.md` (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-3/verificar-jwt-a-mano.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-3/verificar-jwt-a-mano.md` — no la mires antes de
intentarlo de verdad.
