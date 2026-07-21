"""
Funciones de acceso a datos.

Por qué separar esto de main.py (los endpoints): los endpoints se
encargan de HTTP (status codes, request/response). Estas funciones
se encargan solo de la base de datos. Así puedes testear la lógica
de datos sin levantar un servidor HTTP, y reusar estas funciones
desde otros sitios (por ejemplo, un futuro script de administración).
"""

from sqlalchemy.orm import Session

from api import models, schemas


def create_device(db: Session, device: schemas.DeviceCreate) -> models.Device:
    db_device = models.Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_devices(db: Session) -> list[models.Device]:
    return db.query(models.Device).all()


def get_device_by_hostname(db: Session, hostname: str) -> models.Device | None:
    return db.query(models.Device).filter(models.Device.hostname == hostname).first()


def create_snapshot(
    db: Session, device_id, snapshot: schemas.SnapshotCreate
) -> models.MetricSnapshot:
    data = snapshot.model_dump(exclude={"hostname"})
    db_snapshot = models.MetricSnapshot(device_id=device_id, **data)
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot


def get_snapshots(
    db: Session, device_id=None, limit: int = 100
) -> list[models.MetricSnapshot]:
    query = db.query(models.MetricSnapshot)
    if device_id:
        query = query.filter(models.MetricSnapshot.device_id == device_id)
    return query.order_by(models.MetricSnapshot.timestamp.desc()).limit(limit).all()


def get_latest_snapshot(db: Session, device_id) -> models.MetricSnapshot | None:
    return (
        db.query(models.MetricSnapshot)
        .filter(models.MetricSnapshot.device_id == device_id)
        .order_by(models.MetricSnapshot.timestamp.desc())
        .first()
    )
