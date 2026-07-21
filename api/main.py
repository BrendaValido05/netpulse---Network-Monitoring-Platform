from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from api import crud, schemas
from api.database import get_db

app = FastAPI(title="NetPulse", version="0.1.0")


@app.post("/devices", response_model=schemas.DeviceOut, status_code=201)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    existing = crud.get_device_by_hostname(db, device.hostname)
    if existing:
        raise HTTPException(status_code=409, detail="hostname ya registrado")
    return crud.create_device(db, device)


@app.get("/devices", response_model=list[schemas.DeviceOut])
def list_devices(db: Session = Depends(get_db)):
    return crud.get_devices(db)


@app.post("/snapshots", response_model=schemas.SnapshotOut, status_code=201)
def create_snapshot(snapshot: schemas.SnapshotCreate, db: Session = Depends(get_db)):
    device = crud.get_device_by_hostname(db, snapshot.hostname)
    if not device:
        raise HTTPException(
            status_code=404,
            detail=f"dispositivo '{snapshot.hostname}' no registrado, usa POST /devices primero",
        )
    return crud.create_snapshot(db, device.id, snapshot)


@app.get("/snapshots", response_model=list[schemas.SnapshotOut])
def list_snapshots(hostname: str | None = None, db: Session = Depends(get_db)):
    device_id = None
    if hostname:
        device = crud.get_device_by_hostname(db, hostname)
        if not device:
            raise HTTPException(status_code=404, detail="dispositivo no encontrado")
        device_id = device.id
    return crud.get_snapshots(db, device_id=device_id)


@app.get("/health")
def health():
    # Endpoint que usará AWS (o cualquier load balancer/orquestador) para
    # saber si la instancia está viva. Cuando tengamos DB obligatoria en
    # el camino crítico, aquí se podría añadir un `SELECT 1`.
    return {"status": "healthy"}
