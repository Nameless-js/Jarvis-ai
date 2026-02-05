import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем переменные
load_dotenv()

# Настраиваем Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Выбираем модель (gemini-1.5-flash — быстрая и дешевая/бесплатная)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
Ты — официальный виртуальный ассистент колледжа.
Твоя задача: отвечать на вопросы, используя ТОЛЬКО предоставленный контекст.

ПРАВИЛА:
1. Используй ТОЛЬКО информацию из блока "ВНУТРЕННЯЯ БАЗА ЗНАНИЙ".
2. Если информации нет, отвечай: "К сожалению, у меня нет информации по этому вопросу."
3. Не придумывай (не галлюцинируй).
4. Отвечай вежливо, кратко и официально.
5. Если вопрос на казахском — отвечай на казахском.
"""

async def generate_answer(user_question: str, context: str) -> str:
    """
    Отправляет запрос в Google Gemini
    """
    full_prompt = f"""
    {SYSTEM_PROMPT}

    ВНУТРЕННЯЯ БАЗА ЗНАНИЙ:
    {context}
    
    ВОПРОС ПОЛЬЗОВАТЕЛЯ:
    {user_question}
    """

    try:
        # Gemini поддерживает асинхронность через generate_content_async
        response = await model.generate_content_async(full_prompt)
        return response.text
    except Exception as e:
        return f"Ошибка при обращении к Gemini: {str(e)}"