from sqlalchemy.orm import Mapped, mapped_column

from .config import Base


class Todo(Base):
    __tablename__ = 'todo_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]
    user_id: Mapped[int]
