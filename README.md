# NetPulse

Plataforma de monitorización de red: agentes ligeros recogen métricas
de dispositivos (CPU, RAM, disco, red, latencia) y las envían a una
API que las persiste y expone para consulta e histórico.

**Estado actual:** v0.2 — registro de dispositivos, ingesta de métricas
(`MetricSnapshot`) y agente real que recoge CPU/RAM/disco/red con `psutil`.

## Arquitectura

```
Agent (Linux) --POST--> API (FastAPI) --> PostgreSQL
```

## Stack

- FastAPI + Pydantic
- SQLAlchemy + PostgreSQL
- Alembic (migraciones)

## Cómo levantarlo en local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # y ajusta DATABASE_URL si hace falta
uvicorn api.main:app --reload
```

Docs interactivas: http://localhost:8000/docs

## Roadmap

- [x] v0.1 — Devices CRUD básico
- [x] v0.2 — MetricSnapshots + agente Python real + health check + migraciones (Alembic)
- [ ] v0.3 — Dockerizado (app + Postgres vía docker-compose)
- [ ] v0.4 — Desplegado en AWS (VPC, EC2, RDS)
- [ ] v0.5 — Infraestructura como código (Terraform)
- [ ] v0.6 — CI/CD (GitHub Actions: lint + tests + build)
- [ ] v0.7 — Autenticación por API key para el agente
- [ ] v0.8 — Detección de estado (online/offline) a partir del último snapshot
- [ ] v0.9 — Alertas simples (umbrales, ej. CPU > 90%)
- [ ] v1.0 — Dashboard (evaluar Grafana sobre Postgres vs. frontend propio)
