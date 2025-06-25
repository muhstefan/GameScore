from contextlib import asynccontextmanager
from items_views import router as items_router
from microshop.core.models import db_helper
from templates import templates
from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from api_v1 import router as router_v1
from pages import router as pages_router
from core.config import settings
from fastapi.staticfiles import StaticFiles
import uvicorn

@asynccontextmanager          # контекстный менеджер в котором можно создать БД и что-то сделать после завершения
async def lifespan(app: FastAPI):
    async  with db_helper.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)  # передаем функцию но не вызываем ее, этим займется фреймворк.
app.include_router(items_router)
app.include_router(router_v1,prefix=settings.api_v1_prefix)
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index_page(request: Request):
    print(f"Request object: {request.url}")
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )






if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)