# Repo a auditar: `mi-rag-app`

> Esta es la "foto" de un repo de portafolio real-ish que un junior subió a GitHub para mostrarlo en su
> perfil. Tu trabajo (en `auditoria.md`) es diagnosticarlo. NO necesitas clonarlo ni ejecutar nada:
> todo lo que necesitas está aquí abajo.

## `git log --oneline` (más reciente arriba)

```text
a1b2c3d update
e4f5a6b asdf
1a2b3c4 fix bug
9z8y7x6 wip
5q4w3e2 Update README (again)
0p9o8i7 add openai key so it works
7h6g5f4 first commit
```

## Árbol de archivos (`git ls-files`)

```text
mi-rag-app/
├── .env
├── main.py
├── ingest.py
├── requirements.txt
├── notebook_pruebas.ipynb
└── README.md
```

> Nota: no hay `LICENSE`. No hay `.gitignore`.

## Fragmento de `.env` (sí, está commiteado en el repo)

```bash
OPENAI_API_KEY=sk-proj-9aF2b7QxLmN0pRsTuVwXyZ1234567890abcdEFGH
DATABASE_URL=postgres://admin:admin123@localhost:5432/ragdb
```

## Contenido completo de `README.md`

```markdown
# mi-rag-app
```

## Fragmento de `main.py` (para contexto, no para arreglar el código)

```python
import os
from openai import OpenAI

# la key esta en .env, ver el commit "add openai key so it works"
client = OpenAI(api_key="sk-proj-9aF2b7QxLmN0pRsTuVwXyZ1234567890abcdEFGH")

def responder(pregunta: str) -> str:
    resp = client.responses.create(model="gpt-4o-mini", input=pregunta)
    return resp.output_text
```

> (El código en sí no es el foco del ejercicio: el foco es la **higiene del repo** como pieza de
> portafolio. Pero si algo del código agrava un problema de seguridad, anótalo.)
