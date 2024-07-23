from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(main_router, prefix="")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)