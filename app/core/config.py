from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot - спонсирование котиков'
    description: str = 'Спонсируйте котиков в любых количествах!'
    database_url: str = 'sqlite+aiosqlite:///./catprojects.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
