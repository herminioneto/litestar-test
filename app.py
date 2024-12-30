from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'todo_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    user_id: Mapped[int]


@get('/todos')
async def get_todos(db_session: AsyncSession) -> list[Todo]:
    async with db_session.begin():
        query = select(Todo)
        result = await db_session.execute(query)
        return result.scalars().all()


db_config = SQLAlchemyAsyncConfig(
    connection_string='sqlite+aiosqlite:///db.sqlite',
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)

app = Litestar([get_todos], plugins=[SQLAlchemyPlugin(db_config)])
