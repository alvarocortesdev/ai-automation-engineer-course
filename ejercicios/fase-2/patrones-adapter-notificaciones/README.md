# Ejercicio 2.5 — Integra dos terceros con Adapter (y prueba Open/Closed)

> **Modalidad: código (sin IA primero).** Este ejercicio entrena el patrón más concreto y testeable de
> la Fase 2: **Adapter**. La regla de oro: *el que se adapta es el extraño, nunca tu dominio.* Tu código
> de negocio no cambia ni una línea; las librerías de terceros se doblan a tu contrato, no al revés.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.5` Patrones de diseño esenciales
**Ruta:** profundización · **Timebox:** 35–45 min

## 🎯 Objetivo

Hacer compatibles **dos librerías de terceros con interfaces incompatibles** (`GatewaySmsLegacy.send_text(...)`
y `ClienteEmailV2.dispatch(payload)`) con el contrato `Notificador` que tu app entiende, escribiendo **un Adapter
por cada una**. Y demostrar **Open/Closed**: agregar el segundo proveedor es escribir una clase nueva, sin tocar
el código de negocio ni el otro adapter.

## 📋 Contexto

Tu dominio (`enviar_alerta`) solo sabe llamar `Notificador.enviar(destino, mensaje)`. El smell que cura Adapter
es la *interfaz incompatible*: cada librería externa habla su propio idioma (otros nombres, otro orden de
argumentos, un parámetro extra, otro formato de payload). Si dejaras que el negocio llamara directo a `send_text`
o a `dispatch`, lo acoplarías a ese proveedor —y migrar sería *shotgun surgery* en cada call site. El Adapter pone
esa traducción en un solo punto. Es exactamente cómo, en la Fase 6, envolverás un cliente de LLM.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces consulta **documentación oficial** (`typing.Protocol`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones (en este orden estricto)

1. **Corre los tests primero.** Están en **rojo** porque los adapters aún no existen (`NotImplementedError`).
   Ése es tu punto de partida (TDD: rojo → verde).

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

2. **Implementa `SmsAdapter`** en `notificaciones.py` para que `GatewaySmsLegacy` satisfaga `Notificador`:
   - cumple `enviar(self, destino: str, mensaje: str) -> None` **por fuera**,
   - por dentro traduce a `gateway.send_text(destino, mensaje, sender=self._remitente)`,
   - guarda el gateway y el remitente en `__init__` (composición, no herencia).
   - Los tests de SMS deben pasar a **verde**.
3. **Demuestra Open/Closed:** escribe `EmailAdapter` para `ClienteEmailV2` (que espera
   `dispatch({"recipient": ..., "subject": ..., "html": ...})`) **sin tocar** `enviar_alerta` ni `SmsAdapter`,
   y **agrega su test** en `tests/test_notificaciones.py` demostrando que `enviar_alerta` funciona con él.
4. Confirma que tu dominio (`enviar_alerta`, el contrato `Notificador`) **no cambió ni una línea**.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tests de SMS pasan **sin que hayas modificado** `enviar_alerta` ni el contrato `Notificador`.
- [ ] `SmsAdapter` y `EmailAdapter` **cumplen `Notificador` por fuera** y traducen a la API ajena por dentro;
      tu dominio nunca importa la librería de terceros directamente.
- [ ] Agregaste `EmailAdapter` con **solo una clase nueva** + su test, sin tocar `SmsAdapter` ni el negocio.
- [ ] (transversal, seguridad) tu adapter **no propaga a ciegas una falla del tercero**: razona qué pasa si la
      librería externa lanza una excepción (déjalo anotado o manéjalo).
- [ ] Puedes **explicar sin notas** por qué "el que se adapta es el extraño" y qué cambiarías para migrar de proveedor.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

Un Adapter es **composición**: guarda la librería de terceros en `__init__` y, en el método de tu contrato,
llama al método ajeno traduciendo nombres y orden de argumentos.

- `SmsAdapter.enviar(destino, mensaje)` → `self._gateway.send_text(destino, mensaje, sender=self._remitente)`.
- `EmailAdapter.enviar(destino, mensaje)` → `self._cliente.dispatch({"recipient": destino, "subject": "Alerta", "html": mensaje})`.

No reimplementes el envío: **solo traduce la llamada**. Revisa la sección 4.4 de la lección antes de mirar la
solución de referencia. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/patrones-adapter-notificaciones.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/patrones-adapter-notificaciones.md` — no la mires
antes de intentarlo de verdad.
