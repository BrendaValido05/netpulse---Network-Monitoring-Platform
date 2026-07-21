import socket

from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    api_url: str = "http://localhost:8000"
    interval_seconds: int = 30
    local_ip: str = socket.gethostbyname(socket.gethostname())

    class Config:
        env_file = ".env"


agent_settings = AgentSettings()
