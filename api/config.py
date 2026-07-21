"""
Configuración centralizada de la app.

Por qué esto y no leer os.environ directamente en cada archivo:
- Un único punto de verdad para toda la configuración.
- pydantic-settings valida tipos y falla rápido si falta una variable.
- Cuando despliegues en AWS, solo cambias las variables de entorno
  reales (o un Secrets Manager) — el código no cambia nada.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://netpulse:netpulse@localhost:5432/netpulse"

    class Config:
        env_file = ".env"


settings = Settings()
