from alembic.config import Config
from alembic import command
from src.database.db import SQLALCHEMY_DATABASE_URL

def test_run_migrations_offline():
    test_database_url = "sqlite:///test.db"
    
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", test_database_url)
    command.upgrade(alembic_config, "head")
    command.downgrade(alembic_config, "base")

