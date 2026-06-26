---
ejercicio_id: fase-2/que-no-testear-y-umbral
fase: fase-2
sub_unidad: "2.9"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala sólo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6). Es un ejercicio de juicio: hay un rango amplio de respuestas defendibles; lo que sigue es el razonamiento de referencia, no la única respuesta correcta.

# Solución de referencia — Qué NO testear + tu política de umbral honesta

## Parte 1 — Clasificación de referencia

| Caso | Decisión | Por qué |
|---|---|---|
| **A** Getter trivial | **no-testear** | Sin lógica: solo devuelve un atributo. Un test aquí no atrapa ningún bug interesante y se rompe si renombras el campo. Costo > valor. |
| **B** Wrapper de `requests` | **no-testear** unitario | No tiene lógica propia; reenvía a `requests`. Un test unitario que mockea `requests` prueba el mock, no tu código. A lo sumo, un **test de contrato/integración** que verifique que el endpoint externo responde con el shape esperado. |
| **C** Cálculo de IVA | **testear-unitario** (centro) | Pura lógica de negocio con ramas (`basico`/`alcohol`/resto) y aritmética. Puede fallar de formas interesantes (tasa equivocada, rama olvidada). Aquí va el mutation testing. |
| **D** Logging | **no-testear** | Infraestructura sin comportamiento de negocio. Afirmar "se logueó tal string" acopla el test al texto del log; se rompe al editarlo sin atrapar nada. |
| **E** DTO autogenerado | **no-testear** | No es *tu* código: se regenera del contrato. Testearlo prueba al generador. Se cubre indirectamente al testear C/F que lo consumen. |
| **F** Parser de fechas propio | **testear-unitario** | Lógica propia con **bordes** (días/meses inválidos, formato malo) y manejo de errores (`ValueError`). Justo lo que falla de forma interesante; ideal para casos de borde + mutation. |
| **G** `if __name__ == "__main__"` | **no-testear** | Bloque de arranque/infra; no contiene lógica testeable de forma útil. |
| **H** Endpoint orquestador | **testear-en-integración** | El valor está en que los tres servicios cooperen (stock → pago → notificación) y en el manejo de fallas reales. Un test unitario con los tres mockeados solo verifica que llamaste a los mocks; no prueba el flujo. |

**Regla de fondo:** testea lo que (1) tiene lógica que puede equivocarse y (2) es tu
responsabilidad. No testees unitariamente lo trivial, lo de terceros ya probado, ni la
infraestructura. El esfuerzo se concentra en **C** y **F**; el sistema se valida en **H**
con integración.

## Parte 2 — Política de calidad de referencia

Una política honesta (≈1 página) cubre cuatro puntos:

1. **Coverage NO es un gate de objetivo.** Lo usamos como **diagnóstico**: revisamos los
   módulos con coverage bajo o **0%** (señal de "esto no tiene ni un test") y los
   atendemos. No celebramos el 90% ni ponemos "≥80% o no mergeas": ese número se infla
   con tests que ejecutan sin afirmar (Goodhart: la medida deja de medir cuando se
   vuelve objetivo). Coverage es un piso, no un techo.

2. **La fuerza se mide con mutation score**, no con coverage. Sobre la **lógica crítica**
   (cálculos, parsing, reglas de negocio: casos C y F del ejercicio) corremos `mutmut`
   y exigimos un mutation score alto *sobre ese código*, no sobre todo el repo.

3. **Cadencia por costo.** El mutation testing es caro (corre la suite por cada mutante),
   así que **no** va en cada push. Va: (a) sobre el **diff** del PR (solo el código
   cambiado) como gate rápido, y (b) **nightly** completo sobre los módulos críticos,
   con reporte. El costo de la métrica de calidad se presupuesta, igual que el de los
   evals de IA en la Fase 6.

4. **Exclusiones explícitas y justificadas.** Sacamos de la medición el código
   **generado** (DTOs del cliente OpenAPI), la **infraestructura** (logging, `__main__`,
   wrappers sin lógica) y el código de terceros. No es trampa: no es *nuestra* lógica;
   medirlo infla el número sin medir calidad real. La exclusión se documenta (en
   `setup.cfg`/`pyproject.toml` para coverage, en la config de `mutmut`), no se asume.

> Resumen en una frase defendible en entrevista: *"Coverage me dice qué no toqué —lo uso
> para encontrar agujeros—; el mutation score me dice si lo que toqué lo pruebo de verdad
> —ese es mi gate, y solo sobre la lógica que importa, por costo—."*

## Puntos resbalosos (donde el corrector debe mirar)
1. **B y H son los discriminantes.** Un alumno que testea el wrapper o el orquestador
   unitariamente (mockeando todo) no entendió la diferencia entre "ejecuté el código" y
   "verifiqué comportamiento real". Es el error más informativo.
2. **El DTO (E) "se testea" indirectamente.** Si el alumno dice "lo testeo al testear C/F
   que lo usan", es una respuesta **excelente**, no un error.
3. **Matiz de B aceptable.** Proponer un *contract test* para B (que el shape externo no
   cambió) es válido y maduro; no es lo mismo que un unit test con mock.
4. **Política sin costo = incompleta.** Si la política manda mutation testing en cada PR
   completo, falló O3 aunque el resto esté bien.

## Rango de soluciones aceptables
- Las clasificaciones admiten matices: B como "contract/integración mínimo" en vez de
  "no-testear" es igual de válido; C/F como centro unitario es innegociable.
- La política puede optar por **mantener** un gate de coverage *bajo* (p. ej. "el coverage
  no puede *bajar* respecto al baseline") siempre que argumente que lo usa como red
  anti-regresión y no como objetivo de calidad. Eso es defendible y maduro.
- No se exige un formato concreto; se exige que los cuatro puntos (diagnóstico vs meta,
  mutation sobre lógica crítica, cadencia por costo, exclusiones justificadas) estén
  argumentados, no solo enunciados.
