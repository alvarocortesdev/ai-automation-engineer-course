---
ejercicio_id: fase-3/disenar-esquema-reservas
fase: fase-3
sub_unidad: "3.1"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diseña un esquema desde requisitos: reservas de coworking

## Respuesta canónica (esquema en 3NF)

```sql
CREATE TABLE socios (
    id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre  TEXT    NOT NULL,
    email   TEXT    NOT NULL UNIQUE
);

CREATE TABLE salas (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre        TEXT    NOT NULL,
    capacidad     INTEGER NOT NULL CHECK (capacidad > 0),
    precio_hora   NUMERIC(10, 2) NOT NULL CHECK (precio_hora >= 0)
);

CREATE TABLE reservas (
    id           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    socio_id     INTEGER NOT NULL REFERENCES socios(id),
    sala_id      INTEGER NOT NULL REFERENCES salas(id),
    fecha        DATE    NOT NULL,
    hora_inicio  TIME    NOT NULL,
    hora_fin     TIME    NOT NULL,
    CHECK (hora_fin > hora_inicio)
);

-- Índices: las dos consultas del requisito filtran por estas FK.
CREATE INDEX idx_reservas_socio ON reservas (socio_id);
CREATE INDEX idx_reservas_sala  ON reservas (sala_id);
```

## Razonamiento paso a paso

1. **Entidades.** Tres "cosas" con identidad propia: `socios`, `salas`, `reservas`. Prueba: un socio existe aunque no tenga reservas; una sala existe aunque nadie la reserve. Ambas piden tabla propia. La reserva también es una entidad porque tiene atributos propios (fecha, horas) y existencia propia (un evento).

2. **Relaciones.** Socio–sala es **N:M** (un socio usa muchas salas; una sala la usan muchos socios). No se puede poner una FK en `socios` ni en `salas` porque ambos lados son "muchos". Se resuelve con `reservas`, que parte el N:M en dos relaciones 1:N: `socios 1--N reservas` y `salas 1--N reservas`. La clave es que `reservas` **no es una tabla de unión pura**: tiene atributos propios (fecha, hora_inicio, hora_fin), así que es una entidad por derecho propio con dos FK.

3. **Claves.** PK sustituta `id` en cada tabla (no cambia, sin significado de negocio). `email UNIQUE` en `socios` (clave natural candidata, pero usamos `id` como PK porque el email podría cambiar). Las FK `socio_id` y `sala_id` declaradas con `REFERENCES` dan integridad referencial: no se puede reservar para un socio o sala inexistente.

4. **Tipos.** `DATE` y `TIME` separados (permiten filtrar por fecha y por rango horario; nunca texto). `precio_hora` con `NUMERIC` (jamás `FLOAT` para dinero). `capacidad` entero positivo (`CHECK`).

5. **Normalización (lo que mide NOTAS.md).** Está en 3NF:
   - **1NF:** todos los valores atómicos (no hay "lista de salas" en una celda).
   - **2NF/3NF:** ningún atributo no-clave depende de otra cosa que no sea la clave de su tabla. El `email` del socio vive **solo** en `socios`; el `precio_hora` vive **solo** en `salas`. Si hubiéramos puesto `email` o `nombre_sala` en `reservas`, romperíamos 3NF y abriríamos la **anomalía de actualización** (cambiar el email del socio obligaría a tocar todas sus reservas).

6. **Índices.** `socio_id` y `sala_id` en `reservas` porque las dos consultas explícitas del requisito ("reservas de cada socio", "reservas de cada sala") filtran/unen por ahí. Las FK son candidatas naturales a índice. Cada índice acelera esas lecturas a costa de hacer un poco más lentos los `INSERT` de reservas —trade-off aceptable porque se lee mucho más de lo que se escribe. La PK ya viene indexada, no se indexa de nuevo.

## Puntos resbalosos (donde el corrector debe mirar)

1. **Email/nombre duplicado en `reservas`** → rompe 3NF, anomalía de actualización. El error #1.
2. **Tabla intermedia "pura"** (solo `socio_id` + `sala_id`, sin fecha/horas) → no modela la reserva como evento; pierde los atributos del requisito.
3. **FK sin declarar** (`socio_id INTEGER` sin `REFERENCES`) → sin integridad referencial; admite reservas huérfanas.
4. **`precio_hora` como `FLOAT`** → pérdida de precisión monetaria.
5. **Indexar todo / indexar la PK** → no entendió el costo de escritura del índice.
6. **PK natural frágil** (usar `email` como PK) → defendible, pero hay que notar que el email puede cambiar y eso es problemático para una PK; la sustituta es preferible.

## Rango de soluciones aceptables

- Usar `SERIAL` en vez de `GENERATED ALWAYS AS IDENTITY` es aceptable (forma antigua de Postgres, mismo efecto).
- Usar `TIMESTAMP` único en vez de `DATE` + `TIME` separados para el inicio/fin es **válido y hasta más robusto** (evita ambigüedad de medianoche); no penalizar, valorar si lo justifica.
- Una PK compuesta `(socio_id, sala_id, fecha, hora_inicio)` en `reservas` en vez de `id` sustituto es aceptable si el alumno argumenta unicidad; tiene el inconveniente de FK más pesadas, pero no es incorrecto.
- Modelar una restricción de **no solapamiento** de reservas (con `EXCLUDE` de Postgres o validación en la app) es nivel **excelente**; no se exige.
- `NOTAS.md` vale con cualquier redacción que (a) nombre el tipo de cada relación, (b) explique la normalización con al menos una anomalía concreta, y (c) ate cada índice a una consulta. El nivel **excelente** menciona el costo de escritura del índice y `EXPLAIN`.
- **Variante de control para detectar dependencia-IA:** pedir que explique qué pasaría con la complejidad de "listar las reservas del socio 42" si `reservas.socio_id` **no** estuviera indexado. Quien entendió dice "escaneo de toda la tabla, O(n)"; quien no, se traba.
