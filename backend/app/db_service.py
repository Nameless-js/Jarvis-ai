import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Указываем путь к .env, который лежит в той же папке app
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_ANON_KEY")

# Проверка для отладки (увидим в терминале)
if not url or not key:
    print("❌ DB_SERVICE: URL или KEY для Supabase не найдены в .env!")
else:
    supabase: Client = create_client(url, key)

async def get_relevant_context(question: str):
    try:
        # Пытаемся достать данные из таблицы university_info
        # Убедись, что в Supabase создана таблица с таким именем!
        response = supabase.table("university_info").select("content").execute()
        
        if response.data:
            # Просто склеиваем все записи для примера
            all_info = " ".join([item['content'] for item in response.data])
            return all_info
        return ""
    except Exception as e:
        return f"Ошибка подключения к базе данных: {str(e)}"