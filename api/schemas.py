"""
Schemas de Pydantic: definen la forma de los datos que entran y
salen de la API. Son distintos de los modelos de SQLAlchemy (models.py)
a propósito: los modelos representan la tabla en la base de datos,
los schemas representan el contrato de la API. Separarlos te permite,
por ejemplo, no exponer nunca campos internos por accidente.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    hostname: str
    ip: str
    type: str


class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    hostname: str
    ip: str
    type: str
    created_at: datetime


class SnapshotCreate(BaseModel):
    hostname: str  # el agente se identifica por hostname, no por UUID interno
    cpu_pct: Optional[float] = None
    ram_pct: Optional[float] = None
    disk_pct: Optional[float] = None
    net_in_kbps: Optional[float] = None
    net_out_kbps: Optional[float] = None
    latency_ms: Optional[float] = None


class SnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_id: uuid.UUID
    timestamp: datetime
    cpu_pct: Optional[float] = None
    ram_pct: Optional[float] = None
    disk_pct: Optional[float] = None
    net_in_kbps: Optional[float] = None
    net_out_kbps: Optional[float] = None
    latency_ms: Optional[float] = None
