---
ejercicio_id: fase-4/estados-de-primera-clase
fase: fase-4
sub_unidad: "4.10"
version: 1
---

# Rúbrica — Los cuatro estados de primera clase en React

> Rúbrica **analítica** atada a los `objetivos` del contrato. Ejercicio **de código**: una parte es objetiva
> (el test pasa o no) y otra es de criterio (cómo modeló el estado, si los cuatro estados son distintos y
> accesibles, si el empty vive dentro del éxito). El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es
> una nota: es un mapa de qué observar y cómo dar feedback.

## Objetivos evaluados
> Copiados de `objetivos` en `ejercicio.yml`.

- **O1** — Implementar los cuatro estados (empty/loading/error/success) modelando el estado como máquina de
  estados.
- **O2** — Renderizar cada rama distinta y accesible (loading `role="status"`, error `role="alert"`).
- **O3** — Chequear el vacío dentro del éxito (`length === 0`); dar salida en error (reintentar) y en vacío (CTA).

## Criterios y niveles

### C1 — Los cuatro estados existen y son distintos · mapea: O1, O3
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Solo dibuja el happy path (lista) y/o el loading; falta error o empty; el test no pasa. |
| **en-progreso** | Tres de cuatro estados; típicamente falta el **empty** (renderiza `<ul>` vacío) o el empty se confunde con error. |
| **competente** | Los cuatro estados presentes y **visualmente distintos**; el test pasa en verde. |
| **excelente** | Además distingue tipos de vacío o usa un skeleton (no spinner) para loading, y lo justifica. |

### C2 — Máquina de estados (calidad de modelado) · mapea: O1
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Reescribió el estado con booleanos sueltos (`cargando`/`error`/`vacio`) que pueden contradecirse. |
| **en-progreso** | Mantuvo la unión discriminada pero mete estado redundante (guarda la lista en otro `useState`, o un flag `esVacio`). |
| **competente** | Usa la unión `cargando \| error \| listo` tal cual; el render es un `switch`/cadena de `if` exhaustiva. |
| **excelente** | Sabe explicar por qué la unión hace **imposibles** los estados imposibles vs. tres booleanos. |

### C3 — Accesibilidad de los estados (cruce con 4.4) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Loading y error son texto plano sin rol; un lector de pantalla no se entera del cambio. |
| **en-progreso** | Uno de los dos anunciado (p. ej. error con `role="alert"`) pero el otro no. |
| **competente** | Loading con `role="status"` y error con `role="alert"`; el reintento es un `<button>` real. |
| **excelente** | Conecta con SC 4.1.3 (Status Messages) de WCAG y verifica el anuncio (lo menciona). |

### C4 — Salidas: el usuario nunca queda atrapado · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Error sin reintento; vacío sin CTA (callejón sin salida). |
| **en-progreso** | Hay reintento pero el botón no vuelve a llamar a `ejecutarCarga` (no recarga de verdad), o el CTA no es accionable. |
| **competente** | Error → "Reintentar" que recarga; vacío → CTA que invita a crear. Ambas salidas funcionan. |
| **excelente** | El reintento vuelve a `cargando` antes de reintentar (feedback de que está trabajando otra vez). |

## Errores típicos a marcar
- **Olvidar el empty:** `if (tareas.length === 0)` ausente → renderiza un `<ul>` vacío (la caja en blanco). El error central de la lección.
- **Empty tratado como error:** muestra un `role="alert"` cuando la lista está vacía → la UI miente (success no es error).
- **Tragarse el error:** un `.catch` que vuelve a `{ fase: "listo", tareas: [] }` en vez de `error` → el fallo se disfraza de vacío. (Cruce con 4.7: la `queryFn`/loader debe propagar el error.)
- **Loading/error sin rol** (`role="status"` / `role="alert"` ausentes): el test los exige, pero algunos los ponen como texto y se confunden de por qué el test marca rojo.
- **Estado redundante:** guardar `tareas` en un `useState` separado del estado, reintroduciendo dos fuentes de verdad.
- **Reintento que no recarga:** el botón existe pero su `onClick` no llama a `ejecutarCarga`.
- (transversal seguridad) mensaje de error que filtra el detalle crudo del backend (stack/SQL) al usuario en vez de un texto humano; un "excelente" lo evita.

## Señales de dependencia-IA
> Describir sin acusar; proponer una verificación.

- Código con un `useReducer` sofisticado o una librería de máquinas de estado (XState) impropios del nivel,
  sin que el alumno pueda explicar por qué: pídele que reescriba la misma lógica con `useState` + `switch`.
- Test verde pero no sabe **por qué** el empty va dentro del éxito: pídele que diga qué pasaría si chequeara
  `length === 0` como una cuarta fase de la carga.
- Comentarios pulidos que citan "máquina de estados" pero el código usa tres booleanos: pídele que diga qué
  significa tener `cargando=true` y `error=true` a la vez.
- **Verificación sugerida:** pídele que, sin mirar, agregue un quinto estado (p. ej. "recargando en
  segundo plano") y diga dónde lo pondría. Si entendió el modelo, lo ubica en la unión sin dudar.

## Feedback sugerido (graduado)
> Nunca redactar el componente por el alumno. De menos a más directo.

- **Pista (nivel 1):** "Corre el test y mira qué rama falla. ¿Tienes los **cuatro** estados, o se te
  escapó el vacío? Pregúntate: cuando `cargar` resuelve con `[]`, ¿qué dibuja hoy tu componente?"
- **Pregunta socrática (nivel 2):** "El test de 'empty' pide un botón y que NO haya `<li>` ni `role='alert'`.
  Si tu lista vacía renderiza un `<ul>` sin items, ¿en qué rama del render caíste? ¿Dónde deberías
  chequear `tareas.length === 0`, antes o después de decidir mostrar la lista?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu rama `listo` salta directo al `<ul>`. Antes
  del `.map`, agrega `if (estado.tareas.length === 0) return <vacío con un button CTA>`. Y revisa que tu
  `.catch` ponga `fase: 'error'`, no `tareas: []`: si te tragas el error, la UI miente. No te doy el JSX
  completo: hazlo rama por rama y vuelve a correr el test."

## Conexión con el proyecto / capstone
- Este componente es el **panel de fuentes / lista de conversaciones** del Capstone F4 en miniatura: las
  vistas que cargan server state (4.7) necesitan exactamente estas cuatro ramas para cumplir el gate de
  "estados completos" del Definition of Done. El reflejo de "¿y si vuelve vacío? ¿y si falla?" que entrenas
  aquí es el que hace que tu demo no se caiga delante del evaluador.
