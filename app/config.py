from pydantic_settings import BaseSettings, SettingsConfigDict
from decimal import Decimal

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    REDIS_URL: str
    BOT_TOKEN: str
    ADMIN_IDS: list[int] = []

    @property
    def DATABASE_URL_asyncpg(self):
        
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    model_config = SettingsConfigDict(env_file='.env')

settings=Settings()

DEFAULT_REWARD_FOR_SUB = Decimal("1") 
DEFAULT_WORKER_PAY = Decimal("0.25")
SYSTEM_BANK_ID = 1
STARS_TO_USDT = Decimal('0.013')
MIN_WITHDRAWAL = Decimal(25)

