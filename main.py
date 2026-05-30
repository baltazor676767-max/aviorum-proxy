import os
from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

# Получаем ключ из переменных Railway
MASTER_KEY = os.environ.get("MASTER_GOOGLE_KEY")

# Список ключей (можете добавить свои)
KEYS = {"av_user1": 1000, "av_user2": 1000}

@app.post("/ask")
async def ask(prompt: str, api_key: str = Header(...)):
    # Проверка наличия ключа в переменных окружения
    if not MASTER_KEY:
        raise HTTPException(status_code=500, detail="Ошибка: MASTER_GOOGLE_KEY не задан в настройках Railway")
    
    # Проверка ключа доступа пользователя
    if api_key not in KEYS or KEYS[api_key] <= 0:
        raise HTTPException(status_code=403, detail="Доступ запрещен или закончились лимиты")
    
    # URL для обращения к модели Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={MASTER_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        # Отправка запроса к Google
        response = requests.post(url, json=payload, timeout=20)
        
        # Если Google вернул ошибку, пробрасываем её в ответе
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Google ответил: {response.text}")
        
        # Уменьшаем лимит пользователя
        KEYS[api_key] -= 1
        return response.json()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка соединения с ИИ: {str(e)}")

@app.get("/")
async def root():
    return {"status": "Aviorum Server is running"}
    
