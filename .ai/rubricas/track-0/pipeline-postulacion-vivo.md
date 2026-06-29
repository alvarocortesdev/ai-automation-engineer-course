---
ejercicio_id: track-0/pipeline-postulacion-vivo
fase: track-0
sub_unidad: "T0.2"
version: 1
---

# Rúbrica — Monta tu pipeline de postulación vivo

> Rúbrica **analítica** para un ejercicio de **diseño/estrategia**. Lo que se evalúa es el **criterio**:
> que el reencuadro sea genuino, que los roles sean stretch de verdad, que la tabla **instrumente un
> funnel** (no sea una libreta) y que el loop lea el funnel **en agregado**. No hay una única respuesta
> correcta: los 5 roles del alumno serán distintos a cualquier ejemplo. Lo que separa un pipeline pensado
> de uno improvisado es que cada pieza tenga una razón medible detrás.

## Objetivos evaluados
> Copiados del contrato. Cada criterio mapea a uno o más.

- **O1** — Argumentar por qué se postula para **calibrar** y no para **conseguir** todavía.
- **O2** — Definir "stretch" y justificar el rango ~50-70% de match.
- **O3** — Diseñar un pipeline instrumentado por funnel + un loop de calibración que realimente el plan.

## Criterios y niveles

### C1 — Reencuadro genuino (calibrar vs conseguir) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | No hay reencuadro, o es la frase del enunciado copiada sin apropiársela. |
| **en-progreso** | Menciona "calibrar" pero el resto del documento traiciona el marco (trata cada rechazo como fracaso, o solo elige roles "seguros"). |
| **competente** | Reencuadro con palabras propias y coherente con el resto: postula a stretch y trata el rechazo como dato esperado. |
| **excelente** | Además articula el costo de oportunidad de NO calibrar (meses de feedback perdido) y lo usa para justificar postular desde el mes 2. |

### C2 — Definición de stretch y % de match calculado · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No define stretch, o los % de match están inventados sin conteo de requisitos. |
| **en-progreso** | Define stretch pero el % no surge de un conteo verificable, o elige roles seguros (~95%) o imposibles (~10%) y los llama stretch. |
| **competente** | Define un criterio de conteo (requisitos duros cumplidos vs faltantes) y los 5 roles caen en ~50-70% con el cálculo mostrado. |
| **excelente** | Distingue requisito "duro" de "nice-to-have" al contar, y justifica por qué un rol seguro da poca señal y uno imposible da señal falsa. |

### C3 — El mercado como temario (lectura de las ofertas) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No extrae requisitos repetidos, o lista uno por aviso sin agregar. |
| **en-progreso** | Lista requisitos pero sin frecuencia ni orden (no se ve qué se repite). |
| **competente** | Ordena los requisitos por frecuencia de aparición entre los 5 avisos (p. ej. "Docker 4/5"). |
| **excelente** | Usa ese ranking para anticipar un ajuste de estudio concreto (el requisito más repetido entra a la columna "Ajuste"). |

### C4 — Tabla instrumentada por funnel · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay tabla, o es una lista de "a qué postulé" sin etapa ni funnel. |
| **en-progreso** | Tabla con datos pero sin la columna **Etapa actual** mapeada al funnel; no se puede leer en qué punto se cae cada postulación. |
| **competente** | Tabla con `Etapa actual` ubicada en el funnel (postulé → screening → técnica → final) + gap + ajuste por fila. |
| **excelente** | Trata la tabla como telemetría: deja explícito que mirará **tasas de conversión por etapa**, no casos sueltos (hilo de observabilidad). |

### C5 — Loop de calibración agregado · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay loop, o el "loop" es "veré qué pasa con cada postulación". |
| **en-progreso** | Describe ajustar, pero caso por caso, sin lectura agregada del funnel. |
| **competente** | Lee el funnel completo: responde "si 0 de 5 pasan el screening, ajusto X arriba del funnel porque aún no me evaluaron técnicamente". |
| **excelente** | Cierra el ciclo de vuelta al plan de estudio (el gap repetido reordena una fase del roadmap) y nombra el inglés como gap medible si aparece (hilo inglés). |

## Errores típicos a marcar
- **Tabla-libreta:** registra a qué postuló sin la etapa del funnel → no puede leer el sistema en agregado.
- **Roles seguros disfrazados de stretch:** elige avisos donde cumple ~95% (da poca señal) y los llama stretch.
- **% de match inventado:** sin conteo de requisitos cumplidos vs faltantes; el número no es verificable.
- **Loop caso por caso:** ajusta por una postulación aislada en vez de por lo que se repite (ruido vs señal).
- **Reencuadro de fachada:** dice "calibrar" pero el resto del documento revela mentalidad de "conseguir".
- (transversales) no trata la búsqueda como proyecto instrumentado (spec-driven/observabilidad ausentes); ignora el inglés aunque aparezca en los avisos.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Los "5 roles" son genéricos o inventados (sin empresa/link real, descripciones que suenan a plantilla).
- Tabla y loop impecables en forma pero el reencuadro y los % no calzan entre sí (texto generado sin criterio propio).
- Vocabulario de "funnel/conversión" sin poder explicar, sin notas, qué etapa evalúa qué.
- **Verificación sugerida:** pide que explique, sin notas, qué ajustaría si las postulaciones pasaran el screening pero cayeran todas en la técnica. Si diseñó de verdad, distingue ese caso del silencio masivo al instante.

## Feedback sugerido (graduado)
> Nunca reescribir el pipeline por el alumno.
- **Pista (nivel 1):** "Mira tu tabla: si tapas la columna de etapa, ¿podrías saber dónde se cae cada postulación? Esa columna es la que convierte la libreta en un funnel."
- **Pregunta socrática (nivel 2):** "Si 0 de 5 no pasan el screening, ¿el problema está en tu código o en algo anterior? ¿Qué etapa evalúa el screening, y por tanto qué deberías ajustar?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Tu loop ajusta caso por caso; eso te hace perseguir ruido. Reescríbelo para que decida según el gap que se **repite** en el funnel agregado, y que ese gap reordene una fase de tu plan de estudio."

## Conexión con el proyecto / capstone
- Este pipeline es la espina dorsal del track-0: alimenta los mocks (T0.3), reordena el portafolio (T0.5) y el CV (T0.7), y vuelve medible el gate de inglés (T0.1). El "capstone" del track es conseguir el trabajo, y este es su sistema de medición.
