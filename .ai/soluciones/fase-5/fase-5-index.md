---
ejercicio_id: fase-5/fase-5-index
fase: fase-5
sub_unidad: "5.0"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Este ejercicio no
> tiene "respuesta correcta": lo que sigue es un **exemplar** y una lista de qué
> observar. Úsalo como vara de honestidad/realismo/verificabilidad, nunca como
> plantilla a copiar (ver `.ai/soluciones/README.md` y
> `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diagnóstico de Fase 5 y plan de ruta a producción

## Respuesta canónica
**No existe una respuesta única.** Una entrega `competente` es cualquier conjunto
de tres archivos **honesto, concreto y verificable**. La calidad se mide por
proceso (autoevaluación + planificación + verificabilidad), no por contenido
específico.

## Qué constituye una entrega correcta (por archivo)

### `diagnostico.md` — exemplar (alumno cero real en DevOps)
Tabla con las 8 sub-unidades de ruta-crítica. En un cero real, lo esperable es
mayoría de `nuevo` con quizá algún `lo reconozco`. La señal de calidad es la
**razón por fila** y la prueba "¿podría resolverlo sin notas ahora?".

| Sub-unidad | Nivel | Por qué (ejemplo) |
|---|---|---|
| 5.1 Docker a fondo | nuevo | Corrí contenedores ajenos, nunca escribí un Dockerfile multi-stage. |
| 5.2 12-factor app | nuevo | No conozco el manifiesto; hardcodeo config a veces. |
| 5.3 CI/CD GitHub Actions | lo reconozco | Vi workflows, nunca escribí uno de cero. |
| 5.4 Gates de seguridad / supply chain | nuevo | Nunca configuré SCA, secret-scanning ni SBOM. |
| 5.5 Cloud troncal | lo reconozco | Tengo cuenta cloud, pero no domino IAM ni serverless. |
| 5.8 Costos cloud | nuevo | Nunca estimé costo por request. |
| 5.9 Despliegue | lo reconozco | Desplegué algo en Vercel, no contenedores con dominio. |
| 5.10 Observabilidad | nuevo | Uso `print`/logs sueltos; no sé qué es una traza ni un correlation ID. |

> Para un perfil **con experiencia oxidada**, más `lo reconozco` y algún `lo sé
> hacer sin notas` es válido — pero solo si lo puede defender. La trampa a
> detectar: "lo sé hacer" en algo que solo *usó* (clásico: confundir
> `docker compose up` con saber escribir el Dockerfile, o "usé Compose" con
> "configuré un gate de seguridad en CI").

### `plan-fase-5.md` — exemplar
Un plan creíble + un orden de apilado coherente, p. ej.:
- **Mar/Jue 20:00–20:45** (2 bloques × 45 min) + **Dom 10:00–12:00** (sesión larga).
- **Ritual de repaso:** cada sesión arranca con 5 min reescribiendo de memoria lo
  anterior; los domingos, repaso de la semana; re-repaso una semana después de
  cerrar la fase (ya en F6).
- **Orden de apilado sobre la app de F3/F4:** (1) `Dockerfile` multi-stage de la
  API; (2) extraer config a variables de entorno (12-factor); (3) workflow de CI
  que corre lint + tests; (4) sumar gates: SCA + secret-scanning + SBOM que rompen
  el build; (5) desplegar contenedor con dominio (homelab + Cloudflare Tunnel, o
  cloud); (6) instrumentar logs estructurados + correlation IDs + una traza con
  OpenTelemetry.
- **Usuarios reales (≥3):** nombrados — p. ej. pareja, un amigo y un colega; cómo
  los invitará y qué les pedirá que hagan.

Señal de calidad: **día/hora concretos**, **ritual de repaso explícito** y un
**orden donde cada capa depende solo de las anteriores**, terminando en usuarios
reales + observabilidad. No "estudiaré ~10 h semanales de DevOps".

### `definicion-de-listo.md` — exemplar
Los 7 puntos del DoD del Capstone F5, cada uno con una **evidencia abrible**:

1. **Spec + ADRs** → link a `SPEC.md` y a `docs/adr/` en el repo.
2. **Tests verdes + lint en CI** → link al run de GitHub Actions en verde.
3. **Seguridad en el pipeline** → captura del job de SCA/secret-scanning fallando ante un hallazgo y bloqueando el merge; el SBOM generado como artefacto.
4. **Observabilidad** → captura de una **traza** con su **correlation ID** atravesando la petición; el formato de los logs estructurados.
5. **Demo que corre + ≥3 usuarios reales** → la URL pública (no `localhost`) y los nombres/uso de los 3 usuarios.
6. **README en inglés + write-up de trade-offs** → link al README y al write-up.
7. **Conventional Commits** → muestra del historial (`git log`) con el formato.

La señal de calidad: cada punto es algo que el corrector podría **abrir y ver**,
no una promesa ("tendré...").

## Puntos resbalosos (donde el corrector debe mirar)
1. **Sobreconfianza** en el diagnóstico, sobre todo confundir "usé una herramienta"
   con "sé construir con ella sin notas". Verificación: que defienda una fila en voz alta.
2. **Orden de apilado roto:** deploy/CI antes de empaquetar o de hacer configurable
   la app. Es justo el malentendido que la fase corrige.
3. **Plan irreal o sin *spacing*:** bloques que no caben; ausencia de ritual de repaso.
4. **DoD como intención, no evidencia:** "tendré observabilidad" en vez de "esta
   traza con este correlation ID".
5. **Sin usuarios reales:** olvidar el ≥3, que es la semilla de la "historia de
   falla en producción" del track de empleabilidad.

## Rango de soluciones aceptables
- Cualquier formato (tabla, listas, prosa breve) sirve si los tres entregables están
  y son honestos, concretos y verificables. No exigir la tabla exacta de arriba.
- Tanto un perfil cero como uno oxidado pueden ser `excelente`: se evalúa la
  **calidad del proceso**, no el nivel de partida.
- Un plan **modesto pero sostenible y bien ordenado** es preferible (y mejor
  calificado) que uno ambicioso e irreal.
- Un alumno con experiencia puede marcar que ya domina varias sub-unidades: válido y
  `excelente` **si** dice cómo lo va a *validar* (resolver un Primero-Sin-IA sin IA),
  no si las salta a ciegas.
