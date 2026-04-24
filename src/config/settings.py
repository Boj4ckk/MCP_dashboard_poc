


import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=str(env_file),
		case_sensitive=False
	)

	ENV: str
	DUCK_PATH: str

settings = Settings()
print(f"[DEBUG] Loaded from: {env_file}")
print(f"[DEBUG] DUCK_PATH={settings.DUCK_PATH}")
print(f"[DEBUG] Current directory: {os.getcwd()}")



