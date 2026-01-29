import logging
import os
from dataclasses import dataclass
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass(frozen=True, slots=True)
class AiConfig:

    _Config = None

    @classmethod
    def get_config(cls) -> "AiConfig":
        if cls._Config is None:
            raise Exception("Config not loaded")
        return cls._Config

    @classmethod
    def _env_override(cls, config_dict: dict):
        for key in config_dict.keys():
            override = os.getenv(f"ASSISTVET_PROVET_{key.upper()}", None)
            if override:
                logger.info(f"Overriding config {key} with env var ASSISTVET_PROVET_{key.upper()}")
                config_dict[key] = override

    @classmethod
    def load(cls, path: str):
        with Path(path).open("r", encoding="utf-8") as f:
            config_dict = yaml.safe_load(f.read())
        cls._env_override(config_dict)
        cls._Config = AiConfig(**config_dict)
        return cls._Config
