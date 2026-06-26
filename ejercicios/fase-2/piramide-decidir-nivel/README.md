# 2.6 — Ubica los tests en la pirámide y caza el sobre-mockeo

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.6` Testing: fundamentos
**Ruta:** crítica · **Timebox:** 25 min · **Modalidad:** a-mano (razonamiento/diseño)

## 🎯 Objetivo

Ejercitar el **juicio** que separa a un semi-senior: clasificar tests en la
pirámide (unit / integration / e2e), decidir **qué se mockea y qué no**, y
reconocer dos antipatrones (sobre-mockeo y testear detalles internos). Esto es
literalmente lo que un entrevistador prueba cuando dice "¿cómo testearías esto?".

## 📋 Contexto

No hay código que correr: hay **decisiones que defender**. Un test mal ubicado en
la pirámide o sobre-mockeado no "falla", pero envenena la suite a largo plazo
(lenta, frágil, que se rompe al refactorizar). Saber detectarlo a ojo es el skill.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). Escribe tus respuestas antes de
   consultar nada.
2. Solo entonces, consulta [la pirámide de Fowler](https://martinfowler.com/articles/practical-test-pyramid.html).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar*.
4. Mañana, **reexplícalo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ La tarea

Entrega un archivo `respuestas.md` con tres partes.

### Parte 1 — Clasifica seis tests

Para cada uno, di el **nivel de la pirámide** (unit / integration / e2e) y
**una línea** de justificación (¿toca alguna frontera real? ¿cuántas piezas reales
participan?).

1. Verifica que `calcular_iva(1000)` devuelve `190`, sin tocar nada externo.
2. Abre un navegador con Playwright, hace login, agrega un producto al carrito y
   confirma que aparece en el resumen de la orden.
3. Inserta una fila en una base de datos Postgres **real** (de prueba) mediante el
   repositorio del proyecto, y la vuelve a leer para confirmar que se guardó.
4. Verifica que `formatear_fecha(d)` produce `"2026-06-26"` para una fecha dada,
   con la zona horaria fijada por la propia función.
5. Llama al endpoint `POST /ordenes` con un cliente HTTP de prueba que arranca la
   app **en memoria** y verifica el status 201 y el cuerpo de la respuesta.
6. Verifica que `descuento(monto, "vip")` devuelve `monto * 0.9`, pasando el tipo
   de cliente como argumento.

### Parte 2 — Caza el antipatrón en dos fragmentos

Para **cada** fragmento: di **qué está mal** y **cómo lo arreglarías** (en
palabras, sin escribir la suite completa).

**Fragmento A** (Python — el SUT `total_carrito` es lógica pura que internamente
llama a `_sumar_items`, también pura, sin fronteras):

```python
def test_total_carrito(mocker):
    mock_sumar = mocker.patch("tienda._sumar_items", return_value=100)
    total = total_carrito([("pan", 1000, 2)])
    assert total == 119  # 100 + IVA
    mock_sumar.assert_called_once()
```

**Fragmento B** (el SUT es una clase `Cuenta` con un método público `depositar`
y un atributo interno `_saldo`):

```python
def test_depositar():
    cuenta = Cuenta()
    cuenta.depositar(500)
    assert cuenta._saldo == 500          # ¿es esto lo que importa?
    assert cuenta._ultima_operacion == "deposito"
```

### Parte 3 — Diagnostica una suite

Tu equipo tiene una suite con **4 tests e2e y 2 unit**. En un párrafo: ¿qué
antipatrón es?, ¿qué problemas concretos te causará?, y ¿qué harías para
corregir la forma de la pirámide?

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] Clasificaste los **6** con una justificación coherente (no solo la etiqueta).
- [ ] En el Fragmento A identificaste el **sobre-mockeo** (mock de una función pura
      sin frontera) y propusiste no mockearla.
- [ ] En el Fragmento B identificaste el test de **detalle interno** (afirma sobre
      `_saldo`/`_ultima_operacion`) y propusiste testear comportamiento observable.
- [ ] Nombraste el **cono de helado** y diste una acción concreta para corregirlo.
- [ ] Puedes explicar **sin notas** la regla "mockea solo en la frontera".

## 📦 Qué entregar

- `respuestas.md` con las tres partes.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

La pregunta que clasifica: ¿el test toca una **frontera real** (DB, HTTP de red,
navegador)? Ninguna → unit (casos 1, 4, 6). Una/dos piezas reales del sistema
juntas → integration (casos 3 y 5: DB real, app real en memoria). App entera como
usuario → e2e (caso 2). En el Fragmento A, `_sumar_items` es pura: mockearla acopla
el test a *cómo* se calcula y deja de probar el cálculo real. En el Fragmento B,
afirmar sobre `_saldo` ata el test a la implementación; mejor afirmar sobre un
método público como `cuenta.saldo()` o el efecto observable de una operación
posterior. Pista, no solución.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu `respuestas.md`,
- la **rúbrica**: `.ai/rubricas/fase-2/piramide-decidir-nivel.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/piramide-decidir-nivel.md`
— no la mires antes de intentarlo de verdad.
