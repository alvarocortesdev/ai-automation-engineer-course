---
ejercicio_id: fase-2/flujo-pr-commits-code-review
fase: fase-2
sub_unidad: "2.13"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver
> `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). La redacción exacta varía; lo que se
> mide es el **tipo de commit correcto (con el breaking bien marcado)**, una descripción de PR que
> comunica el *por qué*, y un review que **caza el bug** y comenta el código, no a la persona.

# Solución de referencia — Conventional Commits + PR + code review

## 1. `commits.md` de referencia

```text
1. feat(descuentos): añade aplicar_cupon para descontar por cupón
2. fix(descuentos): corrige el cálculo del total con descuento
3. test(descuentos): cubre cupones válidos e inválidos de aplicar_cupon
4. feat(descuentos)!: lanza ValueError ante cupón inválido

   BREAKING CHANGE: un cupón inexistente ahora lanza ValueError en vez de
   aplicar 0 de descuento y continuar. Quien dependía del comportamiento
   anterior (ignorar el cupón) debe capturar el error.
5. chore(deps): actualiza dependencias y corrige warnings de lint
```

**Por qué cada uno:**
- **1 → `feat`**: agrega funcionalidad nueva (la función no existía). MINOR.
- **2 → `fix`**: corrige un bug de cálculo. PATCH.
- **3 → `test`**: solo tests; no cambia producción. Sin bump.
- **4 → `feat!`/`fix!` + `BREAKING CHANGE`**: cambia el **contrato público** (ignorar → lanzar). Es el
  punto del ejercicio. MAJOR. (Da igual `feat!` o `fix!`; lo que NO puede faltar es el `!`/footer.)
- **5 → `chore`** (o `build`): mantenimiento. Idealmente **dos commits** (deps + lint); marcar como
  excelente a quien lo note y lo proponga partir.

## 2. `pr.md` de referencia

```markdown
## Qué
Añade soporte de cupones de descuento al carrito (`aplicar_cupon`). Closes #42.

## Por qué
Los usuarios necesitan aplicar cupones promocionales (10 %, 30 %) al subtotal
antes de pagar; hoy no hay forma de descontar.

## Cómo probarlo
`uv run pytest tests/test_descuentos.py` — cupones válidos, inválido (ValueError).

## Trade-offs
- Cupón inexistente → ValueError (cambio breaking: antes se ignoraba). Decidido
  así para fallar visible en vez de cobrar de más en silencio.
- Porcentajes en una tabla simple por ahora; si crecen, evaluar mover a config/DB.
```

## 3. `review.md` de referencia (3-4 comentarios etiquetados)

```text
🟢 praise: el test parametrizado de cupones válidos + el test del cupón inválido
   (ValueError) cubren bien el contrato. El caso ENVIOGRATIS (0 %) es un buen
   borde para incluir.

🔴 issue (blocking): el cálculo del descuento está en la escala equivocada.
   `descuento = subtotal * pct` con pct=10 da 10× el subtotal, no el 10 %. Para
   aplicar_cupon(10000, "BIENVENIDO10") devuelve 10000 - 100000 = -90000 (total
   negativo). Falta dividir por 100: `subtotal * pct // 100`. De hecho el propio
   test test_cupones_validos (espera 9000) estaría ROJO con este código.

🟡 suggestion (non-blocking): aunque arregles el porcentaje, conviene decidir qué
   pasa si el total quedara negativo por un descuento > 100 %. ¿Clamp a 0? Vale
   una línea de spec/ADR. No bloquea este PR.

❓ question: ¿por qué un dict suelto para TABLA_CUPONES y no un Enum o cargarlo de
   config? No es objeción —quiero entender si es temporal o la forma final.
```

## Razonamiento paso a paso (lo que el corrector busca)
1. **El breaking change (commit 4) es el filtro principal.** Marcarlo `feat`/`fix` sin `!`/`BREAKING
   CHANGE` es el error más común y más caro. Si el alumno lo marca bien y explica *a quién* rompe, C1
   competente.
2. **El bug es findable traduciendo a mano.** `subtotal * pct` con `pct=10` y `subtotal=10000` = 100000;
   `10000 - 100000 = -90000`. El alumno que tradujo el cálculo lo ve; el que solo "leyó por encima" no.
   La pista del propio diff (el test espera `9000`) lo confirma: **la suite ya delata el bug**.
3. **La forma del review importa tanto como el fondo.** Etiquetas (`praise`/`issue`/`suggestion`/
   `question`), separar bloqueante de nit, y comentar el código ("esto devuelve -90000"), no a la persona
   ("no sabes calcular un porcentaje").

## Puntos resbalosos (donde el corrector debe mirar)
1. **Breaking sin marcar** (commit 4): el error central. C1 en-progreso máximo si se le escapa.
2. **Descripciones en pasado/gerundio**: "añadí"/"añadiendo" en vez del imperativo "añade".
3. **No encontrar el bug del porcentaje**: si el `issue` bloqueante no aparece, el review no cumplió su
   función. C3 incompleto/en-progreso.
4. **Review sin `praise`** o sin etiquetas: encuentra el bug pero no enseña qué replicar ni distingue
   bloqueante de opinión.
5. **Atacar a la persona**: cualquier "no pensaste"/"obvio que" baja C3, sin importar si el bug se
   encontró.
6. **Confundir el cupón inválido (commit 4) con el bug del porcentaje (review)**: son cosas distintas; el
   primero es un cambio de contrato intencional, el segundo es un defecto.

## Rango de soluciones aceptables
- **`fix!` en vez de `feat!`** para el commit 4: ambos válidos mientras lleven el breaking marcado.
- **Partir el commit 5** en dos (`chore(deps)` + `style`/`chore: lint`): excelente, no exigible.
- **Proponer el fix exacto** (`subtotal * pct // 100`) o solo señalar la escala mal: ambos cuentan como
  `issue` bloqueante válido; lo importante es que **identifique el bug**, no que dé el parche.
- **El comentario del total negativo** como `issue` en vez de `suggestion`: defendible (es un riesgo
  real); calificar por el razonamiento, no por la etiqueta exacta.
- Más de 4 comentarios, todos pertinentes y etiquetados: bien, mientras no caiga en nitpicking infinito.
- Lo que **no** es aceptable: "lgtm"; no marcar el breaking; no encontrar el bug; review sin etiquetas ni
  distinción bloqueante/preferencia; comentarios que atacan a la persona.
