import uvicorn
from typing import List
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from scripts.tg.start import get_channel_messages
from domain.db_config import init_db
app = FastAPI()

class Search(BaseModel):
    text: str = Field(min_length=3)
    channel: str or None
    limit: int = Field(ge=1, default=10) 

@app.get("/user/{user_id}")
async def get_user(useer_id: int = 1):
    return {"message": "Hello World"}

@app.post("/tg/search")
async def add_test(search: Search, background_tasks: BackgroundTasks):
    background_tasks.add_task(get_channel_messages, search_text=search.text, channel_username=search.channel, limit=search.limit)
    
    return {"message": "ok"}



@app.on_event("startup")
async def startup():
    await init_db()
    

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=settings.SERVICES['pos_service']['port'],
        host=settings.SERVICES['pos_service']['ip'],
    )