from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db_config = SQLAlchemyAsyncConfig(
    connection_string='sqlite+aiosqlite:///db.sqlite',
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)
