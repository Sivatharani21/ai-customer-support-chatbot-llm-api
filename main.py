from fastapi import FastAPI
from dotenv import load_dotenv
from backend.db.database import init_db
from backend.api.routes import router

load_dotenv()

app = FastAPI(title="AI Customer Support Chatbot", version="1.0.0")

init_db()

app.include_router(router)
