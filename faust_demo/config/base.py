from typing import Optional
from pydantic import BaseSettings, validator, SecretStr
from typing import Optional, Dict, Any
import faust
from faust.types.auth import AuthProtocol
import ssl


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    FAUST_APP_ID: Optional[str] = "faust-demo"
    KAFKA_CLIENT_ID: Optional[str] = "faust-demo"
    KAFKA_BROKERS: Optional[str] = "kafka://localhost:9092"
    KAFKA_USERNAME: Optional[str] = None
    KAFKA_PASSWORD: Optional[SecretStr] = None
    KAFKA_CONSUMER_AUTO_OFFSET_RESET: Optional[str] = "earliest"
    KAFKA_TOPIC_REPLICATION_FACTOR: Optional[int] = 1
    KAFKA_TOPIC_PARTITIONS: Optional[int] = 1

    FAUST_CONNECT_OPTIONS: Optional[Dict[str, Any]] = None

    @validator("FAUST_CONNECT_OPTIONS", pre=True)
    def assemble_faust_connect_options(cls, v: Optional[str], values: Dict[str, Any]):

        username = values.get("KAFKA_USERNAME")
        password = values.get("KAFKA_PASSWORD")

        if username is not None and password is not None:
            credentials = faust.SASLCredentials(
                username=username,
                password=password.get_secret_value(),
                ssl_context=ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH),
            )

        options = {
            "id": values.get("FAUST_APP_ID"),
            "broker": values.get("KAFKA_BROKERS"),
            "broker_credentials": credentials if credentials else None,
            "topic_replication_factor": values.get("KAFKA_TOPIC_REPLICATION_FACTOR"),
            "topic_partitions": values.get("KAFKA_TOPIC_PARTITIONS"),
            "consumer_auto_offset_reset": values.get("KAFKA_CONSUMER_AUTO_OFFSET_RESET"),
        }

        return options
