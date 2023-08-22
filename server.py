import uvicorn
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from application.api_routers import public_router
from config import settings
from domain.db_config import init_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_db()


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public_router)

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=settings.SERVICES['sc_service']['port'],
        host=settings.SERVICES['sc_service']['ip'],
    )

