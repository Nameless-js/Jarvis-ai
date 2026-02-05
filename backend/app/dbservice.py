import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Читаем настройки из .env
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Если ключей нет - будет ошибка, но пока оставим так
if url and key:
    supabase: Client = create_client(url, key)
else:
    supabase = None

async def get_relevant_context(query: str) -> str:
    # Если база не подключена (нет ключей), вернем заглушку
    if not supabase:
        return "Ошибка: Не настроено подключение к базе данных (нет ключей в .env)."

    try:
        # ВАЖНО: Спроси у друга, как называется таблица!
        # Здесь я написал 'documents', а колонку 'content'.
        # Если у него таблица 'info', замени "documents" на "info".
        response = supabase.table("documents") \
            .select("content") \
            .ilike("content", f"%{query}%") \
            .execute()

        if not response.data:
            return "В базе данных нет информации по этому вопросу."

        # Собираем все найденные тексты
        found_texts = [item['content'] for item in response.data]
        return "\n---\n".join(found_texts)

    except Exception as e:
        return f"Ошибка при поиске в БД: {str(e)}"