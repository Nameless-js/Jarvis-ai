import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем ключ из .env
load_dotenv(dotenv_path="app/.env") 
# Если файл .env лежит внутри папки app, путь может быть "app/.env"
# Если в корне backend, то просто load_dotenv()
# Давай попробуем универсально:
if not os.getenv("GOOGLE_API_KEY"):
    load_dotenv() 

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Ошибка: Не найден GOOGLE_API_KEY. Проверь файл .env")
else:
    print(f"🔑 Ключ найден (хвост: ...{api_key[-4:]})")
    genai.configure(api_key=api_key)

    print("\n🔍 Список моделей, доступных для генерации текста:")
    try:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"   ✅ {m.name}")
                found = True
        
        if not found:
            print("   ⚠️ Модели найдены, но ни одна не поддерживает generateContent.")
            
    except Exception as e:
        print(f"❌ Ошибка при запросе списка моделей: {e}")