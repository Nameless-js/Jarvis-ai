import os
import google.generativeai as genai
from dotenv import load_dotenv
from .db_service import get_relevant_context

load_dotenv()

# --- 1. ПРОВЕРКА КЛЮЧА ---
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ КРИТИЧЕСКАЯ ОШИБКА: В файле .env нет GOOGLE_API_KEY!")
else:
    # Показываем последние 4 символа ключа для проверки (безопасно)
    print(f"✅ API Key загружен (заканчивается на ...{API_KEY[-4:]})")
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

def get_answer(question: str):
    print(f"\n🧠 [AI] Получен вопрос: {question}")
    
    # Добавь async перед def
async def get_answer(question: str):
    print(f"\n🧠 [AI] Получен вопрос: {question}")
    
    # --- 2. ПОИСК В БАЗЕ (Supabase) ---
    context = ""
    try:
        # Добавляем await, чтобы дождаться ответа от базы
        context = await get_relevant_context(question) 
        if context:
            print(f"📚 [DB] Найден контекст: {context[:50]}...")
        else:
            print("📭 [DB] Контекст не найден (база пуста или нет совпадений)")
    except Exception as e:
        print(f"⚠️ [DB] Ошибка подключения к базе: {e}")

    # --- 3. ЗАПРОС К GEMINI ---
    prompt = f"""
    Ты — голосовой ассистент Джарвис. Отвечай кратко (1-2 предложения), с сарказмом.
    Если в контексте есть информация о кабинетах — используй её.
    Контекст: {context}
    Вопрос: {question}
    """

    try:
        print("⏳ [AI] Отправляю запрос в Google Gemini...")
        # Сами запросы к Gemini обычно блокирующие в этой библиотеке, 
        # но мы можем оставить как есть, главное — починить await выше.
        response = model.generate_content(prompt)
        
        if response and response.text:
            clean_text = response.text.strip()
            print(f"🗣 [AI] Ответ Gemini: {clean_text}")
            return clean_text
        else:
            return "Мои нейросети молчат. Попробуй спросить по-другому."

    except Exception as e:
        print(f"💀 [AI] ОШИБКА GEMINI: {e}")
        return f"Ошибка мозга: {str(e)}"