# 2.9 — Caza los mutantes que tu coverage no ve

**Fase:** Fase 2 — Ingeniería de software · **Lección:** `2.9` Coverage vs mutation/behavior
**Ruta:** crítica · **Timebox:** 40–45 min · **Modalidad:** código

## 🎯 Objetivo

Demostrar, con una función real, que **100% de line coverage no significa que tus
tests prueben algo**. Vas a (1) predecir a mano qué mutantes sobreviven una suite
aparentemente completa, (2) confirmarlo con `mutmut`, y (3) fortalecer la suite con
tests de borde que maten a los sobrevivientes — sin tocar el código fuente.

## 📋 Contexto

`descuento.py` calcula el porcentaje de descuento de un cliente (0..30) según sus
puntos y si es socio. Está **correcta** y `test_descuento.py` pasa en **verde** con
**100% de coverage**. Y aun así es débil. Este es exactamente el escenario que
enfrentarás en el **Capstone F2**, donde la calidad se mide por mutation score y
aserciones reales, no por el porcentaje de cobertura.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo**, a mano (timebox arriba). **Predice antes de ejecutar `mutmut`.**
2. Solo entonces, consulta las [docs de mutmut](https://mutmut.readthedocs.io/).
3. **Solo al final**, usa IA para *revisar y explicar* — no para *generar* tus tests.
4. Mañana, **reescríbelo de memoria**. Si no puedes, no lo aprendiste todavía.

## 🛠️ Instrucciones (en este orden estricto)

### Paso 0 — Confirma el punto de partida

```bash
uv run pytest                  # debe estar VERDE (4 tests)
uv run pytest --cov=descuento  # debe decir 100% (el dato que engaña)
```

Si no está verde, no sigas: algo está mal en tu entorno, no en el ejercicio.

### Paso 1 — PREDICE a mano (sin ejecutar mutmut)

Estos son los **7 mutantes candidatos**. Para cada uno, decide en `mutantes.md` si
**sobrevive** (todos los tests siguen verdes) o **muere** (algún test falla), y *por qué*:

| # | Mutación sobre `descuento.py` |
|---|---|
| M1 | línea `puntos >= 100 and es_socio` → `puntos > 100 and es_socio` |
| M2 | línea `puntos >= 100 and es_socio` → `puntos >= 100 or es_socio` |
| M3 | línea `puntos >= 100:` (la segunda) → `puntos > 100:` |
| M4 | línea `puntos >= 50:` → `puntos > 50:` |
| M5 | `return 30` → `return 31` |
| M6 | `return 10` → `return 11` |
| M7 | `return 0` → `return 1` |

> Razona como en la sección 4 de la lección: ¿qué **caso de entrada** distinguiría el
> código correcto del mutado? Si ningún test usa ese caso, el mutante sobrevive.

### Paso 2 — VERIFICA con la herramienta

```bash
mutmut run        # corre la suite contra cada mutante
mutmut browse     # inspecciona los sobrevivientes (TUI); 'q' para salir
```

`mutmut` generará **más** mutantes que los 7 de la tabla (muta cada número y
operador). No pasa nada: anota en `mutantes.md` cuáles de **tus** 7 predicciones
acertaste y cuáles no. Acertar o fallar la predicción es lo que de verdad aprendes.

### Paso 3 — FORTALECE la suite

Agrega a `test_descuento.py` los tests mínimos que **matan a los sobrevivientes**.
Vuelve a correr `mutmut run` hasta que no queden sobrevivientes (salvo los
**equivalentes**, si los hubiera: anótalos y explica por qué no se pueden matar).

> ⚠️ **No toques `descuento.py`.** No borres ni debilites los tests existentes; solo
> **agrega** los que falten. El line coverage seguirá en 100% antes y después: esa es
> justo la prueba de que el coverage nunca fue el problema.

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `mutantes.md` tiene tu predicción de los 7 mutantes **hecha antes** de correr `mutmut`.
- [ ] Identificaste que los sobrevivientes son los de **comparación en el borde** (`>=` → `>`).
- [ ] Tu suite fortalecida mata a todos los sobrevivientes no-equivalentes (lo confirmaste con `mutmut run`).
- [ ] No modificaste `descuento.py` ni debilitaste ninguna aserción.
- [ ] Puedes explicar **sin notas** por qué un test de borde sube el mutation score sin mover el coverage.

## 📦 Qué entregar (deja estos archivos en esta carpeta)

- `test_descuento.py` — tu versión fortalecida (todos los tests verdes).
- `mutantes.md` — tabla: **mutante → predicción (survive/killed) → resultado real → qué test lo mata**. Mínimo las 7 filas.

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

El patrón es siempre el mismo:

- Un mutante que cambia un **valor de retorno** o un **número** (`return 30` →
  `return 31`) lo mata cualquier test que afirme ese retorno exacto. Esos ya están
  cubiertos por la suite de partida (M5, M6, M7 mueren).
- Un mutante que cambia un **operador de comparación** (`>=` → `>`) solo lo mata un
  test en el **borde exacto** del umbral. Mira los umbrales (100 y 50) y pregúntate:
  ¿hay un test con `puntos == 100`? ¿con `puntos == 50`? No. Ahí sobreviven M1, M3, M4.
- El mutante `and` → `or` (M2) se mata con un caso donde las dos condiciones
  difieran: un no-socio con muchos puntos (la suite ya lo tiene → M2 muere).

Para matar a M1, M3, M4 agrega: `descuento(100, True) == 30`, `descuento(100, False) == 20`,
`descuento(50, False) == 10`. Pista, no solución: razona por qué cada uno mata su mutante.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio, **incluido `mutantes.md`**),
- la **rúbrica**: `.ai/rubricas/fase-2/cazar-mutantes-sobrevivientes.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-2/cazar-mutantes-sobrevivientes.md`
— no la mires antes de intentarlo de verdad.
