---
ejercicio_id: fase-3/refactor-hexagonal-tareas
fase: fase-3
sub_unidad: "3.9"
version: 1
---

# Rúbrica — Refactor: desacopla un endpoint en dominio + puerto + adaptadores

> Rúbrica **analítica** atada a los `objetivos`. Evalúa el código del directorio + `bitacora.md` con
> `pytest` en verde. Tres tests son objetivos: pureza del dominio (escaneo de imports), contrato de
> ambos adaptadores, y la regla de negocio por HTTP con `dependency_overrides`. Pero pasar los tests no
> basta: la `bitacora.md` debe mostrar que el alumno entiende **la dirección de las dependencias** y
> sabe **dónde NO** poner un puerto (criterio "light").

## Objetivos evaluados
- **O1** — Separar el endpoint acoplado en dominio puro + puerto (`Protocol`) + adaptador, con las
  dependencias apuntando hacia el dominio (el dominio no importa `fastapi` ni `sqlalchemy`).
- **O2** — Un puerto, dos adaptadores intercambiables (memoria + SQLAlchemy), cableados en FastAPI con
  `Depends`.
- **O3** — Testear la regla de negocio sin DB; justificar en un ADR dónde sí y dónde no va un puerto.

## Criterios y niveles

### C1 — Dominio puro y dirección de dependencias · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `dominio.py` importa `fastapi`/`sqlalchemy` (test de pureza en rojo), o la lógica sigue en el endpoint. |
| **en-progreso** | Movió algo de lógica al dominio pero deja `HTTPException`, el modelo ORM como entidad, o un import de infra colado. |
| **competente** | `test_dominio_sin_infra.py` en verde: dominio sin infra, entidad `Tarea` distinta de `TareaORM`, regla de negocio en `ServicioTareas`. |
| **excelente** | Lo anterior + explica en `bitacora.md` por qué la flecha apunta hacia el dominio y por qué la entidad no es el ORM (con el costo del mapeo asumido conscientemente). |

### C2 — Puerto y adaptadores intercambiables · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Un solo adaptador, o `test_contrato_repositorio.py` en rojo para alguno. |
| **en-progreso** | Ambos adaptadores existen pero uno falla el contrato (p. ej. `agregar` no asigna id, o devuelve `TareaORM`/dict en vez de `Tarea`). |
| **competente** | Ambos pasan el **mismo** contrato; el endpoint pide el puerto y `obtener_repo` es el único lugar que nombra el adaptador concreto. |
| **excelente** | Reconoce explícitamente que "el mismo test contra dos adaptadores" ES la prueba del beneficio, y anticipa el adaptador-LLM-falso de la Fase 6. |

### C3 — Testabilidad y cableado FastAPI · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | `test_api.py` en rojo, o el endpoint no traduce la excepción de dominio (500 en vez de 409). |
| **en-progreso** | Endpoint funciona pero la regla de negocio sigue en el endpoint, o el override no comparte instancia (estado no persiste). |
| **competente** | `dependency_overrides` inyecta el doble; el 6º request da 409; la regla vive en el dominio, no en el router. |
| **excelente** | Entiende y comenta por qué el override debe devolver la **misma** instancia del doble para que el estado persista entre requests. |

### C4 — Criterio "light" y comunicación (ADR) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | Sin `bitacora.md`, o "metí puertos a todo". |
| **en-progreso** | Justifica el puerto de persistencia pero no nombra nada que NO merezca puerto. |
| **competente** | Mini-ADR: por qué un puerto en la persistencia **y** un ejemplo de qué NO le puso puerto (y por qué sería sobre-ingeniería). |
| **excelente** | Conecta con testabilidad/punto-de-cambio como criterio general y menciona el riesgo de pattern-itis. |

## Errores típicos a marcar
- **Usar `TareaORM` como entidad de dominio:** acopla el dominio a SQLAlchemy por la puerta de atrás; el test de pureza puede pasar si no lo importa en `dominio.py`, pero el diseño filtra el ORM. Marca el mapeo faltante.
- **`HTTPException` en el dominio:** el dominio no sabe de HTTP; debe lanzar `LimiteTareasPendientes` y el endpoint traduce a 409.
- **Adaptador que devuelve `TareaORM` o un dict** hacia el dominio en vez de la entidad `Tarea` (lo caza `test_agregar_devuelve_entidad_de_dominio`).
- **`agregar` que no asigna id** (olvidó `flush()` en el adaptador SQLAlchemy).
- **Override con instancia nueva por request** (`lambda: RepositorioTareasMemoria()`): el estado no persiste y el límite nunca se alcanza.
- **Sobre-ingeniería:** un puerto por cada cosa, mappers innecesarios, una "capa de aplicación" que solo reenvía. El criterio "light" pide lo mínimo que paga.
- (transversal spec-driven) no escribir el ADR de la decisión arquitectónica.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código impecable con 6 carpetas y mappers genéricos (`BaseMapper[T]`) impropios del enunciado y del nivel: huele a plantilla de tutorial pegada, no a decisión.
- `bitacora.md` que repite "clean architecture / SOLID" sin poder decir en qué **dirección** apuntan las dependencias en SU código.
- No sabe explicar por qué el endpoint pide el puerto y no el adaptador.
- **Verificación sugerida:** pídele que, sin correr, prediga qué pasa si en `dominio.py` agrega `from sqlalchemy.orm import Session` (falla el test de pureza) y por qué eso rompe la arquitectura; y que señale qué pieza tendría que cambiar si mañana migrara de Postgres a un servicio externo (solo el adaptador + `obtener_repo`).

## Feedback sugerido (graduado)
> Nunca pegar el código de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "Corre `test_dominio_sin_infra.py`. Si la pureza falla, ¿qué import de infra quedó en `dominio.py`? Muévelo al adaptador que corresponde."
- **Pregunta socrática (nivel 2):** "¿Quién debería saber qué es un status code 409: el `ServicioTareas` o el endpoint? Si la regla de negocio lanza `HTTPException`, ¿podrías reusar ese servicio desde una CLI o un test sin arrastrar FastAPI?"
- **Dirección concreta (nivel 3, sólo tras intento real):** "El servicio solo debe hablar con el puerto: `if self._repo.contar_pendientes() >= MAX_PENDIENTES: raise LimiteTareasPendientes(...)`. El adaptador SQLAlchemy traduce `TareaORM`→`Tarea` y usa `flush()` para el id. El endpoint envuelve `crear_tarea` en `try/except` y mapea a 409. Repasa 4.4–4.8 antes de la referencia."

## Conexión con el proyecto / capstone
- Es la columna del capstone: cada regla de negocio sobre datos persistidos vive en un servicio testeable sin DB, detrás de un puerto. El mismo patrón de `dependency_overrides` hace los tests de endpoint rápidos y deterministas, y prepara el adaptador-LLM de la Fase 6. La decisión "puerto sí / puerto no" va en un ADR.
