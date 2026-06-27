---
ejercicio_id: fase-4/ux-formulario-prevencion-errores
fase: fase-4
sub_unidad: "4.10"
version: 1
---

# Rúbrica — Rediseña la UX de un formulario hostil

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **a mano** (razonamiento/diseño): no
> hay test. Se evalúa el **criterio de UX**: calidad de los mensajes, timing de validación, prevención,
> estados del envío y conexión con a11y. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Mensajes qué/por qué/cómo sin culpa; timing de validación por campo.
- **O2** — Prevención (H5), affordances, feedback; envío como máquina de estados.
- **O3** — Conectar ≥3 decisiones con accesibilidad.

## Criterios y niveles

### C1 — Mensajes de error claros y constructivos · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Deja mensajes vagos ("inválido") o que culpan ("escribiste mal"); no los reescribe. |
| **en-progreso** | Mejora algunos mensajes pero sin estructura clara o sin decir **cómo** arreglar / sin ejemplo. |
| **competente** | Cada mensaje reescrito con qué/por qué/cómo, sin culpa, con ejemplo de formato cuando aplica. |
| **excelente** | Además da **feedback positivo** (check verde al quedar válido) y traduce la jerga (`se esperaba number`) a lenguaje humano. |

### C2 — Timing de validación · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Mantiene validar-en-cada-tecla, o no decide el timing. |
| **en-progreso** | Cambia a "validar al enviar" para todo, sin matizar por campo. |
| **competente** | Por campo: onBlur la primera vez; en vivo solo tras el primer fallo; submit valida todo. Justificado. |
| **excelente** | Nota casos especiales (la API key conviene validarla onBlur/al pegar, no en cada carácter pegado) y lo razona. |

### C3 — Prevención, affordances y feedback (estados del envío) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No previene nada; el envío sigue sin feedback. |
| **en-progreso** | Una medida de prevención o solo deshabilita el botón; falta modelar éxito/error del envío. |
| **competente** | ≥2 medidas de prevención (input adecuado para frecuencia, formato de ejemplo, toggle de la key); el envío tiene loading ("Conectando…" + deshabilitado), éxito y error. |
| **excelente** | Conecta el envío con la **máquina de estados** de la lección (loading/error/success del submit) y previene la doble conexión explícitamente (idempotencia de UX). |

### C4 — Conexión con accesibilidad · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No menciona a11y. |
| **en-progreso** | Una conexión genérica ("hacerlo accesible"). |
| **competente** | ≥3 decisiones concretas: `<label>` asociados (no placeholder), error con `role="alert"`, foco al primer campo con error, contraste del estado de error. |
| **excelente** | Nota que el error global "No se pudo conectar" debe **mover el foco** y anunciarse, y cita el SC pertinente (4.1.3 Status Messages / 3.3.1 Error Identification). |

## Errores típicos a marcar
- **Reescribir mensajes pero seguir validando en cada tecla:** arregla la mitad y deja la fricción peor.
- **"Validar todo al enviar" como única regla:** mejor que cada-tecla, pero pierde el feedback temprano útil
  (onBlur). El timing es por campo, no binario.
- **Confundir prevención con mensaje:** mejorar el texto del error de frecuencia, pero dejar el campo de
  texto libre (no prevenir con un input numérico/selector).
- **Olvidar los estados del envío:** el formulario es la fuente del bug de doble-submit; si no deshabilita el
  botón ni muestra "Conectando…", no resolvió el problema central del punto 4.
- **Placeholder como label:** no notar que los "labels" son `<div>` y el placeholder hace de etiqueta (falla
  de a11y, cruce con 4.4).
- (transversal seguridad) la API key se ve en pantalla y se pega "a ciegas": un excelente propone toggle
  mostrar/ocultar y no loguear la key; nota que validarla en cliente no reemplaza validarla en el servidor.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Mensajes pulidos y "de manual" pero que no calzan con **estos** campos concretos (no mencionan `sk-`, los
  40 caracteres, la frecuencia en minutos): pídele que reescriba el mensaje del campo de frecuencia con el
  formato real.
- Lista de "buenas prácticas de a11y" copiada sin atarla a los problemas del formulario (labels = div,
  error fuera de vista): pídele que diga qué SC se viola con el placeholder-como-label.
- Propone timing perfecto pero no sabe explicar por qué validar en cada tecla es hostil: pídele que describa
  la experiencia de escribir un email con validación en cada carácter.

## Feedback sugerido (graduado)
> De menos a más directo. Nunca redactar el rediseño completo.

- **Pista (nivel 1):** "Lee tus mensajes de error en voz alta como si fueras el usuario. '¿Campo inválido?'
  ¿Sabrías qué hacer? Un buen mensaje dice qué pasó, por qué y cómo arreglarlo."
- **Pregunta socrática (nivel 2):** "El bug de la doble conexión (punto 4): el usuario hace click de nuevo
  porque no pasó nada visible. ¿Qué estado le falta al botón mientras valida contra el proveedor? ¿Te suena
  a la máquina de estados de la lección?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Para la frecuencia, no mejores el mensaje:
  **previene** el error con un input numérico (o un selector 15/30/60 min) para que no se pueda escribir
  'sesenta'. Y el error global 'No se pudo conectar' debe anunciarse (`role='alert'`) y mover el foco hacia
  él; hoy queda fuera de la vista. No te doy el rediseño entero: completa el timing y la a11y que te faltan."

## Conexión con el proyecto / capstone
- El **input del prompt** y los **ajustes** del Capstone F4 son formularios: este ejercicio te da el criterio
  para que validen con amabilidad, den feedback de envío (botón "Enviando…") y anuncien errores. El envío
  como máquina de estados es la misma idea del ejercicio A aplicada a un submit, y cierra el gate de
  "estados completos" + a11y del Definition of Done.
