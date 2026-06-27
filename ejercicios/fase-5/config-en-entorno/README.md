# Ejercicio 5.2 — Config en el entorno (Factor III)

> **Modalidad: código (sin IA primero).** El Factor III es el que más se incumple y el de mayor riesgo: un secreto en el código viaja al repo y a la imagen. Aquí conviertes config hardcodeada en config leída del entorno, con validación y arranque-que-falla-rápido. Es el patrón que usarás en cada backend de aquí en adelante.

**Fase:** Fase 5 — DevOps, Cloud y despliegue · **Lección:** `5.2` 12-factor app
**Ruta:** crítica · **Timebox:** 35–40 min

## 🎯 Objetivo

Refactorizar un módulo de config **hardcodeada** (URL de base, clave de API, puerto) a una clase `Settings` de `pydantic-settings` que lea del entorno con prefijo `APP_`, valide tipos y **falle al arrancar** si falta un valor requerido — sin defaults inseguros para los secretos.

## 📋 Contexto

El capstone de la Fase 5 corre **una sola imagen** en dev y en prod; toda la diferencia entre entornos tiene que vivir en variables de entorno, no en el código. Este `Settings` es la pieza que lo hace posible y lo que hace pasar el gate de secret-scanning de `5.4`. Documenta la decisión (qué es config, dónde vive cada secreto) como material de un ADR.

## 📏 Primero-Sin-IA

1. Resuélvelo **solo** (timebox arriba). Implementa la clase a mano; míra fallar los tests primero.
2. Solo entonces consulta **documentación oficial** (`pydantic-settings`, `12factor.net` factor III).
3. **Solo al final**, usa IA para *revisar y explicar* tu solución — no para generarla.
4. Mañana, reescribe el `Settings` de memoria (prefijo, requerido sin default, opcional con default).

## 🛠️ Instrucciones

1. Necesitas el paquete: `uv add pydantic-settings` (o `pip install pydantic-settings`).
2. Abre `settings.py` y completa la clase `Settings` y la función `get_settings()` (no cambies sus nombres ni el contrato: los tests dependen de ellos).
3. Corre los tests:

   ```bash
   uv run pytest        # o:  pytest
   ```

4. Itera hasta que **todos pasen en verde**. Añade al menos **un caso de prueba tuyo** en `test_settings.py`.
5. Escribe `bitacora.md` (ver criterios).

## ✅ Criterios de "hecho" (Definition of Done del ejercicio)

- [ ] `pytest` en verde: lee los requeridos del entorno; `port`/`debug` usan default y también se leen del entorno; `debug` parsea `"true"`/`"1"`; falta un requerido → `ValidationError`; entorno vacío también lanza (no hay default inseguro).
- [ ] `database_url` y `api_key` **no** tienen default; ningún secreto aparece escrito en el código.
- [ ] `bitacora.md` explica qué es config y qué no (un ejemplo de cada uno de tu propio proyecto) y por qué un `.env` commiteado rompe el Factor III.
- [ ] Añadiste un caso de prueba propio.
- [ ] Puedes **explicar sin notas** por qué un requerido-sin-default es mejor que un default vacío (fail-fast).

## 💡 Pista (ábrela solo si superaste el timebox)

<details>
<summary>Mostrar pista</summary>

En `pydantic-settings`, un campo **sin** `=` es requerido; uno **con** `=` tiene default. La conexión al entorno va en `model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")`. `Settings()` lee del entorno al instanciarse: si falta un requerido, lanza `ValidationError`. `get_settings()` debe devolver `Settings()` (instancia nueva) en cada llamada. Repasa la sección 4.2 y 6.3 de la lección antes de mirar la referencia.

</details>

## 🤖 Cómo pedir la corrección

Cuando termines, entrega a tu asistente de IA:

- tu solución (este directorio: `settings.py`, `test_settings.py`, `bitacora.md`),
- la **rúbrica**: `.ai/rubricas/fase-5/config-en-entorno.md`,
- las instrucciones: `.ai/INSTRUCCIONES-CORRECTOR.md`.

La **solución de referencia** vive en `.ai/soluciones/fase-5/config-en-entorno.md` — no la mires antes de intentarlo de verdad.
