import os
from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

# 1. Берем секретный мастер-ключ из настроек Railway
# (он называется MASTER_GOOGLE_KEY в разделе Variables)
MASTER_KEY = os.environ.get("MASTER_GOOGLE_KEY")

# 2. База данных ключей пользователей (можно добавлять новые сюда)
KEYS = {
    "av_user1": 1000,
    "av_user2": 1000
}

@app.post("/ask")
async def ask(prompt: str, api_key: str = Header(...)):
    # Проверка существования ключа и лимита
    if api_key not in KEYS or KEYS[api_key] <= 0:
        raise HTTPException(status_code=403, detail="Доступ запрещен: неверный ключ или лимит исчерпан")
    
    # URL для обращения к Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MASTER_KEY}"
    
    # Формируем тело запроса
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    # Отправляем запрос к Google
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Вызовет ошибку, если запрос не удался
        
        # Уменьшаем лимит пользователя
        KEYS[api_key] -= 1
        
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка соединения с ИИ: {str(e)}")

# Для тестирования (просто чтобы сервер "дышал")
@app.get("/")
async def root():
    return {"status": "Aviorum Server is running"}
    
