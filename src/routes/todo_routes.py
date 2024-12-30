from litestar import get, post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto import WriteTodoDTO
from src.models import Todo


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
