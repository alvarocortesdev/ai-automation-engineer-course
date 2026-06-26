---
ejercicio_id: fase-1/capstone-misma-app-dos-lenguajes
fase: fase-1
sub_unidad: "1.P"
version: 1
---

> 🚫 **SPOILER — material del corrector.** No mostrar al alumno. Úsala solo como
> vara de medir (ver `.ai/soluciones/README.md` y `INSTRUCCIONES-CORRECTOR.md` §6).
> Es **una** solución de referencia válida, no la única. El código de abajo está
> **verificado** (pytest 8/8, vitest 8/8, `tsc --noEmit` limpio, y smoke con `curl`
> de las 5 rutas + 6 casos borde en ambas versiones).

# Solución de referencia — Capstone F1: La misma app, dos lenguajes

## 1. Dominio Python (`python/pantry.py`)

```python
from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError  # noqa: F401


class NewItem(BaseModel):
    name: str = Field(min_length=1)
    quantity: float = Field(gt=0)
    unit: str = Field(min_length=1)


class Item(NewItem):
    id: int


class PantryStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _load(self) -> list[dict]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, items: list[dict]) -> None:
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_items(self) -> list[dict]:
        return self._load()

    def add_item(self, data: dict) -> dict:
        new = NewItem.model_validate(data)  # ValidationError si no valida
        items = self._load()
        next_id = max((it["id"] for it in items), default=0) + 1
        item = Item(id=next_id, **new.model_dump())
        items.append(item.model_dump())
        self._save(items)
        return item.model_dump()

    def get_item(self, item_id: int) -> dict | None:
        for it in self._load():
            if it["id"] == item_id:
                return it
        return None

    def remove_item(self, item_id: int) -> bool:
        items = self._load()
        kept = [it for it in items if it["id"] != item_id]
        if len(kept) == len(items):
            return False
        self._save(kept)
        return True
```

## 2. Capa HTTP Python (`python/server.py`, solo ruteo)

```python
def do_GET(self) -> None:
    if self.path == "/health":
        return self._send(200, {"status": "ok"})
    if self.path == "/items":
        return self._send(200, STORE.list_items())
    if self.path.startswith("/items/"):
        item_id = self._parse_id()
        if item_id is None:
            return self._send(400, {"error": "id inválido"})
        item = STORE.get_item(item_id)
        return self._send(200, item) if item else self._send(404, {"error": "no encontrado"})
    self._send(404, {"error": "ruta no encontrada"})

def do_POST(self) -> None:
    if self.path != "/items":
        return self._send(404, {"error": "ruta no encontrada"})
    try:
        data = json.loads(self._read_body())
    except json.JSONDecodeError:
        return self._send(400, {"error": "JSON inválido"})
    try:
        item = STORE.add_item(data)
    except ValidationError as e:
        detalles = [
            {"campo": ".".join(str(p) for p in err["loc"]), "problema": err["msg"]}
            for err in e.errors()
        ]
        return self._send(422, {"error": "validación", "detalles": detalles})
    self._send(201, item)

def do_DELETE(self) -> None:
    if self.path.startswith("/items/"):
        item_id = self._parse_id()
        if item_id is None:
            return self._send(400, {"error": "id inválido"})
        return self._send(204) if STORE.remove_item(item_id) else self._send(404, {"error": "no encontrado"})
    self._send(404, {"error": "ruta no encontrada"})
```

> Nota sobre serializar `ValidationError`: `e.errors()` trae dicts con `loc`/`msg`;
> se mapean a una forma simple y JSON-serializable. Devolver `str(e)` también es
> aceptable; lo importante es el status `422` y que el dato **no** se persista.

## 3. Dominio TypeScript (`typescript/pantry.ts`)

```ts
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { z } from "zod";

export const NewItemSchema = z.object({
  name: z.string().min(1),
  quantity: z.number().positive(),
  unit: z.string().min(1),
});

export type NewItem = z.infer<typeof NewItemSchema>;
export type Item = NewItem & { id: number };

export class PantryStore {
  constructor(private readonly path: string) {
    if (!existsSync(this.path)) writeFileSync(this.path, "[]", "utf-8");
  }

  private load(): Item[] {
    return JSON.parse(readFileSync(this.path, "utf-8")) as Item[];
  }

  private save(items: Item[]): void {
    writeFileSync(this.path, JSON.stringify(items, null, 2), "utf-8");
  }

  list(): Item[] {
    return this.load();
  }

  add(data: unknown): Item {
    const parsed = NewItemSchema.parse(data); // ZodError si no valida
    const items = this.load();
    const nextId = items.reduce((max, it) => Math.max(max, it.id), 0) + 1;
    const item: Item = { id: nextId, ...parsed };
    items.push(item);
    this.save(items);
    return item;
  }

  get(id: number): Item | undefined {
    return this.load().find((it) => it.id === id);
  }

  remove(id: number): boolean {
    const items = this.load();
    const kept = items.filter((it) => it.id !== id);
    if (kept.length === items.length) return false;
    this.save(kept);
    return true;
  }
}
```

## 4. Capa HTTP TypeScript (`typescript/server.ts`, solo ruteo)

```ts
const server = createServer(async (req, res) => {
  const path = req.url ?? "";
  const method = req.method ?? "GET";

  if (method === "GET" && path === "/health") return send(res, 200, { status: "ok" });
  if (method === "GET" && path === "/items") return send(res, 200, store.list());

  if (method === "POST" && path === "/items") {
    const raw = await readBody(req);
    let data: unknown;
    try {
      data = JSON.parse(raw);
    } catch {
      return send(res, 400, { error: "JSON inválido" });
    }
    try {
      return send(res, 201, store.add(data));
    } catch (err) {
      if (err instanceof ZodError) return send(res, 422, { error: "validación", detalles: err.issues });
      throw err;
    }
  }

  if (path.startsWith("/items/")) {
    const id = parseId(path);
    if (id === null) return send(res, 400, { error: "id inválido" });
    if (method === "GET") {
      const item = store.get(id);
      return item ? send(res, 200, item) : send(res, 404, { error: "no encontrado" });
    }
    if (method === "DELETE") {
      return store.remove(id) ? send(res, 204) : send(res, 404, { error: "no encontrado" });
    }
  }

  send(res, 404, { error: "ruta no encontrada" });
});
```

## 5. El write-up de trade-offs esperado (qué debe nombrar)

Un write-up **competente** menciona diferencias concretas y vividas en *este*
código, no generalidades. Las que de verdad aparecen al construirlo:

- **Coerción de tipos en runtime.** pydantic con `quantity: float` convierte el
  `2` entero del JSON en `2.0` → la API Python responde `"quantity": 2.0`. zod con
  `z.number()` deja `2` como `2`. Misma regla ("número > 0"), distinto resultado
  serializado. *(Diferencia real verificada con `curl`.)*
- **Derivación del tipo.** En TS, `z.infer<typeof NewItemSchema>` da el tipo gratis;
  en Python la "herencia" `class Item(NewItem)` reusa los campos validados. Dos
  formas de no repetirse.
- **Ausencia.** `get` devuelve `None` (Python) vs `undefined` (TS). El test lo
  refleja (`is None` vs `toBeUndefined`).
- **La excepción de validación.** `ValidationError` (pydantic) vs `ZodError` (zod);
  la capa HTTP las atrapa distinto pero mapea al mismo `422`.
- **La plomería HTTP.** `BaseHTTPRequestHandler` con métodos `do_GET/do_POST` vs
  `createServer((req, res) => …)` con `req.method`. Leer el body: `self.rfile.read`
  vs `for await (const chunk of req)`.
- **Lo que NO cambió** (y es el punto): la estructura —dominio + validación +
  persistencia + HTTP— es idéntica. *El problema es el mismo; el idioma cambia.*

## 6. Rango de soluciones aceptables
- **`quantity` como `int` en vez de `float`:** válido si el alumno decide que la
  despensa solo maneja enteros; entonces Python no coerciona a `2.0`. Es una
  decisión de diseño defendible (debería estar en `DECISIONES.md`).
- **Persistencia:** un solo archivo JSON es lo esperado. Usar SQLite es
  sobre-ingeniería para F1 (DB llega en F3); no es "mejor", es fuera de alcance.
- **Cuerpo de error:** cualquier forma JSON razonable para el `422`/`400`/`404`
  sirve; el contrato no fija el cuerpo de error, solo el status.
- **`if/elif` vs `if`+`return` temprano:** ambos válidos en el ruteo.
- **Devolver `str(e)` en el `422`** en vez del detalle estructurado: aceptable.
- **No separar `_load`/`_save`** (inline en cada método): funciona, pero baja la
  legibilidad; `competente`, no `excelente`.
- **Framework web (FastAPI/Express), base de datos, async sin necesidad:** fuera de
  alcance para F1 → señal de dependencia-IA (ver rúbrica), aunque "funcione".
- **Ruta opcional de IA:** si la implementó, debe **validar** la salida del LLM con
  pydantic/zod (no `json.loads` a secas) y registrar tokens/costo. Sin eso, no
  cuenta como victoria-IA bien hecha.

## 7. Cómo verificar rápido (para el corrector)
```bash
# Python
cd python && uv run pytest -q            # espera: 8+ passed
uv run python server.py &                # luego curl localhost:8000/health -> {"status":"ok"}
# TypeScript
cd typescript && npm install && npm test # espera: 8+ passed
npm start &                              # luego curl localhost:8001/health -> {"status":"ok"}
```
