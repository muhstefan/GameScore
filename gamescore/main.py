import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from starlette.responses import RedirectResponse

from gamescore.api_v1 import router as router_v1
from gamescore.core.config import settings
from gamescore.core.models import db_helper
from gamescore.middleware.middleware import auth_middleware
from gamescore.pages import router as pages_router

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager  # контекстный менеджер в котором можно создать БД и что-то сделать после завершения
async def lifespan(app: FastAPI):
    async  with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
app.include_router(pages_router)
app.middleware("http")(auth_middleware)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/pages/home")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
