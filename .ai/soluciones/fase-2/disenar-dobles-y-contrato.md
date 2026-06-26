---
ejercicio_id: fase-2/disenar-dobles-y-contrato
fase: fase-2
sub_unidad: "2.8"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).

# Solución de referencia — Diseña la estrategia de dobles y decide dónde va un contrato

## 1. Tabla de dobles (respuesta canónica)

| Colaborador | Double | Por qué |
|---|---|---|
| `Reloj` | **Stub** | Solo necesito que `ahora()` devuelva una hora **fija** para que el test sea determinista. No me importa si lo llamaron ni cuántas veces. Provee una entrada indirecta enlatada. |
| `RepositorioDeReembolsos` | **Fake** (en memoria) | Quiero comprobar que el reembolso **quedó guardado**. Un fake funcional (lista/dict en memoria) me deja verificar el **estado real** (`repo.por_cobro(...)` lo devuelve), más robusto al refactoring que mockear `guardar`. |
| `EnviadorDeEmail` | **Mock / Spy** | El envío SMTP **no deja estado consultable** desde el test. La única forma honesta de afirmar "se envió el comprobante" es **verificar la interacción** (`enviar_comprobante` se llamó una vez con el reembolso correcto). |
| `PasarelaDePago` | **Stub** (camino feliz) / **Mock** (caso de rechazo) | Camino feliz: stub que devuelve `ResultadoPasarela(estado="aprobado")`. Caso de borde: mock para afirmar que **no se llamó** cuando el reembolso se rechaza por regla de negocio. *Además* merece un **contract test** (sección 4). |

> No hay un `dummy` natural en este SUT (los cuatro colaboradores se usan). Mencionarlo como categoría
> ("sería un argumento exigido por la firma pero no tocado en este camino") es correcto; inventar uno
> forzado, no.

## 2. Dos casos en Given-When-Then

**Caso feliz — reembolso aprobado se persiste y se notifica**
```
Given un cobro "cob-1" de 5000 centavos y una pasarela que aprobará el reembolso con tx "rf-9"
When  reembolso 5000 centavos de ese cobro al email "ana@ej.cl"
Then  el reembolso queda guardado en el repositorio con monto 5000 y tx "rf-9"
 And  se envía el comprobante a "ana@ej.cl" exactamente una vez
```

**Caso de borde — reembolso mayor que el cobro original se rechaza y no toca la pasarela**
```
Given un cobro "cob-1" cuyo monto original fue 5000 centavos
When  intento reembolsar 8000 centavos (más de lo cobrado)
Then  se lanza ReembolsoRechazado
 And  la pasarela NUNCA es llamada (la regla de negocio corta antes de tocar la red)
 And  nada se guarda ni se envía email
```

## 3. Estado vs. interacción (clasificación de los casos)

- **Caso feliz:** verificación **mixta**, dominada por **estado** para el repo (`repo.por_cobro("cob-1")`
  devuelve el reembolso esperado → verifico el resultado real) e **interacción** para el email
  (`enviar_comprobante.assert_called_once_with(...)` → no hay estado que mirar).
- **Caso de borde:** verificación de **interacción negativa**: `pasarela.reembolsar.assert_not_called()`
  y `repo` vacío. Lo que importa aquí no es un valor devuelto sino que el SUT **cortó antes** de tocar
  los colaboradores externos. Es la clase de aserción que solo un spy/mock puede hacer.

> Esbozo de los tests (referencia, no se exige código al alumno):
> ```python
> from unittest.mock import Mock
>
> def test_reembolso_aprobado_persiste_y_notifica():
>     pasarela = StubPasarela(estado="aprobado", id_transaccion="rf-9")
>     emailer = Mock()
>     repo = RepoFake()
>     servicio = ServicioDeReembolsos(pasarela, RelojStub("2026-06-26T10:00:00Z"), emailer, repo)
>
>     servicio.reembolsar("cob-1", 5000, monto_cobro_original=5000, email="ana@ej.cl")
>
>     guardado = repo.por_cobro("cob-1")           # ESTADO
>     assert guardado.monto == 5000 and guardado.id_transaccion == "rf-9"
>     emailer.enviar_comprobante.assert_called_once()   # INTERACCIÓN
>
> def test_reembolso_excesivo_se_rechaza_sin_tocar_la_pasarela():
>     pasarela = Mock()
>     servicio = ServicioDeReembolsos(pasarela, RelojStub("..."), Mock(), RepoFake())
>     with pytest.raises(ReembolsoRechazado):
>         servicio.reembolsar("cob-1", 8000, monto_cobro_original=5000, email="ana@ej.cl")
>     pasarela.reembolsar.assert_not_called()      # INTERACCIÓN NEGATIVA
> ```

## 4. El contrato: por qué la `PasarelaDePago` y no otro

- **Cuál:** la `PasarelaDePago`. Es la única frontera **HTTP hacia un servicio que despliega otro equipo**.
  El `Reloj`, el `Repo` y el `EnviadorDeEmail` son dependencias del mismo proceso (o infraestructura que
  tú controlas): un fake/stub basta. El contrato es para acoplamientos entre **servicios independientes**.
- **Qué falla un mock que un contrato previene:** tu `StubPasarela`/`Mock` codifica **tu suposición** de la
  respuesta del banco (`{"id_transaccion": ..., "estado": "aprobado"}`). Si el equipo de la pasarela
  renombra `id_transaccion` a `transaction_id`, tu mock **sigue verde** (lo escribiste tú), tus tests
  pasan, y tu cliente revienta en runtime al leer un campo que ya no existe. El mock no sabe nada de la
  realidad del otro lado.
- **Consumer / provider:** tú (el `ServicioDeReembolsos`) eres el **consumer**; el equipo de la pasarela es
  el **provider**. En *consumer-driven contracts*, el consumer declara qué espera y eso se guarda como el
  *pact*.
- **Pipelines:** el pact se **genera en el CI del consumer** (al correr el test de contrato, que produce el
  archivo). El **provider lo verifica en SU CI** contra su API real: si rompe el contrato, su build falla
  **antes** de desplegar. Así ambos lados se prueban **por separado**, sin levantar todo el stack — que es
  justo lo que un test de integración end-to-end exigiría, y por eso el contrato escala a muchos servicios.
- (Detalle de nivel excelente) en Pact se usa `match.string(...)` / matchers para afirmar la **forma**
  (existe `id_transaccion`, es un string), no el valor exacto: el contrato verifica estructura, no datos.

## Puntos resbalosos (donde el corrector debe mirar)
1. **"Mock para todo":** el alumno asigna mock al reloj y al repo. Señalar que el reloj solo necesita un
   valor (stub) y el repo se prueba mejor por estado (fake).
2. **Contract test para el repo/reloj:** error de alcance. El contrato es para fronteras entre servicios
   desplegados por separado, no para dependencias internas.
3. **Olvidar la interacción negativa** en el caso de borde (`assert_not_called`). Sin ella, el test no
   prueba que la regla de negocio cortó *antes* de tocar la red.
4. **Confundir contract test con integración:** si dice que "levanta ambos servicios", está describiendo
   integración end-to-end, no contract testing.

## Rango de soluciones aceptables
- Verificar el repo por **interacción** (`repo.guardar.assert_called_once_with(...)`) en vez de por estado
  (fake) es **aceptable** pero inferior: anótalo y explica por qué el fake + estado es más robusto.
- Usar un **spy** en lugar de **mock** para el email es equivalente (ambos verifican interacción); no penalizar.
- Para la `PasarelaDePago`, elegir mock también en el camino feliz (para afirmar `assert_called_once_with`)
  es válido si lo justifica; el stub es suficiente, el mock es defendible.
- **Variante de control para detectar dependencia-IA:** pedir que explique, en una frase y con *este*
  caso, qué pasa en producción si el provider renombra `id_transaccion` y solo hay un mock. Quien entendió
  conecta el concepto con el síntoma ("verde en tests, crash en runtime"); quien no, da una definición de libro.
