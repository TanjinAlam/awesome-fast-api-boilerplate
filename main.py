import os

import click
import uvicorn
from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from core.config import config
engines = {
    "writer": create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
    "reader": create_async_engine(config.READER_DB_URL, pool_recycle=3600),
}


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str, debug: bool):
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False
    )


if __name__ == "__main__":
    main()


