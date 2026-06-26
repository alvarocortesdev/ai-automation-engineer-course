---
ejercicio_id: fase-1/bitacora-json
fase: fase-1
sub_unidad: "1.5"
version: 1
---

# Rúbrica — Bitácora en JSON (round-trip robusto)

> Rúbrica **analítica** atada a los `objetivos` del contrato. Se evalúa que el round-trip sea
> fiel **y** que el manejo de casos borde refleje una decisión de ingeniería consciente
> (qué error se traga, cuál se propaga), no solo que los tests pasen. Un alumno puede hacer
> pasar los tests escondiendo errores con un `except` genérico: eso NO es competente.

## Objetivos evaluados
- **O1** — Implementar lectura/escritura JSON con round-trip fiel (encoding utf-8, ensure_ascii=False).
- **O2** — Manejar archivo inexistente (default `[]`) vs JSON corrupto (excepción de dominio).
- **O3** — Decidir qué error se traga y cuál se propaga, envolviendo `JSONDecodeError`.

## Criterios y niveles

### C1 — Corrección del round-trip · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No persiste, o `agregar`+`cargar` no devuelve los mismos datos; o usa `dumps`/`loads` sobre el archivo de forma incorrecta. |
| **en-progreso** | Round-trip funciona para ASCII pero se rompe con `ñ`/acentos (falta `encoding="utf-8"` o `ensure_ascii=False`), o escribe escapes `\uXXXX` en el archivo. |
| **competente** | Round-trip fiel con UTF-8; el archivo en disco conserva los caracteres legibles; `agregar` acumula en orden. |
| **excelente** | Además usa `json.dump`/`json.load` (no `dumps`+`write` manual), `indent=2` para legibilidad, y `pathlib` o `with` de forma idiomática. |

### C2 — Manejo de casos borde (decisión de ingeniería) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Archivo inexistente revienta con `FileNotFoundError`; o un `except:` genérico se traga todo. |
| **en-progreso** | Maneja el inexistente (`[]`) pero deja escapar el `JSONDecodeError` crudo, o lo convierte sin preservar la causa. |
| **competente** | Inexistente → `[]`; corrupto → `BitacoraCorrupta`; los dos `except` son **específicos** (`FileNotFoundError`, `json.JSONDecodeError`), no un catch-all. |
| **excelente** | Re-lanza con `raise BitacoraCorrupta(...) from e` (preserva la cadena de causa) y un mensaje que incluye la ruta/contexto útil para depurar. |

### C3 — Calidad de ingeniería (tests reales) · mapea: O1–O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No agregó test propio, o el test agregado no afirma nada (sin `assert`). |
| **en-progreso** | Agregó un test pero redundante con los dados (no cubre un caso nuevo). |
| **competente** | Agregó al menos un caso borde genuino (mensaje vacío, muchos registros, carácter unicode raro). |
| **excelente** | El test propio prueba una propiedad real (p. ej. round-trip idempotente, o que `agregar` no pierde registros previos) con aserciones precisas. |

## Errores típicos a marcar
- **Confundir `dump`/`dumps`** (sin `s` = archivo, con `s` = string): usar `json.dumps(datos, f)` da `TypeError`.
- **Olvidar `encoding="utf-8"`**: "funciona en mi Mac" pero corrompe acentos en otra máquina.
- **Olvidar `ensure_ascii=False`**: el archivo queda con `ñ` en vez de `ñ` (técnicamente válido, pero ilegible y contra el contrato).
- **`except Exception:` o `except:` genérico**: esconde el `JSONDecodeError` y cualquier otro bug. El contrato pide excepciones específicas.
- **No usar `from e`** al re-lanzar: pierde la causa original, dificulta el debug.
- **Reimplementar la serialización a mano** en vez de usar el módulo `json`.
- (transversal testing) test propio sin `assert`, o que persigue cubrir líneas en vez de afirmar comportamiento.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Manejo de excepciones más sofisticado que el resto del código (logging estructurado, custom exception jerarquías) que el alumno no puede explicar.
- Uso de `pathlib` mezclado inconsistentemente con `open()` sin criterio, como pegado de dos respuestas distintas.
- El `from e` aparece pero el alumno no sabe qué hace (no distingue "encadenar causa" de "ocultar").
- **Verificación sugerida:** pedir que explique, sin notas, por qué un archivo inexistente devuelve `[]` pero un JSON corrupto lanza excepción — y qué cambiaría si ambos se trataran igual.

## Feedback sugerido (graduado)
> Nunca dar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Tus dos casos borde —archivo que no existe y archivo con basura— no son el mismo problema. ¿Cuál es 'esperable y benigno' y cuál es 'un bug que debo gritar'? Trátalos distinto."
- **Pregunta socrática (nivel 2):** "¿Qué tipo de excepción lanza exactamente `json.load` cuando el contenido no es JSON? ¿Es subclase de algo que ya conoces? ¿Por qué te conviene envolverla en `BitacoraCorrupta` en vez de dejarla pasar?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "Necesitas dos `except` específicos: `FileNotFoundError` para devolver `[]`, y `json.JSONDecodeError` para re-lanzar `BitacoraCorrupta(...) from e`. El `from e` conserva la causa. Revisa la sección 4.3 de la lección y vuelve a intentar antes de mirar la referencia."

## Conexión con el proyecto / capstone
- Persistir/cargar estado en JSON es la primera versión del almacenamiento del **Capstone F1 — La misma app, dos lenguajes** (antes de migrar a una base de datos en F3). El criterio "qué error se traga vs cuál se propaga" reaparece en cada endpoint que escribas.
