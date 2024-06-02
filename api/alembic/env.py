from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src import create_app
from src.config import settings
from src.database import Base
from src.users.models import User
from src.tdd.models import Member
from src.datasets.models import Dataset
from src.locations.models import Location
from src.people.models import Person
from src.organizations.models import Organization


def include_name(name, type_, parent_names) -> bool:
    """
    Determine if a given database object should be included in the migration scripts.

    This function is used to filter out specific database objects during the migration process.
    It is particularly useful for excluding objects from certain schemas, such as PostGIS objects,
    which might otherwise be automatically included and processed by Alembic.
    For PostGis specifically, see: https://github.com/sqlalchemy/alembic/discussions/1282

    Args:
        name (str): The name of the database object.
        type_ (str): The type of the database object (e.g., 'table', 'schema').
        parent_names (dict): A dictionary containing the parent names of the database object.

    Returns:
        bool: True if the object should be included, False otherwise.
    """
    if type_ == "schema":
        return False
    else:
        return True


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

fastapi_app = create_app()

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_name=include_name,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
