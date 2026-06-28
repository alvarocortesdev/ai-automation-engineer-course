"""bot_legado.py  —  NO lo ejecutes. Léelo y diagnostícalo.

Bot RPA "grabado" hace años. Cada noche toma una planilla de proveedores nuevos y
los da de alta, uno por uno, en un portal web que (dicen) no tiene API. Opera la
interfaz por COORDENADAS y esperas fijas. En la demo funcionaba. En producción se
rompe cada vez que alguien estornuda cerca del portal.

Tu trabajo (en `migracion.md`): diagnosticar por qué se rompe, clasificar cada paso
en la escalera de integración, y planear la migración con Strangler Fig.
"""

import csv
import time

import pyautogui  # mueve el mouse y teclea a nivel de sistema operativo


def cargar_proveedores(ruta: str) -> list[dict]:
    with open(ruta, newline="", encoding="latin-1") as f:
        return list(csv.DictReader(f))


def validar_rut(rut: str) -> bool:
    # Validación de RUT chileno (dígito verificador). Lógica pura, sin UI.
    cuerpo, dv = rut[:-1].replace(".", ""), rut[-1].upper()
    suma, factor = 0, 2
    for d in reversed(cuerpo):
        suma += int(d) * factor
        factor = 2 if factor == 7 else factor + 1
    resto = 11 - (suma % 11)
    esperado = {10: "K", 11: "0"}.get(resto, str(resto))
    return dv == esperado


def dar_de_alta(proveedor: dict) -> None:
    pyautogui.click(820, 410)              # "botón Nuevo proveedor" (posición fija)
    time.sleep(3)                          # esperar a que cargue el formulario
    pyautogui.typewrite(proveedor["rut"])
    pyautogui.press("tab")
    pyautogui.typewrite(proveedor["nombre"])
    pyautogui.press("tab")
    pyautogui.typewrite(proveedor["email"])
    pyautogui.click(960, 720)              # "botón Guardar" (otra posición fija)
    time.sleep(2)
    # ¿se guardó? ¿salió "RUT duplicado"? ¿se cayó la sesión? El bot no lo sabe.


def main() -> None:
    proveedores = cargar_proveedores("proveedores.csv")
    for p in proveedores:
        if not validar_rut(p["rut"]):
            continue                       # RUT inválido: se ignora SIN avisar a nadie
        dar_de_alta(p)                     # sin try/except, sin log, sin reanudación


if __name__ == "__main__":
    main()
