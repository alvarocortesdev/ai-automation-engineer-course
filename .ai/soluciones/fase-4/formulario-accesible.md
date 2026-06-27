---
ejercicio_id: fase-4/formulario-accesible
fase: fase-4
sub_unidad: "4.4"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). No hay una única respuesta correcta:
> otro HTML semántico puede ser igualmente `excelente` si pasa el test, se opera con teclado y usa ARIA
> con disciplina.

# Solución de referencia — Haz accesible un formulario

## Respuesta canónica (ejemplo de entrega "excelente")

### `formulario.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Aprobar acción detectada por la IA</title>
    <link rel="stylesheet" href="estilos.css" />
  </head>
  <body>
    <main class="card">
      <h1 class="card__title">Revisar acción detectada por la IA</h1>

      <p class="card__body">
        <!-- Decorativa: el texto ya dice todo. alt="" => el lector la ignora. -->
        <img src="check.svg" alt="" class="card__icon" />
        Renegociar contrato de logística antes de Q1.
      </p>

      <form class="form" novalidate>
        <div class="form__row">
          <label for="nota">Nota para el aprobador <span aria-hidden="true">*</span></label>
          <textarea
            id="nota"
            name="nota"
            required
            aria-describedby="nota-error"
            aria-invalid="true"
          ></textarea>
          <!-- role="alert" => se anuncia solo al aparecer. Enlazado por aria-describedby. -->
          <p id="nota-error" role="alert" class="form__error">
            <span aria-hidden="true">⚠️</span> Escribe una nota antes de aprobar.
          </p>
        </div>

        <div class="form__row">
          <label for="email">Email del aprobador</label>
          <input id="email" name="email" type="email" autocomplete="email" />
        </div>

        <!-- <button> nativo: rol, nombre, foco y teclado gratis. SIN role="button". -->
        <button type="submit" class="boton">Aprobar acción</button>
      </form>
    </main>
  </body>
</html>
```

### `estilos.css` (lo relevante a a11y)

```css
/* Foco visible para teclado, sin molestar al click. Contrasta >= 3:1 (SC 1.4.11). */
:focus-visible {
  outline: 3px solid #1d4ed8;
  outline-offset: 2px;
  border-radius: 4px;
}

/* El error NO depende solo del color: lleva ícono + texto, y el color cumple AA. */
.form__error {
  color: #b91c1c; /* ~5.9:1 sobre blanco */
}

/* Target size cómodo (SC 2.5.8 pide >= 24x24; apuntamos a 44). */
.boton {
  min-height: 44px;
  padding: 0.5rem 1rem;
  background: #1d4ed8;
  color: #fff; /* ~6.7:1 sobre el azul */
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}
```

### `decisiones.md` (ejemplo)

> `<main>` + `<h1>` = landmark y encabezado (SC 1.3.1 / 2.4.6). `<div onclick>` → `<button>`: rol, nombre,
> foco y teclado gratis (SC 2.1.1, 4.1.2); quité el `tabindex="3"` (el orden lo da el DOM). Cada campo con
> `<label for>` (SC 1.3.1, 4.1.2) — el placeholder no es label. Imagen decorativa → `alt=""` (SC 1.1.1).
> Error con `role="alert"` + `aria-describedby` para que se anuncie al aparecer (SC 4.1.3) y con ícono +
> texto, no solo color (SC 1.4.1). `:focus-visible` para que el foco siempre se vea (SC 2.4.7). Probado con
> `Tab`/`Enter` y con VoiceOver.

## Razonamiento paso a paso (lo que debe entender el alumno)
1. **HTML semántico primero.** La mayoría del test pasa solo con `<main>`, `<h1>`, `<button>`, `<label>`,
   porque esos elementos ya traen rol, nombre y teclado. ARIA no se "añade encima": se usa donde el HTML no
   alcanza.
2. **Teclado = orden del DOM + foco visible.** El orden de foco se arregla ordenando el HTML, no con
   `tabindex` positivos. `:focus-visible` muestra el anillo solo a quien tabula.
3. **ARIA quirúrgica.** Solo tres usos legítimos aquí: `aria-describedby` (asociar el error), `role="alert"`
   (anunciarlo al aparecer), `aria-invalid` (marcar estado). El `<button>` y `<main>` no llevan ARIA.
4. **alt es una decisión.** Decorativa → `alt=""` (silencio); informativa → describe la info; funcional →
   describe la acción.

## Puntos resbalosos (donde el corrector debe mirar)
- **ARIA redundante:** `role="main"` en `<main>` o `role="button"` en `<button>` — pasa el test pero
  delata que no entendió la Primera Regla. Marcar como `en-progreso` en C2.
- **`placeholder` como label:** si el alumno deja placeholders y agrega `aria-label` igual al placeholder,
  técnicamente pasa, pero lo ideal es `<label>` visible (mejor para todos, no solo lector).
- **`outline: none`** colado en el CSS sin `:focus-visible` que lo reemplace.
- **Error solo color:** test verde pero el mensaje sigue siendo solo rojo, sin ícono ni texto adicional.
- **`alt="check"`** en la imagen decorativa: pasa el test (tiene alt) pero agrega ruido al lector.

## Rango de soluciones aceptables
- Cualquier HTML semántico que pase los siete chequeos cuenta: `<section aria-labelledby>` en vez de
  `<main>` puede valer si hay landmark; el encabezado puede ser `<h2>`; el botón puede ser
  `<button type="button">`.
- El nombre accesible puede venir de `<label for>`, label envolvente o `aria-label` (label visible es
  preferible, pero no obligatorio para el test).
- La paleta y los valores de contraste pueden variar mientras pasen AA.
- `decisiones.md` puede ser breve; lo que importa es que **mapee arreglos a SC** y que el alumno pueda
  defender por qué cada ARIA está (o no está).
