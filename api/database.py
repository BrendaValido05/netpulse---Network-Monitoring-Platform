"""
Setup de SQLAlchemy: engine (conexión física a Postgres), SessionLocal
(fábrica de sesiones) y Base (clase de la que heredan todos los modelos).

Por qué una función get_db() con yield en vez de crear una sesión
global: cada request de FastAPI necesita SU PROPIA sesión, que se
abre al empezar la request y se cierra al terminar (incluso si hay
un error). Esto evita conexiones colgadas y fugas de memoria.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
