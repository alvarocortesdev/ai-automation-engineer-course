# 8.2 — Refactor de modelo anémico a aggregate + value object

**Fase:** Fase 8 — System Design y Arquitectura · **Lección:** `8.2` Arquitectura de aplicaciones + DDD táctico
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** código

## 🎯 Objetivo

Refactorizar un modelo **anémico** de una billetera de pre-pago (estilo Copec Pay) a **DDD
táctico**: un value object `Dinero`, un aggregate root `Billetera` que **protege sus
invariantes**, y un domain event `PagoRealizado`. La meta no es "que funcione" —el anémico
ya funciona en el caso feliz—; es hacer que **el estado inválido sea imposible de construir**.

## 📋 Contexto

El modelo anémico de `billetera.py` tiene agujeros que un test feliz no atrapa: el `saldo`
se mantiene a mano (se desincroniza), nada impide dejarlo **negativo**, y el dinero es un
`int` pelado sin invariantes. Esta es la clase de bug que cuesta dinero de verdad. Vas a
cerrarlos no con más validaciones sueltas, sino **moviendo las reglas dentro de los objetos
que las dueñan**. Es el músculo del capstone de la fase (modelar dominios) y de cualquier
sistema de pagos, pedidos o billeteras.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Una invariante a la vez.
2. Solo entonces, consulta la [doc oficial de `dataclasses`](https://docs.python.org/3/library/dataclasses.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* el modelo ni los tests.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones

Abre `billetera.py`: trae el **modelo anémico de partida** (con sus agujeros marcados).
Reescríbelo a DDD táctico, **test-driven** (un ciclo red→green→refactor por invariante,
anotado en `bitacora.md`). El contrato al que debes llegar (lo verifica `acceptance_test.py`):

**Value object `Dinero`**
- `Dinero(centavos: int, moneda: str = "CLP")`, **inmutable** (`@dataclass(frozen=True)`).
- Igualdad **por valor**: `Dinero(1000) == Dinero(1000)`.
- Es **imposible** construir un `Dinero` negativo → `ValueError`.
- `Dinero(a) + Dinero(b)` suma si la moneda coincide; **monedas distintas → `ValueError`**.

**Aggregate root `Billetera`**
- `cargar(monto: Dinero) -> None` — recarga (suma al saldo).
- `pagar(monto: Dinero) -> None` — paga; si no hay saldo suficiente lanza
  `SaldoInsuficiente` (excepción de dominio) y **no** deja el saldo negativo ni registra nada.
- `saldo() -> Dinero` — el saldo es una **función de los movimientos**, no un campo a mano.
- `eventos_no_publicados() -> list` — los domain events registrados, sin mutar lo interno.
- **No** expongas la colección interna de movimientos por referencia (recuerda el "spot the
  leak" de la sección 6.2 de la lección: devolver la lista interna deja saltarse las reglas).

**Domain event `PagoRealizado`**
- Inmutable, nombrado en pasado, con al menos `monto: Dinero`.
- `pagar()` exitoso lo registra; un pago **rechazado no registra evento**.

> ⚠️ **El orden importa.** En `pagar()`: valida el saldo **primero**; solo si alcanza,
> registra el movimiento y **después** el evento. Si emites `PagoRealizado` antes de validar,
> estás anunciando un hecho que no ocurrió.

### Auto-verificación (solo al final)

```bash
uv run pytest acceptance_test.py
```

No la abras antes de cerrar tus ciclos: te quita el trabajo de traducir el contrato a tests.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `Dinero` es `frozen`, compara por valor, y **es imposible** construirlo negativo o sumar monedas distintas (probado con `pytest.raises`).
- [ ] **Es imposible** dejar la `Billetera` en saldo negativo desde afuera: `pagar()` de más lanza `SaldoInsuficiente` y deja el saldo intacto.
- [ ] El saldo se **calcula** de los movimientos; no existe un campo `saldo` mutable que se desincronice.
- [ ] No se puede mutar la colección interna desde fuera (devuelves copia/tupla).
- [ ] `pagar()` exitoso registra un `PagoRealizado`; un pago rechazado **no** registra evento.
- [ ] `bitacora.md` muestra el 🔴 antes del 🟢 en cada invariante.
- [ ] Puedes **explicar sin notas** por qué *calcular* el saldo elimina una clase entera de bug.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `billetera.py` — tu modelo refactorizado (`Dinero`, `Billetera`, `PagoRealizado`, `SaldoInsuficiente`).
- `test_billetera.py` — tus tests (una invariante a la vez).
- `bitacora.md` — el log de ciclos: por cada invariante,
  `🔴 <qué probé> → 🟢 <qué código mínimo> → 🔵 <refactor o "nada">`.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

`Dinero`: `@dataclass(frozen=True)` con `centavos: int` y `moneda: str = "CLP"`; valida en
`__post_init__` (`if self.centavos < 0: raise ValueError(...)`); `__add__` chequea
`self.moneda != otro.moneda`. Para la `Billetera`, guarda una **lista de movimientos**
(cada uno con su tipo carga/pago y un `Dinero`) y calcula `saldo()` sumando cargas y
restando pagos **en centavos** (devuelve `Dinero` al final). La invariante "no negativo" se
protege en `pagar()`: `if monto.centavos > self.saldo().centavos: raise SaldoInsuficiente`,
y **recién después** agregas el movimiento y el evento. Para no filtrar lo interno,
`return tuple(self._movimientos)` o `list(self._eventos)`. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `bitacora.md`**),
- la **rúbrica**: `.ai/rubricas/fase-8/modelar-aggregate-y-value-object.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-8/modelar-aggregate-y-value-object.md`
— no la mires antes de intentarlo de verdad.
