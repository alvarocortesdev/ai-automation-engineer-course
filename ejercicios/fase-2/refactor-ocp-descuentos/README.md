# Ejercicio 2.4 — Refactor a Open/Closed con red de tests

> **Modalidad: código (sin IA primero).** Este ejercicio entrena el corazón de la Fase 2: **refactorizar
> sin cambiar el comportamiento**, con una suite de tests como red de seguridad. Si los tests cambian,
> el comportamiento cambió: eso es un bug en tu refactor, no un test malo.

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.4` SOLID con crítica
**Ruta:** crítica · **Timebox:** 35–45 min

## 🎯 Objetivo

Refactorizar una función con una cadena de `if/elif` que crece (smell *switch statements*, violación de
**Open/Closed**) hacia un diseño donde la función pública queda **cerrada a modificación**: agregar un tipo
de cliente nuevo es **escribir una clase**, no **editar** código que ya funciona.

## 📋 Contexto

`calcular_descuento` decide el descuento por tipo de cliente con un `if/elif` de cinco ramas. Cada cliente
nuevo obliga a abrir y editar la función —arriesgando romper los casos que ya pasaban—. Este es el smell que
OCP cura. Es exactamente lo que harás en el **Capstone F2** sobre tu propio proyecto: aplicar SOLID donde un
smell lo justifique, con tests verdes antes y después.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Está bien que sea lento.
2. Solo entonces, consulta **documentación oficial** (`abc`, `typing.Protocol`).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones (en este orden estricto)

1. **No toques los tests primero.** Córrelos y confirma que están **verdes**: esa es tu red de seguridad.

   ```bash
   uv run pytest        # o simplemente:  pytest
   ```

2. **Refactoriza** `calcular_descuento` en `descuentos.py` hacia OCP:
   - una abstracción `Descuento` (con `abc.ABC` + `@abstractmethod`, **o** un `typing.Protocol`),
   - una clase por tipo de cliente que implemente un método común `calcular(self, monto: int) -> int`,
   - una función/punto de entrada **cerrado a modificación**: no debe contener `if/elif` ni `isinstance`
     sobre el tipo de cliente para decidir el cálculo.
   - **No cambies la firma pública** `calcular_descuento(cliente_tipo: str, monto: int) -> int`: los tests
     dependen de ella (puedes delegar internamente a las clases, p. ej. con un `dict` de registro).
3. Corre los tests de nuevo: deben **seguir verdes sin que los hayas modificado**.
4. **Demuestra OCP de verdad:** agrega el tipo `"mayorista"` (25% de descuento) creando **solo una clase
   nueva** (sin editar las demás ni la lógica de despacho más allá de registrarla) y **agrega su test** en
   `test_descuentos.py`.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Los tests originales pasan **sin haberlos modificado** (refactor = mismo comportamiento).
- [ ] Existe una abstracción `Descuento` y una clase por tipo; la lógica de precio no usa `if/elif`/`isinstance`
      sobre `cliente_tipo`.
- [ ] Agregaste `"mayorista"` (25%) con **solo** una clase nueva + su test, sin tocar las demás clases.
- [ ] `mypy descuentos.py` no reporta errores de tipo (las clases honran el contrato).
- [ ] Puedes **explicar sin notas** qué queda "cerrado a modificación" y por qué tu diseño lo cumple.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El contrato común es `calcular(self, monto: int) -> int`. Cada rama del `if/elif` se vuelve una clase con ese
método. Para conservar la firma pública sin un `if/elif`, mapea el string a una instancia con un `dict`:
`_REGISTRO = {"regular": SinDescuento(), "vip": DescuentoVip(), ...}` y delega
`return _REGISTRO[cliente_tipo].calcular(monto)`. Ese `dict` es un *registro* (un punto de extensión), no el
smell `switch`: agregar un tipo es añadir una clase y una entrada, sin lógica condicional ramificada. Trabaja
en pesos enteros (`//`) para esquivar el `float`. Revisa la sección 4.2 de la lección antes de mirar la
solución de referencia. Esto es una pista, no la solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio),
- la **rúbrica**: `.ai/rubricas/fase-2/refactor-ocp-descuentos.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/refactor-ocp-descuentos.md` — no la mires antes
de intentarlo de verdad.
