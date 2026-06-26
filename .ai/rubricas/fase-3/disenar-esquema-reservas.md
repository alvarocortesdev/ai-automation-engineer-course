---
ejercicio_id: fase-3/disenar-esquema-reservas
fase: fase-3
sub_unidad: "3.1"
version: 1
---

# Rúbrica — Diseña un esquema desde requisitos: reservas de coworking

> Rúbrica **analítica** atada a los `objetivos` del contrato. Lo que se evalúa es el **modelo** y su
> **justificación**, no que el SQL compile. Un alumno puede tener DDL sintácticamente perfecto y un
> modelo equivocado (datos duplicados, relación mal implementada), o un modelo correcto con sintaxis
> imperfecta. La rúbrica prioriza el modelo y el razonamiento.

## Objetivos evaluados
- **O1** — Diseñar el esquema desde la prosa: entidades, atributos, relaciones, traducidas a tablas con PK/FK.
- **O2** — Justificar la normalización hasta 3NF (anomalías evitadas) y, si desnormaliza, hacerlo consciente.
- **O3** — Elegir índices defendiendo el trade-off lectura/escritura contra consultas concretas.

## Criterios y niveles

### C1 — Modelo de entidades y relaciones (corrección del diseño) · mapea: O1
| Nivel | Cómo se ve (observable) |
|---|---|
| **incompleto** | Falta una entidad (p. ej. no separa `salas`), o mete todo en una o dos tablas con datos repetidos. La relación socio–sala no está modelada con FK. |
| **en-progreso** | Tiene las tres tablas pero implementa mal la relación: FK en el lado equivocado, o crea una tabla intermedia "pura" sin notar que la reserva tiene atributos propios (fecha/horas). |
| **competente** | Tres tablas (`socios`, `salas`, `reservas`); `reservas` lleva `socio_id` y `sala_id` como FK declaradas más sus atributos de tiempo; PK en todas. Reconoce la relación como N:M resuelta por `reservas` (entidad con atributos). |
| **excelente** | Además modela detalles realistas defendibles: `CHECK (hora_fin > hora_inicio)`, `precio_hora` con `NUMERIC`/entero (no `FLOAT`), `email UNIQUE`, y comenta una posible restricción de solapamiento de reservas (aunque no la implemente). |

### C2 — Normalización y su justificación (NOTAS.md calza con el esquema) · mapea: O2
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay `NOTAS.md`, o el email/nombre del socio aparece duplicado en `reservas` (rompe 3NF) sin notarlo. |
| **en-progreso** | Esquema sin duplicación, pero `NOTAS.md` no explica *por qué* (dice "está normalizado" sin nombrar dependencias ni anomalías). |
| **competente** | Esquema en 3NF y `NOTAS.md` lo justifica con el vocabulario correcto: cada atributo depende de la clave de su tabla; separar `socios` evita la anomalía de actualización del email. |
| **excelente** | Identifica explícitamente qué anomalía evita cada separación (inserción/actualización/borrado) y, si desnormaliza algo (p. ej. nada aquí, pero podría discutir un `precio_total` cacheado), lo marca como decisión consciente con su trade-off. |

### C3 — Índices y trade-off (criterio de ingeniería) · mapea: O3
| Nivel | Cómo se ve |
|---|---|
| **incompleto** | No hay índices, o indexa todas las columnas "por si acaso" sin justificar. |
| **en-progreso** | Crea índices pero no los ata a una consulta concreta, o indexa la PK (que ya viene indexada) creyendo que aporta. |
| **competente** | Indexa `reservas.socio_id` y `reservas.sala_id` (las FK) y justifica cada uno con una de las dos consultas del requisito ("reservas por socio", "reservas por sala"). |
| **excelente** | Reconoce que cada índice penaliza las escrituras y lo dice; menciona que las FK son candidatas naturales porque se filtra/une por ellas, y propone medir con `EXPLAIN` (puente a 3.3). |

## Errores típicos a marcar
- **Duplicar el email/nombre del socio en `reservas`** (o el nombre de la sala): rompe 3NF, abre la anomalía de actualización. Es el error central.
- **Tabla intermedia "pura"** para socio–sala ignorando que la reserva tiene fecha/horas: la reserva ES la entidad, no un simple cruce.
- **FK no declarada** (solo un `socio_id INTEGER` suelto sin `REFERENCES`): no hay integridad referencial.
- **`FLOAT` para `precio_hora`**: pérdida de precisión en dinero; debe ser `NUMERIC`/`DECIMAL` o entero.
- **Indexar todo** o indexar la PK: muestra que no entendió el costo de escritura del índice.
- (transversales) `NOTAS.md` que no nombra ni una anomalía concreta; índices sin consulta que los motive; falta de un solo trade-off defendible.

## Señales de dependencia-IA
> Describir sin acusar; proponer verificación.
- Esquema impecable y sobre-sofisticado (triggers, particiones, tipos exóticos) impropio de una primera lección de SQL, pero `NOTAS.md` no puede explicar por qué `reservas` necesita dos FK.
- `NOTAS.md` que recita la definición de 1NF/2NF/3NF de manual pero no la aplica al caso concreto (no dice qué columna habría roto cuál forma).
- **Verificación sugerida:** pedir, en voz alta, "si guardaras el email del socio dentro de `reservas`, ¿qué problema concreto tendrías cuando el socio cambie su email?". Quien diseñó entendiendo responde con la anomalía de actualización; quien dependió de la IA se traba.

## Feedback sugerido (graduado)
> Nunca dar el esquema de la solución antes de que el alumno cierre su intento.
- **Pista (nivel 1):** "¿Cuántas 'cosas' con identidad propia hay en el requisito? Cuéntalas: ¿un socio existe sin reservas? ¿una sala existe sin reservas? Si la respuesta es sí, cada una quiere su tabla."
- **Pregunta socrática (nivel 2):** "La reserva conecta un socio con una sala, pero ¿tiene datos propios (fecha, horas) que no son ni del socio ni de la sala? Si los tiene, ¿dónde viven esos datos? ¿Y dónde apuntan las dos FK?"
- **Dirección concreta (nivel 3, solo tras intento real):** "El patrón es N:M con atributos: `reservas(socio_id FK, sala_id FK, fecha, hora_inicio, hora_fin)`. El email del socio vive solo en `socios`. Reescribe `NOTAS.md` nombrando, para cada tabla separada, qué anomalía evitas."

## Conexión con el proyecto / capstone
- Este esquema es el tipo de modelo de datos sobre el que se monta el **Capstone F3 — API de producción**. Modelar bien las entidades y relaciones aquí es lo que evita arrastrar un mal modelo (y datos huérfanos) hasta producción; los índices que elijas son parte del "hecho significa" de rendimiento del capstone.
