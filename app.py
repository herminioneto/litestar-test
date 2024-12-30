from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin

from src.config import db_config
from src.routes.todo_routes import create_todo, get_todos
from src.services.database import provide_transaction

app = Litestar(
    [get_todos, create_todo],
    dependencies={'transaction': provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    debug=True,
)
