/**
 * Ejercicio 4.5 B — Depura un panel lleno de useEffect.
 *
 * ⚠️ Este archivo es para LEER, no para ejecutar. No instales nada ni lo corras:
 *    diagnostícalo como en una revisión de código y escribe tu análisis en `diagnostico.md`.
 *
 * Hay CINCO efectos numerados. Cuatro tienen un problema distinto; uno está correcto.
 * (Las funciones `cargarInfoModelo`, `conectar` y `registrarAnalytics` son simuladas:
 *  fingen un backend, un WebSocket y analytics. No te distraigas con su implementación.)
 */

import { useEffect, useState } from "react";

interface Mensaje {
  id: string;
  texto: string;
}
interface InfoModelo {
  ventanaContexto: number;
}
interface Socket {
  onMessage(cb: (m: Mensaje) => void): void;
  close(): void;
}

declare function cargarInfoModelo(modelo: string): Promise<InfoModelo>;
declare function conectar(modelo: string): Socket;
declare function registrarAnalytics(evento: string, modelo: string): void;

interface PanelBuggyProps {
  modelo: string;
}

export function PanelBuggy({ modelo }: PanelBuggyProps) {
  const [mensajes, setMensajes] = useState<Mensaje[]>([]);
  const [conteo, setConteo] = useState(0);
  const [info, setInfo] = useState<InfoModelo | null>(null);
  const [enviado, setEnviado] = useState(false);

  // ── EFECTO 1 ─────────────────────────────────────────────────────────────
  useEffect(() => {
    setConteo(mensajes.length);
  }, [mensajes]);

  // ── EFECTO 2 ─────────────────────────────────────────────────────────────
  useEffect(() => {
    const socket = conectar(modelo);
    socket.onMessage((m) => setMensajes((prev) => [...prev, m]));
    return () => socket.close();
  }, []);

  // ── EFECTO 3 ─────────────────────────────────────────────────────────────
  useEffect(() => {
    cargarInfoModelo(modelo).then((data) => setInfo(data));
  }, [modelo]);

  // ── EFECTO 4 ─────────────────────────────────────────────────────────────
  useEffect(() => {
    document.title = `Chat con ${modelo} — ${conteo} mensajes`;
  }, [modelo, conteo]);

  // ── EFECTO 5 ─────────────────────────────────────────────────────────────
  useEffect(() => {
    if (enviado) {
      registrarAnalytics("mensaje_enviado", modelo);
      setEnviado(false);
    }
  }, [enviado, modelo]);

  function enviar() {
    const nuevo: Mensaje = { id: crypto.randomUUID(), texto: "hola" };
    setMensajes((prev) => [...prev, nuevo]);
    setEnviado(true);
  }

  return (
    <section>
      <p>
        {modelo}: {conteo} mensajes
      </p>
      <p>Ventana de contexto: {info?.ventanaContexto ?? "cargando..."}</p>
      <button onClick={enviar}>Enviar</button>
    </section>
  );
}
