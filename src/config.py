"""Configuration management"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # Elasticsearch (SIEM)
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    ELASTICSEARCH_USERNAME: str = "elastic"
    ELASTICSEARCH_PASSWORD: str = "changeme"

    # Threat Intelligence
    THREAT_INTEL_ENABLED: bool = True
    MITRE_ATTACK_DB: str = "/data/mitre-attack.json"
    CVE_DATABASE_PATH: str = "/data/cve.db"

    # Anomaly Detection
    ANOMALY_MODEL: str = "isolation_forest"
    ANOMALY_THRESHOLD: float = 0.8
    RETRAINING_INTERVAL: str = "24h"

    # Incident Response
    AUTO_RESPONSE_ENABLED: bool = True
    RESPONSE_TIMEOUT: str = "30s"
    ESCALATION_THRESHOLD: str = "high"

    # Alerts
    ALERT_WEBHOOK: Optional[str] = None
    EMAIL_NOTIFICATIONS: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
