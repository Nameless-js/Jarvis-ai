from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Импортируем нашу функцию получения ответа
from .ai_service import get_answer

app = FastAPI()

# --- НАСТРОЙКА РАЗРЕШЕНИЙ (CORS) ---
# Это позволяет фронтенду на React общаться с бэкендом на FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше заменить на ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных для запроса
class QuestionRequest(BaseModel):
    text: str
    language: str = "ru"

@app.post("/ask")
async def ask_jarvis(request: QuestionRequest):
    """
    Основной маршрут для общения с Джарвисом.
    Мы используем await, так как get_answer теперь асинхронная.
    """
    try:
        # Ждем, пока ИИ сгенерирует ответ и проверит базу данных
        response_text = await get_answer(request.text) 
        return {"response": response_text}
    except Exception as e:
        print(f"💀 КРИТИЧЕСКАЯ ОШИБКА В MAIN: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "Jarvis is online and ready for service"}