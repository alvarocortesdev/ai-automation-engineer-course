# Ejercicio 6.11 — El gate de confianza + validación de un IDP

> **Modalidad: mixto (a mano + código).** Primero predices a mano, sin ejecutar ni usar
> IA. Luego implementas el **cerebro de un pipeline de IDP**: decidir si una factura
> extraída se procesa automáticamente o va a revisión humana (HITL). No necesitas API ni
> API key — los datos extraídos se te **inyectan** como diccionarios.

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.11` Multimodal: STT/TTS/vision/OCR-IDP
**Ruta:** crítica · **Timebox:** 45 min

## Objetivos

- **O1** — Implementar un **gate de confianza**: separar los campos extraídos que se
  auto-aceptan de los que van a **revisión humana**, según un umbral.
- **O2** — Implementar una **validación cruzada** (la suma de las líneas cuadra con el
  total declarado) con **tolerancia** de coma flotante.
- **O3** — Combinar ambos en una decisión `auto` vs `revision_humana`, entendiendo que un
  `confidence` alto **no** garantiza que el dato sea correcto.

## El problema

Un servicio de IDP (Azure Document Intelligence, Textract) te devuelve, por cada factura,
un conjunto de **campos** con un valor y un **`confidence`** (cuán seguro está el modelo
de su lectura), una lista de **líneas** (`items`) y un **total declarado**. Tú decides
qué hacer con eso:

1. **Gate de confianza:** los campos con confidence sobre el umbral se **auto-aceptan**;
   los de abajo (o sin confidence) van a **revisión humana** (HITL).
2. **Validación cruzada:** aunque todos los campos pasen el gate, todavía hay que chequear
   una **regla de negocio**: que la suma de las líneas cuadre con el total declarado. Esto
   atrapa errores que el confidence deja pasar (el modelo leyó bien un total que en sí era
   incoherente).
3. **Decisión final:** se procesa automáticamente **solo si** todos los campos pasan el
   gate **y** el total cuadra. Si cualquiera falla → HITL, con los **motivos**.

Este es, literalmente, el "validación de salida antes de ejecutar" del Definition of Done
del capstone agéntico (Fase 7). Lo construyes aquí, a mano.

## Tu tarea (en este orden — Primero-Sin-IA)

### Parte 1 — A mano (predicción), ~10 min

En un archivo `prediccion.md`, con **umbral = 0.90** y **tolerancia = 0.01**, predice la
decisión de `decidir_procesamiento` para estos 3 casos. **No ejecutes nada todavía.**

- **Caso A (todo limpio):** campos `Proveedor` (0.99), `Fecha` (0.93), `Total` (0.97);
  líneas 60.000 + 30.000; total declarado 90.000.
- **Caso B (campo dudoso):** campos `Proveedor` (0.99), `Total` (0.71); líneas 90.000;
  total declarado 90.000.
- **Caso C (total no cuadra):** campos `Proveedor` (0.99), `Total` (0.97); líneas
  60.000 + 30.000; total declarado **100.000**.

Para cada uno: ¿`auto` o `revision_humana`? Si es HITL, ¿por qué motivo(s)?

### Parte 2 — Código (verificación), ~25 min

1. Abre `idp.py` y completa `clasificar_campos`, `total_cuadra` y `decidir_procesamiento`
   (no cambies las firmas). `decidir_procesamiento` debe **reusar** las otras dos.
2. Corre los tests:

   ```bash
   pytest
   ```

3. Itera hasta que **todos pasen en verde**.

### Parte 3 — Reflexión, ~5 min

En `verificacion.md`, explica en 3-4 frases por qué un `confidence` alto **no** garantiza
que el dato sea correcto, y por qué `total_cuadra` atrapa errores que el gate de confianza
deja pasar. Conéctalo con **Improper Output Handling (OWASP LLM05)**: ¿qué pasaría si un
agente pagara la factura sin esta validación?

## Contrato de las funciones

```python
def clasificar_campos(campos: dict, umbral: float) -> dict:
    """campos: {nombre: {"value": <algo>, "confidence": float | None}, ...}
    Devuelve {"auto": [nombres...], "revisar": [nombres...]} en el ORDEN de entrada.
    Un campo va a "revisar" si su confidence es None o es MENOR que el umbral.
    confidence == umbral se auto-acepta (>= umbral)."""

def total_cuadra(items: list, total_declarado: float, tolerancia: float = 0.01) -> bool:
    """items: [{"descripcion": str, "monto": float}, ...]
    True si abs(suma_de_montos - total_declarado) <= tolerancia.
    Compara con TOLERANCIA, nunca con == sobre floats."""

def decidir_procesamiento(doc: dict, umbral: float, tolerancia: float = 0.01) -> dict:
    """doc: {"campos": {...}, "items": [...], "total_declarado": float}
    Devuelve {"accion": "auto" | "revision_humana", "motivos": [str, ...]}.
    revision_humana si hay campos a revisar O el total no cuadra; junta los motivos.
    Si accion == "auto", motivos == []. Debe REUSAR clasificar_campos y total_cuadra."""
```

## Qué entregar (deja estos archivos en esta carpeta)

- `prediccion.md` — las 3 decisiones a mano + motivos, **antes** de ejecutar.
- `idp.py` — con las tres funciones completadas (los tests pasan).
- `verificacion.md` — la reflexión sobre confianza-vs-corrección y LLM05.

## Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe con las 3 decisiones + motivos, antes de ejecutar.
- [ ] Todos los tests pasan (`pytest`).
- [ ] Un campo con confidence bajo el umbral —o `None`— **siempre** cae en revisión.
- [ ] `total_cuadra` usa **tolerancia**, no `==` sobre floats.
- [ ] `decidir_procesamiento` **reusa** `clasificar_campos` y `total_cuadra` (no duplica).
- [ ] `verificacion.md` separa "confianza" de "corrección" y nombra LLM05.

## Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/idp-confianza-gate/` usando el framework de `.ai/`.
> Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **proceso** (¿predijiste antes de medir?) y tu **comprensión**
(¿la reflexión separa confianza de corrección?), no solo si los tests pasan.
