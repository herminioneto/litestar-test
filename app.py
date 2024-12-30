from collections.abc import AsyncGenerator

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import autocommit_before_send_handler
from litestar import Litestar, get, post
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from litestar.status_codes import HTTP_409_CONFLICT
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = 'todo_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    user_id: Mapped[int]


class WriteTodoDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(exclude={'id'})


async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@post('/todo', dto=WriteTodoDTO)
async def create_todo(data: Todo, transaction: AsyncSession) -> Todo:
    transaction.add(data)
    await transaction.flush()
    return data


@get('/todos')
async def get_todos(transaction: AsyncSession) -> list[Todo]:
    query = select(Todo)
    result = await transaction.execute(query)
    return result.scalars().all()


db_config = SQLAlchemyAsyncConfig(
    connection_string='sqlite+aiosqlite:///db.sqlite',
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)

app = Litestar(
    [get_todos, create_todo],
    dependencies={'transaction': provide_transaction},
    plugins=[
        SQLAlchemyPlugin(db_config),
    ],
    debug=True,
)
