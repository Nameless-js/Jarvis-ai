from pydantic import BaseModel
from typing import Optional

# Модель запроса (то, что присылает фронтенд)
class UserQuery(BaseModel):
    text: str              # Сам вопрос (например: "Где 205 кабинет?")
    language: str = "ru"   # Язык (ru или kk), по умолчанию русский

# Модель ответа (то, что мы отправляем обратно)
class AIResponse(BaseModel):
    answer: str            # Текст ответа от ИИ
    audio_url: Optional[str] = None # Ссылка на озвучку (на будущее)