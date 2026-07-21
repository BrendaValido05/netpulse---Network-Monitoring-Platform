"""
Agente NetPulse: recoge métricas reales de la máquina donde corre y
las envía a la API cada N segundos.

Estructura en funciones pequeñas (collect_cpu, collect_ram...) en vez
de un único bloque, para que cada métrica se pueda testear y ampliar
por separado sin tocar el resto.
"""

import socket
import time

import psutil
import requests

from agent.config import agent_settings


def collect_cpu() -> float:
    return psutil.cpu_percent(interval=1)


def collect_ram() -> float:
    return psutil.virtual_memory().percent


def collect_disk() -> float:
    return psutil.disk_usage("/").percent


def collect_network() -> tuple[float, float]:
    counters = psutil.net_io_counters()
    return counters.bytes_sent / 1024, counters.bytes_recv / 1024


def build_snapshot() -> dict:
    net_out, net_in = collect_network()
    return {
        "hostname": socket.gethostname(),
        "cpu_pct": collect_cpu(),
        "ram_pct": collect_ram(),
        "disk_pct": collect_disk(),
        "net_in_kbps": net_in,
        "net_out_kbps": net_out,
    }


def send_snapshot(snapshot: dict) -> None:
    url = f"{agent_settings.api_url}/snapshots"
    try:
        response = requests.post(url, json=snapshot, timeout=5)
        response.raise_for_status()
        print(f"[ok] snapshot enviado: {snapshot}")
    except requests.RequestException as e:
        print(f"[error] no se pudo enviar el snapshot: {e}")


def register_self() -> None:
    """Registra este host como Device si todavía no existe."""
    url = f"{agent_settings.api_url}/devices"
    payload = {
        "hostname": socket.gethostname(),
        "ip": agent_settings.local_ip,
        "type": "host",
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        print(f"[error] no se pudo registrar el dispositivo: {e}")


def run() -> None:
    register_self()
    while True:
        snapshot = build_snapshot()
        send_snapshot(snapshot)
        time.sleep(agent_settings.interval_seconds)


if __name__ == "__main__":
    run()
