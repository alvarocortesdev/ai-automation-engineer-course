---
ejercicio_id: fase-4/ux-formulario-prevencion-errores
fase: fase-4
sub_unidad: "4.10"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir
> (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). No hay una única respuesta correcta:
> otros mensajes y decisiones de timing son igualmente válidos si respetan los principios. Evalúa el
> **criterio**, no la coincidencia literal.

# Solución de referencia — Rediseño UX de "Conectar fuente de datos"

## 1. Mensajes de error reescritos

| Campo | Actual | Nuevo (qué / por qué / cómo) |
|---|---|---|
| Nombre | "Campo inválido" | "Ponle un nombre a la conexión para reconocerla después (ej: 'Ventas Q3')." |
| API key | "API key inválida" | "La API key debe empezar con `sk-` y tener al menos 40 caracteres. Cópiala completa desde el panel de tu proveedor." |
| URL | "Escribiste mal la URL" | "La URL debe empezar con `https://` (ej: `https://api.proveedor.com/v1`)." |
| Frecuencia | "Error de tipo: se esperaba number, se recibió string" | (Idealmente prevenido — ver §3. Si igual ocurre:) "Indica cada cuántos minutos sincronizar, como un número (ej: 60)." |
| Conexión falla | "No se pudo conectar" | "No pudimos validar la API key con el proveedor. Revisa que sea correcta y que no esté revocada, e inténtalo otra vez." + botón **Reintentar**. |

Principios: **nunca culpar** ("escribiste mal" → describe el problema), siempre **cómo arreglarlo** + un
**ejemplo**, y traducir la jerga (`se esperaba number`) a lenguaje humano. Añadir **feedback positivo**: un
check verde cuando un campo queda válido.

## 2. Timing de validación por campo

- **Nombre:** valida **onBlur** la primera vez (al salir del campo); en vivo solo si ya falló. No molestar
  mientras escribe.
- **API key:** valida el **formato** (prefijo `sk-`, longitud) **onBlur** / al terminar de pegar — nunca en
  cada carácter pegado. La validación **contra el proveedor** (que la key sea real) va en el **submit**
  (cuesta una llamada de red).
- **URL:** onBlur la primera vez; usar `type="url"` ayuda al patrón base.
- **Frecuencia:** si se previene con un input numérico/selector (§3), casi no necesita validación de
  formato; el rango (p. ej. min 5) se valida onBlur.
- **Submit:** valida **todo** al enviar y, si hay errores, **mueve el foco al primer campo con error**.

Regla rectora: **no castigues al que aún escribe.** Valida al salir; en vivo solo tras el primer fallo (para
que vea cuándo lo corrige).

## 3. Prevención, affordances y feedback

**Prevención (H5):**
- **Frecuencia:** cambiar el texto libre por un **input numérico** (`inputmode="numeric"`) o, mejor, un
  **selector** (15 / 30 / 60 min) → es **imposible** escribir "sesenta". El mejor error es el que no puede
  ocurrir.
- **URL:** `type="url"` + placeholder de ejemplo; mostrar el formato esperado antes de fallar.
- **API key:** **toggle mostrar/ocultar** para que el usuario verifique que pegó la correcta sin dejarla
  expuesta; mostrar el formato esperado (`sk-…`).

**Affordances:** el botón "Conectar" se ve presionable (estados hover/focus de 4.4); los campos válidos
muestran borde/ícono de éxito; un campo deshabilitado se ve deshabilitado.

**Feedback — el envío es una máquina de estados (la idea central de la lección):**
- **loading:** al enviar, el botón pasa a "Conectando…" y **se deshabilita** (mata el bug de la doble
  conexión del punto 4).
- **error:** mensaje claro (§1) **anunciado** + reintento.
- **success:** confirmación explícita ("Conexión 'Ventas Q3' creada") — no limpiar el formulario en
  silencio.

## 4. Accesibilidad (≥3 conexiones con 4.4)

1. **`<label>` asociados** por `for`/`id` (los `<div>` no etiquetan; el placeholder no es label) — SC 1.3.1 / 4.1.2.
2. **Errores anunciados:** cada error de campo con `aria-describedby` + el campo con `aria-invalid="true"`;
   el error global con `role="alert"` para que el lector de pantalla lo diga al aparecer — SC 4.1.3.
3. **Foco al primer error** tras un submit fallido: el usuario de teclado/lector llega directo al problema —
   SC 3.3.1 (Error Identification) / 2.4.3 (Focus Order).
4. (extra) **Contraste** del estado de error (texto rojo ≥ 4.5:1) y no comunicar el error **solo con color**
   (ícono + texto) — SC 1.4.3 / 1.4.1.

## Razonamiento que debe demostrar el alumno
- El mejor mensaje de error es el que **no aparece** (prevención sobre corrección).
- Validar en cada tecla desde la primera letra es **hostil**; el timing correcto es onBlur + en vivo tras
  fallo + submit.
- El **envío** no es "mandar y ya": es una carga con loading/error/success, igual que cualquier fetch (la
  máquina de estados de la lección aplicada al submit).
- La UX de un formulario y su accesibilidad son **lo mismo**: un error que no se anuncia no existe para quien
  usa lector de pantalla.

## Rango de soluciones aceptables
- Los textos exactos de los mensajes pueden variar; importa la estructura qué/por qué/cómo, la ausencia de
  culpa y el ejemplo.
- Para la frecuencia, tanto un input numérico como un selector son válidos (el selector previene más).
- El timing puede variar en matices defendibles; lo no aceptable es "validar en cada tecla desde el inicio".
- Basta con ≥3 conexiones de a11y bien atadas; cuatro o cinco es un excelente.
