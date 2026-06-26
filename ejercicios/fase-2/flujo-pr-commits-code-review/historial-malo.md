# Historial de commits a reescribir (input — no lo edites)

Estos son los 5 mensajes de commit tal cual llegaron, en orden cronológico. Reescríbelos como
Conventional Commits en tu `commits.md`. Contexto: trabajan sobre un módulo `descuentos` de una app de
carrito de compras.

```text
1. "cambios"
2. "ya funciona el descuento"
3. "fix"
4. "ahora el cupón inválido tira error en vez de aplicar 0 (antes lo ignoraba y seguía)"
5. "subo deps y arreglo el lint"
```

Notas de contexto (lo que sabes de cada commit, para elegir el tipo correcto):

1. El commit 1 ("cambios") en realidad **agregó** la función `aplicar_cupon` por primera vez.
2. El commit 2 ("ya funciona el descuento") **arregló** un cálculo que daba mal el total.
3. El commit 3 ("fix") **agregó tests** para `aplicar_cupon` (no arregló nada de producción).
4. El commit 4 cambió el comportamiento público: antes un cupón inexistente se ignoraba (descuento 0)
   y ahora **lanza `ValueError`**. Quien dependía del comportamiento viejo se rompe.
5. El commit 5 mezcla dos cosas: actualizar dependencias en `pyproject.toml` y corregir warnings de lint.
