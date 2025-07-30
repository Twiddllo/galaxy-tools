from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL environment variable
db_url = os.getenv('DATABASE_URL')

# Raise an error if DATABASE_URL is not set
if not db_url:
    raise ValueError("❌ DATABASE_URL is not set. Make sure it exists in your .env file.")

# Alembic Config object for handling migrations
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Import the models Base class
from app.models import Base

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = context.engine or context.create_engine(
        db_url,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# Check if Alembic is running in offline mode or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
