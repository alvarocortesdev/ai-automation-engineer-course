# Scaffold del capstone — guía de uso

Este `starter/` te da el corazón testeable del sistema (el plano de control) y el
esqueleto de cómo conectar el "cerebro". **Copia estos archivos a tu repo del
proyecto** y construye la infraestructura alrededor (webhook, Temporal, evals,
observabilidad, CI/CD) siguiendo las Fases A–D del brief.

## Archivos

- `schemas.py` — modelo pydantic `PropuestaTicket` que el LLM llena (salida estructurada).
- `control_plane.py` — `decidir(...)` **a completar** (TODO). Es puro y determinista.
- `test_control_plane.py` — los tests que gatean tu plano de control.
- `.env.example` — variables de entorno; copia a `.env` (no commitees secretos).

## Correr los tests del plano de control

Desde esta carpeta:

```bash
uv run pytest        # o simplemente:  pytest
```

Implementa `decidir()` en `control_plane.py` hasta que **todos pasen en verde**,
incluidos los tests de ORDEN (la primera barrera gana: un duplicado con schema
inválido y acción sensible debe devolver `DUPLICADO`). Luego agrega tu propio test.

## Estructura de repo sugerida (la construyes tú)

```
mi-capstone/
├── README.md            # EN INGLÉS: qué hace, cómo correrlo, arquitectura
├── DISENO.md            # diagrama + tabla de decisión + ADR de Temporal (Primero-Sin-IA)
├── WRITE-UP.md          # trade-offs, número del eval gate + baseline, costo/latencia
├── POST-MORTEM.md       # historia de falla en producción (Track-0)
├── docker-compose.yml   # levanta Temporal + tu app + colector OTel
├── .github/workflows/   # CI: lint + tests + eval gate + secret-scan + SCA
├── app/
│   ├── webhook.py       # FastAPI: verifica HMAC + anti-replay, idempotency key, arranca workflow
│   ├── extraction.py    # el "cerebro": clasificar_y_extraer con Anthropic (corre dentro de una actividad)
│   ├── control_plane.py # ← de este starter
│   ├── schemas.py       # ← de este starter
│   ├── workflow.py      # workflow Temporal + espera durable del HITL
│   ├── activities.py    # actividades: extraer, ejecutar acción (idempotente), enviar_a_dlq
│   └── telemetry.py     # OTel: spans por paso, correlation id = message_id
├── evals/
│   ├── golden_set.jsonl # casos anotados (idealmente desde trazas reales)
│   ├── baseline.json    # accuracy de routing/extracción del baseline (versionado)
│   └── eval_gate.py     # mide y bloquea el deploy ante regresión
└── tests/
    └── test_control_plane.py  # ← de este starter (+ tus tests de integración)
```

## Dónde vive cada punto del Definition of Done

| # | Punto | Archivo / pieza |
|---|---|---|
| 1 | Spec + ADRs | `DISENO.md` |
| 2 | Tests + lint en CI | `tests/`, `.github/workflows/` |
| 3 | Seguridad (HMAC, LLM01/05/06, scanning) | `app/webhook.py`, `app/control_plane.py`, CI |
| 4 | Observabilidad (trazas) | `app/telemetry.py` |
| 5 | Eval gate + budget | `evals/` |
| 6 | Plano de control | `app/control_plane.py` |
| 7 | a11y (si hay UI HITL) | tu UI/consola de aprobación |
| 8 | Demo + README inglés + write-up | `docker-compose.yml`, `README.md`, `WRITE-UP.md` |
| 9 | Conventional Commits | historial del repo |
