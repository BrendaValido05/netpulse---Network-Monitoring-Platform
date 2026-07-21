"""
Modelos de base de datos (tablas).

Decisión de diseño (ver docs/decisions/003-tabla-ancha-metricas.md):
usamos una tabla ancha con columnas fijas para las métricas conocidas,
no un modelo EAV, porque el conjunto de métricas de un sistema es
razonablemente estable y las columnas fijas permiten queries e
índices mucho más simples y rápidos.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, unique=True, nullable=False, index=True)
    ip = Column(String, nullable=False)
    type = Column(String, nullable=False)  # router | server | switch | host
    created_at = Column(DateTime, default=datetime.utcnow)

    snapshots = relationship("MetricSnapshot", back_populates="device")


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    cpu_pct = Column(Float, nullable=True)
    ram_pct = Column(Float, nullable=True)
    disk_pct = Column(Float, nullable=True)
    net_in_kbps = Column(Float, nullable=True)
    net_out_kbps = Column(Float, nullable=True)
    latency_ms = Column(Float, nullable=True)

    device = relationship("Device", back_populates="snapshots")

    __table_args__ = (
        # Query más frecuente: histórico de un dispositivo ordenado por tiempo.
        Index("ix_snapshots_device_timestamp", "device_id", "timestamp"),
    )
