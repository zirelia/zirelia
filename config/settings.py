# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

import yaml
from pathlib import Path
from typing import Dict, Any, Type, Tuple, Optional
from functools import lru_cache
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict

class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a YAML file
    at the project's root.
    """
    def __call__(self) -> Dict[str, Any]:
        """
        Loads settings from the YAML file and returns them as a dictionary.
        This method is required by Pydantic V2 settings sources.
        """
        encoding = self.config.get("env_file_encoding")
        file_content_json = {}
        
        # Try to load settings.yaml
        yaml_file = Path("virtual_influencer_engine/config/settings.yaml")
        if yaml_file.exists():
            try:
                with open(yaml_file, 'r', encoding=encoding) as f:
                    file_content_json = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load settings.yaml: {e}")

        # Map generic YAML structure to flattened settings
        settings_dict = {}
        
        # Helper to safely get nested values
        def get_nested(data, *keys):
            for key in keys:
                if isinstance(data, dict):
                    data = data.get(key)
                else:
                    return None
            return data

        # Map known fields manually or use a flattening strategy
        # Here we manually map for safety and clarity as per get_field_value logic
        
        if val := get_nested(file_content_json, "TWITTER", "API_KEY"):
            settings_dict["TWITTER_API_KEY"] = val
        if val := get_nested(file_content_json, "TWITTER", "API_SECRET"):
            settings_dict["TWITTER_API_SECRET"] = val
        if val := get_nested(file_content_json, "TWITTER", "ACCESS_TOKEN"):
            settings_dict["TWITTER_ACCESS_TOKEN"] = val
        if val := get_nested(file_content_json, "TWITTER", "ACCESS_SECRET"):
            settings_dict["TWITTER_ACCESS_TOKEN_SECRET"] = val
            
        if val := file_content_json.get("DATABASE_URL"):
             settings_dict["DATABASE_URL"] = val
             
        # Add other fields as needed or implement a recursive flatten
        
        return settings_dict

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        # Legacy method kept for compatibility if needed, but __call__ is primary for V2
        return None, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

class Settings(BaseSettings):
    # Core
    PROJECT_NAME: str = "Virtual Influencer Engine"
    ENV: str = "development"
    
    # Database & Redis
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Meta (Facebook, Instagram)
    META_APP_ID: Optional[str] = None
    META_APP_SECRET: Optional[str] = None
    META_ACCESS_TOKEN: Optional[str] = None
    FACEBOOK_PAGE_ID: Optional[str] = None
    INSTAGRAM_ACCOUNT_ID: Optional[str] = None
    
    # Threads (separate app & token from Meta)
    THREADS_ACCESS_TOKEN: Optional[str] = None
    THREADS_USER_ID: Optional[str] = None
    THREADS_APP_SECRET: Optional[str] = None
    
    # Twitter (X)
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    # Image Generation
    REPLICATE_API_TOKEN: Optional[str] = None
    REPLICATE_MODEL_VERSION: str = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b7159d55fe748cc"

    model_config = SettingsConfigDict(
        env_file=[".env", "virtual_influencer_engine/.env"], 
        case_sensitive=True,
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls), # Add YAML source
            file_secret_settings,
        )

@lru_cache()
def get_settings():
    return Settings()
