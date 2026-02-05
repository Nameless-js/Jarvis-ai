from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import UserQuery, AIResponse
from .db_service import get_relevant_context
from .ai_service import generate_answer

# Создаем приложение
app = FastAPI(title="College Jarvis Backend")

# Настройка CORS (чтобы React мог стучаться к нам без ошибок)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем всем (для разработки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Jarvis is ready"}

@app.post("/ask", response_model=AIResponse)
async def ask_question(query: UserQuery):
    """
    Главный эндпоинт:
    1. Получает вопрос
    2. Ищет инфу в БД
    3. Генерирует ответ через ИИ
    """
    # Шаг 1: Ищем факты
    context = await get_relevant_context(query.text)
    
    # Шаг 2: Думаем и формулируем ответ
    answer_text = await generate_answer(query.text, context)
    
    # Шаг 3: Отдаем результат
    return AIResponse(answer=answer_text)