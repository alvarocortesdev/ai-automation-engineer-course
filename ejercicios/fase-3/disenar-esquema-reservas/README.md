# Ejercicio 3.1 — Diseña un esquema desde requisitos: reservas de coworking

> **Modalidad: diseño (a mano primero, sin IA).** Lo que se evalúa no es la sintaxis perfecta de SQL, sino tu **modelo**: que identifiques entidades, relaciones y claves correctas a partir de un requisito en prosa, y que sepas defender por qué tu esquema está normalizado. Es exactamente lo que mide una entrevista de backend frente a una pizarra.

## El requisito (tal como te lo daría un cliente)

> "Administro un coworking. Tengo **socios** (con nombre y email). Tengo **salas** (con nombre, capacidad de personas y un precio por hora). Un socio puede **reservar** una sala para un día y un bloque horario (hora de inicio y fin). Quiero saber qué reservas tiene cada socio y qué reservas tiene cada sala. Un socio puede tener muchas reservas; una sala se reserva muchas veces."

## Tu tarea (en este orden — Primero-Sin-IA, timebox 40–45 min)

1. **Identifica las entidades** y sus atributos. Decide el **tipo de dato** de cada columna (texto, entero, fecha, hora…).
2. **Identifica las relaciones** entre entidades (1:1, 1:N o N:M) y cómo se implementan: ¿dónde va la clave foránea?, ¿hace falta una tabla intermedia?
3. **Escribe el DDL** en `esquema.sql`: `CREATE TABLE` con clave primaria en cada tabla, claves foráneas declaradas con `REFERENCES`, y `NOT NULL` / `UNIQUE` / `CHECK` donde tenga sentido.
4. **Decide los índices** y escríbelos (`CREATE INDEX`), justificando cada uno con una consulta concreta del requisito.
5. En `NOTAS.md`, escribe: el tipo de cada relación, **por qué tu esquema está en 3NF** (o dónde elegiste no estarlo y por qué), y qué consulta de lectura motivó cada índice.

> Hazlo primero a mano (papel o un borrador). El valor está en *pensar el modelo*, no en que el SQL compile. Solo después puedes verificar la sintaxis.

## Qué entregar (deja estos archivos en esta carpeta)

- `esquema.sql` — tu DDL completo (tablas + índices). Parte del starter incluido.
- `NOTAS.md` — tu justificación: relaciones, normalización (con el vocabulario de la lección: atómico, dependencia de la clave, anomalías) e índices.

## Criterios de "hecho"

- [ ] Cada tabla tiene clave primaria; cada relación se implementa con una FK declarada (`REFERENCES`).
- [ ] No hay datos duplicados que debieran vivir en otra tabla (el email del socio aparece **una sola vez** en todo el esquema).
- [ ] `NOTAS.md` justifica la normalización con el lenguaje de la lección, no con "porque sí".
- [ ] Cada índice responde a una consulta concreta que nombras; no indexaste "por si acaso".
- [ ] Puedes explicar, sin notas y en voz alta, qué anomalía evitas al separar `socios` de `reservas`.

## Pedir corrección

Cuando termines, pídele a tu IA:

> "Corrige `ejercicios/fase-3/disenar-esquema-reservas/` usando el framework de `.ai/`. Sigue `INSTRUCCIONES-CORRECTOR.md`."

El corrector revisará tu **modelo y tu razonamiento** (relaciones, normalización, índices), no solo si el SQL es sintácticamente válido.
