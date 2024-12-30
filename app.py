from litestar import Litestar, get


@get('/')
async def main() -> str:
    return 'Hello World!'


app = Litestar([main])
