"""Contexto de LECTURA del ejercicio 2.8 — diseño de dobles y contrato.

NO ejecutas ni modificas este archivo: lo lees para diseñar tu estrategia de tests
en `plan-de-tests.md`. Los colaboradores (PasarelaDePago, Reloj, EnviadorDeEmail,
RepositorioDeReembolsos) se muestran como Protocols para que veas su firma; en un
test reemplazarías cada uno por el test double que decidas.

Pregúntate, colaborador por colaborador:
  - ¿Solo necesito que devuelva un valor enlatado?        -> stub
  - ¿Necesito verificar QUE lo llamaron y con qué?        -> spy / mock
  - ¿Necesito una implementación que FUNCIONE pero liviana? -> fake
  - ¿Es un argumento que ni se usa en este camino?         -> dummy
Y: ¿qué colaborador cruza una frontera hacia OTRO equipo y por tanto merece un
contrato (Pact), no un mock que codifica TU suposición de su respuesta?
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ResultadoPasarela:
    id_transaccion: str
    estado: str  # "aprobado" | "rechazado"


@dataclass(frozen=True)
class Reembolso:
    cobro_id: str
    monto: int            # en centavos
    id_transaccion: str
    emitido_en: str       # ISO-8601


class PasarelaDePago(Protocol):
    """API HTTP de OTRO equipo. Ejecuta el reembolso del lado del banco."""
    def reembolsar(self, cobro_id: str, monto: int) -> ResultadoPasarela: ...


class Reloj(Protocol):
    def ahora(self) -> str: ...   # ISO-8601


class EnviadorDeEmail(Protocol):
    """Envía por SMTP externo. No hay estado consultable desde el test."""
    def enviar_comprobante(self, destinatario: str, reembolso: Reembolso) -> None: ...


class RepositorioDeReembolsos(Protocol):
    def guardar(self, reembolso: Reembolso) -> None: ...
    def por_cobro(self, cobro_id: str) -> Reembolso | None: ...


class ReembolsoRechazado(Exception):
    pass


class ServicioDeReembolsos:
    def __init__(
        self,
        pasarela: PasarelaDePago,
        reloj: Reloj,
        emailer: EnviadorDeEmail,
        repo: RepositorioDeReembolsos,
    ) -> None:
        self._pasarela = pasarela
        self._reloj = reloj
        self._emailer = emailer
        self._repo = repo

    def reembolsar(self, cobro_id: str, monto: int, monto_cobro_original: int, email: str) -> Reembolso:
        # Regla de negocio: no se puede reembolsar más de lo cobrado.
        if monto <= 0 or monto > monto_cobro_original:
            raise ReembolsoRechazado("monto de reembolso inválido")

        resultado = self._pasarela.reembolsar(cobro_id, monto)   # frontera HTTP (otro equipo)
        if resultado.estado != "aprobado":
            raise ReembolsoRechazado(f"la pasarela rechazó: {resultado.estado}")

        reembolso = Reembolso(cobro_id, monto, resultado.id_transaccion, self._reloj.ahora())
        self._repo.guardar(reembolso)                            # efecto: persiste (estado)
        self._emailer.enviar_comprobante(email, reembolso)       # efecto: SMTP (sin estado)
        return reembolso
