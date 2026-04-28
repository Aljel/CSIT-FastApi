from src.infrastructure.sqlite.database import database, Base
import asyncio
import uvicorn

from src.app import create_app

app = create_app()


@app.on_event("startup")
def startup():
    from src.infrastructure.sqlite.models import users_model, posts_model, comments_model, categories_model
    Base.metadata.create_all(bind=database._engine)  # используем _engine


async def main() -> None:
    config = uvicorn.Config(
        "main:app", host="0.0.0.0", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    asyncio.run(main())
