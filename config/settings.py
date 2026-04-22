


from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	# Example settings, customize as needed
	ENV:str 
	DUCK_PATH:str

	class Config:
		env_file = ".env"

settings = Settings()



