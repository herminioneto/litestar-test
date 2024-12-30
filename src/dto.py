from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from .models import Todo


class WriteTodoDTO(SQLAlchemyDTO[Todo]):
    config = SQLAlchemyDTOConfig(exclude={'id'})
