# Diff a revisar (input — no lo edites)

El PR de tu compañero **#42 — "Aplicar cupones de descuento al carrito"**. Tu trabajo es revisarlo
(en `review.md`), no arreglarlo. Hay (al menos) **un bug bloqueante** y **algo bien hecho**: encuéntralos.

Contexto: `subtotal` está en centavos (int). `TABLA_CUPONES` mapea código → **porcentaje de descuento**
(p. ej. `10` significa 10%). La función debe devolver el total ya con el descuento aplicado.

```diff
--- /dev/null
+++ b/descuentos.py
@@
+TABLA_CUPONES = {
+    "BIENVENIDO10": 10,   # 10 % de descuento
+    "BLACKFRIDAY": 30,    # 30 %
+    "ENVIOGRATIS": 0,     # sin descuento sobre el subtotal
+}
+
+
+def aplicar_cupon(subtotal, cupon):
+    """Devuelve el total (centavos) tras aplicar el cupón al subtotal."""
+    if cupon not in TABLA_CUPONES:
+        raise ValueError(f"cupón inválido: {cupon!r}")
+    pct = TABLA_CUPONES[cupon]
+    descuento = subtotal * pct          # <-- porcentaje SIN dividir por 100
+    return subtotal - descuento
```

```diff
--- /dev/null
+++ b/tests/test_descuentos.py
@@
+import pytest
+from descuentos import aplicar_cupon
+
+
+@pytest.mark.parametrize("subtotal,cupon,esperado", [
+    (10000, "ENVIOGRATIS", 10000),   # 0 % → total = subtotal
+    (10000, "BIENVENIDO10", 9000),   # 10 % de 10000 = 1000 → total 9000
+])
+def test_cupones_validos(subtotal, cupon, esperado):
+    assert aplicar_cupon(subtotal, cupon) == esperado
+
+
+def test_cupon_invalido_lanza_valueerror():
+    with pytest.raises(ValueError):
+        aplicar_cupon(10000, "NOEXISTE")
```

> Pista de revisor (no es trampa): el test `test_cupones_validos` con `BIENVENIDO10` espera `9000`
> pero, con el código tal como está, ¿qué devuelve realmente `aplicar_cupon(10000, "BIENVENIDO10")`?
> Tradúcelo a mano antes de escribir tu comentario.
