---
ejercicio_id: fase-3/nestjs-recurso-tareas
fase: fase-3
sub_unidad: "3.10"
version: 1
---

# Rúbrica — Recurso de tareas en NestJS

> Rúbrica **analítica** atada a los `objetivos` del contrato. El corrector la usa con `INSTRUCCIONES-CORRECTOR.md`. No es una nota numérica: es un mapa de qué observar y cómo dar feedback. El ejercicio es de **profundización** (NestJS no es ruta crítica); el rigor se mide igual que en cualquier backend.

## Objetivos evaluados
- **O1** — Implementar un recurso REST en NestJS con módulo + controller + service inyectado por constructor (DI).
- **O2** — Validar la entrada con un DTO (clase) + class-validator y explicar por qué clase y no interface.
- **O3** — Mantener el dominio desacoplado del transporte (el service no habla HTTP); razonar `NotFoundException` vs excepción de dominio.

## Criterios y niveles

### C1 — Corrección (¿pasan los tests y se comporta el recurso?) · mapea: O1, O2
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | `npm test` no llega a verde; faltan métodos o el DTO sigue como interface (fallan los 3 tests de validación). |
| **en-progreso** | Pasan unos tests pero no todos: p. ej. el dominio funciona pero el DTO no valida (interface), o `obtener` no lanza `NotFoundException`. |
| **competente** | Los **7 tests** pasan: DI arma el controller, `crear`/`listar`/`obtener` se comportan, `obtener` inexistente lanza `NotFoundException`, y el DTO rechaza vacío/ausente y acepta válido. |
| **excelente** | Además, el código está limpio (tipos correctos, sin `any`), y `BITACORA.md` demuestra que entendió *por qué*, no solo *qué* hizo pasar. |

### C2 — Inyección de dependencias y separación de capas · mapea: O1, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | El controller hace `new TareasService()` (o mete la lógica en el controller); el service toca conceptos HTTP más allá de `NotFoundException`. |
| **en-progreso** | Inyecta el service pero mezcla responsabilidades (algo de lógica de negocio quedó en el controller, o parsea/valida a mano lo que el DTO debería). |
| **competente** | El service tiene la lógica y solo importa `Injectable`/`NotFoundException`; el controller solo orquesta HTTP e inyecta el service por constructor. |
| **excelente** | En `BITACORA.md` explica el desacople total (excepción de dominio + exception filter) y lo mapea al exception handler de FastAPI, aunque el ejercicio acepte `NotFoundException`. |

### C3 — Comprensión demostrada (BITACORA calza con el código) · mapea: O2, O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `BITACORA.md`, o no explica por qué el DTO es clase ni por qué se inyecta. |
| **en-progreso** | Responde las preguntas de forma genérica ("es buena práctica") sin la razón mecánica (runtime/metadata, testeo, desacople). |
| **competente** | Explica que la interface se borra en compilación → class-validator no puede leer decoradores en runtime; que inyectar permite sustituir en tests y comparte una sola instancia; y propone cómo desacoplar el dominio de HTTP. |
| **excelente** | Conecta explícitamente cada pieza con su equivalente FastAPI (DTO↔pydantic, DI↔Depends, NotFoundException↔HTTPException/handler) y nombra el `ValidationPipe` como lo que "enciende" la validación. |

## Errores típicos a marcar
- **DTO como `interface`** en vez de `class`: la validación se salta en silencio (los 3 tests del DTO fallan). Es EL error de esta lección.
- **`new TareasService()` dentro del controller**: anula la DI; el service deja de ser sustituible y compartible.
- **Lógica de negocio en el controller** (filtrar/crear inline) en vez de delegar al service.
- **El service lanzando muchos `HttpException`** o tocando `req`/`res`: acopla el dominio al transporte.
- **Olvidar `Number(id)`** en `obtener` (el `@Param` llega string) — si lo notan en código real, el `find` por `===` nunca coincide.
- (transversales) persigue "que pase el test" sin entender el porqué; no menciona el `ValidationPipe` como pieza que enciende la validación; confía en que "Nest valida solo".

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Código impecable con configuración avanzada (guards, interceptors, custom providers) que el ejercicio no pide y la lección no enseñó: sofisticación impropia del nivel.
- `BITACORA.md` que recita ventajas genéricas de NestJS pero no puede explicar por qué SU interface fallaría (si la hubiera dejado) ni qué hace el `ValidationPipe`.
- **Verificación sugerida:** pedir en voz alta "si cambio el DTO de class a interface, ¿qué tests fallan y por qué exactamente?" y "¿qué pasa si borro el `useGlobalPipes` de `main.ts`?". Quien implementó sabe responder; quien copió, no.

## Feedback sugerido (graduado)
> Ordenado de menos a más directo. **Nunca dar el código de la solución.**
- **Pista (nivel 1):** "Si los 3 tests del DTO fallan pero el dominio pasa, mira la **primera línea** de tu DTO: ¿`class` o `interface`?"
- **Pregunta socrática (nivel 2):** "¿Dónde existe un decorador `@IsString()` cuando el programa ya está corriendo? ¿Una interface de TypeScript existe en ese momento?"
- **Dirección concreta (nivel 3, solo tras intento real):** "Convierte el DTO en `class` con `@IsString()` + `@IsNotEmpty()`. Para la DI, el service se pide en el constructor (`private readonly tareasService: TareasService`), nunca con `new`. Explica en la bitácora el porqué de cada uno."

## Conexión con el proyecto / capstone
- Esta es la base del backend en la **ruta Node**: si el alumno hace un capstone alternativo en TS, este patrón (módulo/controller/service/DTO) es el esqueleto, y la decisión "FastAPI vs NestJS" se vuelve un ADR del Capstone F3.
