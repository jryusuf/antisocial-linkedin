from sqlmodel import SQLModel

class Settings(SQLModel):
    #sqlite+aiosqlite:///test2.db
    #postgresql+asyncpg://postgres:postgres@127.0.0.1:5432
    database_url: str = "sqlite+aiosqlite:///test2.db"
    echo_sql: bool = False
    test: bool = False
    project_name: str = "antisocial_backend"
    oauth_token_secret: str = "my_dec_secret"

settings = Settings()