"""SETTINGS
Settings loaders using Pydantic BaseSettings classes (load from environment variables / dotenv file)
"""

from dotenv import load_dotenv
import pydantic
import os

load_dotenv()


__all__ = ("api_settings", "mongo_settings", "aws_settings","model_settings")


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"


class APISettings(BaseSettings):
    TITLE: str = os.getenv("API_TITLE", "Garderobe")
    HOST: str = "0.0.0.0"
    PORT: int = os.getenv("API_PORT", 5000)
    LOG_LEVEL: str = os.getenv("API_LOG_LEVEL", "info")
    SECRET_KEY: str = os.getenv("API_SECRET_KEY", "secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    class Config(BaseSettings.Config):
        env_prefix = "API_"


class MongoSettings(BaseSettings):
    URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE: str = os.getenv("MONGO_DATABASE", "garderobe")
    COLLECTION: str = os.getenv("MONGO_COLLECTION", "index_features")

    class Config(BaseSettings.Config):
        env_prefix = "MONGO_"


class AwsSettings(BaseSettings):
    AWS_S3_ACCESS_KEY_ID: str= os.getenv("AWS_S3_ACCESS_KEY_ID", "")
    AWS_S3_SECRET_ACCESS_KEY:str = os.getenv("AWS_S3_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET_NAME:str = os.getenv("AWS_S3_BUCKET_NAME", "")

    class Config(BaseSettings.Config):
        env_prefix = "AWS_"


class ModelSettings(BaseSettings):
    MODEL_URL = os.getenv("MODEL_URL", "")
    IMAGE_WIDTH = os.getenv("IMAGE_WIDTH", 224)
    IMAGE_HEIGHT = os.getenv("IMAGE_HEIGHT", 224)

    class Config(BaseSettings.Config):
        env_prefix = "MODEL_"


api_settings = APISettings()
mongo_settings = MongoSettings()
aws_settings = AwsSettings()
model_settings = ModelSettings()