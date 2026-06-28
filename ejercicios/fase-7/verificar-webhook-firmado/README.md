# Ejercicio 7.2 — Verifica un webhook firmado (HMAC + anti-replay)

> **Modalidad: código (verificado por `pytest`, sin red ni cuenta de pagos).** Un webhook
> entra por una URL pública que ejecuta lógica de negocio. Antes de creerle, hay que verificar
> que es auténtico, íntegro y reciente. Es la pieza de seguridad #1 de cualquier integración.

**Fase:** Fase 7 — Automatización, Orquestación y Data Engineering · **Lección:** `7.2` Ingeniería de integración + confiabilidad
**Ruta:** crítica · **Timebox:** 40 min

## 🎯 Objetivo

- **O1** — Verificar una firma **HMAC-SHA256** sobre el **body crudo en bytes**, recomputando sobre `t.payload`.
- **O2** — Comparar firmas en **tiempo constante** (`hmac.compare_digest`) para no abrir un timing attack.
- **O3** — Aplicar **anti-replay**: rechazar una firma válida pero vieja, verificando la firma *antes* que la frescura.

## 📋 Contexto

Es el guardián de la entrada de tu [capstone F7](/fase-7-automatizacion/proyecto/): el receptor que
decide si un input (un pago, un ticket) es legítimo antes de que el agente actúe sobre él. Sin esta
verificación, cualquiera que descubra tu URL puede inyectar un evento falso y disparar una acción real.

## 📏 Primero-Sin-IA (en este orden, timebox 40 min)

1. Resuélvelo **solo**, a mano. Lee el contrato en `verificador.py` y hazlo pasar test por test.
2. Solo entonces, consulta **documentación oficial** (la sección 9 de la lección: `hmac` y Stripe webhooks).
3. **Solo al final**, usa IA para *revisar* tu código —no para generarlo.
4. Mañana, reescribe la función de memoria. Si no puedes, no la aprendiste todavía.

## 🛠️ Instrucciones

1. Abre `verificador.py` y completa `verificar_webhook` (no cambies la firma ni los strings de salida).
2. Corre los tests:

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

3. Itera hasta que **todos pasen en verde**. El helper `_firmar` en el test te muestra cómo se construye una firma válida: es tu spec del esquema.
4. Añade **al menos un caso de prueba tuyo** en `test_verificador.py` (sugerencia: un timestamp en el futuro fuera de tolerancia).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` pasa en verde: los cuatro estados (`VALIDO`, `FIRMA_INVALIDA`, `EXPIRADO`, `MALFORMADO`) cubiertos.
- [ ] La comparación de firmas usa `hmac.compare_digest`, nunca `==`.
- [ ] La verificación opera sobre `bytes` crudos, no sobre un dict ni un string re-serializado.
- [ ] La firma se verifica **antes** que la frescura del timestamp.
- [ ] Agregaste al menos un test propio.
- [ ] Puedes **explicar sin notas** por qué se firma `t.payload` (anti-replay) y qué ataque previene `compare_digest`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Parsea la cabecera con algo como `dict(p.split("=", 1) for p in header.split(","))`, envuelto en un
`try/except` que devuelva `"MALFORMADO"` si falta `t`/`v1` o si `int(t)` revienta. Luego recomputa el
HMAC sobre `f"{t}.".encode() + payload` con el secreto, y compara con `hmac.compare_digest`. Si no
coincide → `"FIRMA_INVALIDA"`. Recién entonces compara `abs(ahora - t)` con `tolerancia_seg` →
`"EXPIRADO"` o `"VALIDO"`. Verificar la firma antes que la frescura evita confiar en un `t` inventado.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-7/verificar-webhook-firmado.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-7/verificar-webhook-firmado.md` — no la mires
antes de intentarlo de verdad.
