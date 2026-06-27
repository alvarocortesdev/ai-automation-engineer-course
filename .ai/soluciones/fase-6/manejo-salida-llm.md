---
ejercicio_id: fase-6/manejo-salida-llm
fase: fase-6
sub_unidad: "6.14"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Es una **vara de
> medir**, no un guion a entregar. Hay varias implementaciones correctas; usa esto para
> detectar huecos y graduar pistas.

# Solución de referencia — Output handling de la salida de un LLM

## Implementación canónica

```python
from __future__ import annotations

import html
from dataclasses import dataclass

MAX_CARACTERES = 4000
PATRONES_PROHIBIDOS = ["[[system_prompt]]", "sk-live-"]


@dataclass
class Resultado:
    accion: str
    motivo: str
    valor_seguro: str | None = None


def manejar_salida(texto: str) -> Resultado:
    bajo = texto.lower()
    # Capa 1: fuga (LLM07 System Prompt Leakage / LLM02 Sensitive Info Disclosure).
    for patron in PATRONES_PROHIBIDOS:
        if patron in bajo:
            return Resultado(accion="BLOQUEAR", motivo="fuga")
    # Capa 2: presupuesto (LLM10 Unbounded Consumption).
    if len(texto) > MAX_CARACTERES:
        return Resultado(accion="BLOQUEAR", motivo="presupuesto")
    # Capa 3: codificacion para el sink HTML (LLM05 Improper Output Handling).
    return Resultado(accion="RENDER", motivo="ok", valor_seguro=html.escape(texto))
```

Pasa los 11 tests. Lo esencial:

- **Orden**: fuga → presupuesto → codificación. La fuga es lo más grave (nunca debe
  salir bajo ninguna forma), por eso va primero, antes incluso del límite de longitud.
- **Comparación insensible a mayúsculas**: `texto.lower()` contra patrones ya en
  minúsculas. Atrapa `SK-LIVE-`, `Sk-Live-`, etc.
- **`html.escape`, no a mano**: la stdlib convierte `< > & " '` en entidades. El
  `<script>` sale como `&lt;script&gt;` (texto inerte), por eso **se renderiza, no se
  bloquea**.
- **Frontera inclusiva**: `len > MAX_CARACTERES` (estricto), así que `MAX_CARACTERES`
  exacto pasa.

## La idea de fondo (lo que se evalúa de verdad)

El ejercicio enseña la **asimetría** de LLM05:

- **HTML peligroso → codificar (RENDER).** La defensa de Improper Output Handling es
  **context-aware encoding**: vuelves la salida segura **para el sink concreto**. Para
  HTML, escapar deja el markup inerte. El usuario igual ve "lo que dijo el modelo",
  solo que como texto, no como código ejecutable.
- **Secreto / system prompt → bloquear.** No existe una codificación que vuelva seguro
  **mostrar** un secreto. La única respuesta correcta es no mostrarlo (LLM07/LLM02).
- **Salida abusiva → bloquear (LLM10).** Un techo duro de recursos no es codificable;
  es un límite.

Si el sink fuera otro, la capa 3 cambiaría: **SQL** → consulta parametrizada (jamás
interpolar la salida); **shell** → nunca pasarla a un shell, usar argumentos
escapados/lista; **otro agente** → marcarla como dato no confiable, no como instrucción.
Mismo principio, distinta codificación según destino. Un alumno **excelente** dice esto
sin que se lo pidan.

## Puntos resbalosos (donde el corrector debe mirar)
1. **Invertir codificar/bloquear.** Bloquear el `<script>` "porque es peligroso" suena
   prudente pero es el error conceptual: para el sink HTML la defensa es codificar. Y
   renderizar un secreto "porque no trae HTML" es la fuga que el ejercicio busca cerrar.
2. **Orden de capas.** Si revisa longitud antes que fuga, un secreto larguísimo podría
   bloquearse "por presupuesto" en vez de "por fuga" — el motivo importa para auditoría,
   y peor: si alguien sube el techo, la fuga se escapa. La fuga va primero.
3. **Escaper a mano.** Reemplazar `<`→`&lt;` manualmente olvida `&`, comillas, casos
   raros. En prod es una vulnerabilidad; aquí, contradice el contrato (`html.escape`).
4. **Confundir el ejercicio con un anti-XSS completo.** Esto es el **modelo mental**;
   en prod se usa bleach/DOMPurify. El write-up debe reconocerlo.

## Rango de soluciones aceptables
- Cualquier estructura de control vale (early-return, if/elif, un dict de chequeos) si
  respeta el **orden** y el **contrato** de `Resultado`.
- `motivo` puede tener cualquier texto razonable; los tests no lo verifican, pero un
  `motivo` informativo es señal de pensar en observabilidad (sube a excelente).
- Está bien usar `any(p in bajo for p in PATRONES_PROHIBIDOS)` en vez del bucle
  explícito.
- NO se acepta: bloquear el `<script>`, renderizar una fuga, escaper a mano, o invertir
  el orden de modo que un secreto pueda escapar por otra rama.
