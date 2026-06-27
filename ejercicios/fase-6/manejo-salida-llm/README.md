# Ejercicio 6.14 — Output handling: trata la salida del LLM como no confiable

> **Modalidad: código (Primero-Sin-IA, timebox 45 min).** La salida de un LLM es tan
> no confiable como el input de un formulario. Este ejercicio implementa **LLM05
> Improper Output Handling**: el gate por el que pasa la respuesta del modelo **antes**
> de llegar a su destino (un sink HTML, en este caso).

**Fase:** Fase 6 — AI Engineering · **Lección:** `6.14` Seguridad LLM: OWASP LLM + Agentic/ASI
**Ruta:** crítica · **Timebox:** 45 min

## 🎯 Objetivo

Implementar `manejar_salida(texto)`: una función pura (sin API) que recibe la cadena
que produjo el LLM y decide qué hacer con ella antes de renderizarla como HTML,
aplicando tres responsabilidades de seguridad **en orden**.

## 📋 El contrato

`manejar_salida(texto: str) -> Resultado` aplica, **en este orden**:

1. **Fuga (LLM07 / LLM02).** Si el texto contiene un marcador de system prompt o un
   patrón de secreto (`PATRONES_PROHIBIDOS`, comparación **insensible a mayúsculas**)
   → `Resultado(accion="BLOQUEAR", ...)`. Una fuga no se "arregla": se bloquea.
2. **Presupuesto (LLM10 Unbounded Consumption).** Si `len(texto) > MAX_CARACTERES`
   → `BLOQUEAR`. Un techo duro evita salidas abusivas / denial-of-wallet.
3. **Codificación para el sink (LLM05).** Si pasó lo anterior, **escapa el HTML** con
   `html.escape` de la stdlib y devuelve `Resultado(accion="RENDER",
   valor_seguro=<texto escapado>)`. El HTML peligroso (`<script>`) sale **inerte**, no
   bloqueado: codificar es la defensa correcta para este sink.

Constantes (ya en el starter, **no las cambies**):

```python
MAX_CARACTERES = 4000
PATRONES_PROHIBIDOS = ["[[system_prompt]]", "sk-live-"]   # comparación en minúsculas
```

`Resultado` es un dataclass con `accion` (`"RENDER"` | `"BLOQUEAR"`), `motivo` (str
corto) y `valor_seguro` (str escapado en `RENDER`, `None` en `BLOQUEAR`).

## 📏 Primero-Sin-IA (en este orden)

1. **A mano:** en `prediccion.md`, para cada caso de la tabla de abajo, predice la
   `accion` y, en los `RENDER`, si el texto cambia y cómo. **Sin ejecutar, sin IA.**

   | Entrada | accion esperada |
   |---|---|
   | `"Hola, tu pedido va en camino."` | ? |
   | `"<script>alert(1)</script>"` | ? |
   | `"Tu clave interna es sk-LIVE-abc123"` | ? |
   | `"x" * 5000` (5000 caracteres) | ? |

2. **Código:** completa `manejador.py` y haz pasar `pytest`.
3. **Solo al final:** usa IA para *revisar*, no para generar.
4. Mañana, **reescribe la función de memoria**.

## 🛠️ Qué entregar (en esta carpeta)

- `prediccion.md` — tus predicciones **antes** de ejecutar.
- `manejador.py` — la función completa (los tests deben pasar).
- `verificacion.md` — 2-3 frases: por qué **escapamos** el `<script>` pero
  **bloqueamos** la fuga de secreto, y por qué en producción usarías una librería
  vetada (bleach / DOMPurify) en vez de escapar a mano.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `prediccion.md` existe **antes** de ejecutar, con las 4 predicciones + razón.
- [ ] Todos los tests pasan (`pytest`).
- [ ] El `<script>` se **escapa** (accion `RENDER`, `<` ya no aparece crudo), no se bloquea.
- [ ] Una fuga (marcador de system prompt o secreto) se **bloquea**, sin importar largo.
- [ ] `verificacion.md` justifica escapar-vs-bloquear y nombra LLM05 / LLM07 / LLM10.
- [ ] Puedes **explicar el orden de las capas sin notas**.

## ▶️ Cómo correr los tests

```bash
cd ejercicios/fase-6/manejo-salida-llm
python -m pytest -q
```

> Necesitas solo la stdlib de Python (3.10+). No hay dependencias externas ni llamadas
> a ninguna API: todo es determinista.

## 🤖 Cómo pedir la corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-6/manejo-salida-llm/` usando el framework de `.ai/`. Sigue
> `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **política de seguridad** (orden y razón de las capas), no solo
si los tests pasan. La **solución de referencia** vive en `.ai/soluciones/fase-6/` — no
la mires antes de intentarlo de verdad.
