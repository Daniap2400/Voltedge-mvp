import os

APP_NAME = os.getenv("APP_NAME", "voltedge-api")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

USE_DATABASE = os.getenv("USE_DATABASE", "false").lower() == "true"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://voltedge:voltedge@db:5432/voltedge",
)