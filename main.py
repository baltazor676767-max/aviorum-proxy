from fastapi import FastAPI, Header, HTTPException
import requests
import os

app = FastAPI()

# Мастер-ключ берется из настроек Railway (настроим позже)
MASTER_KEY = os.environ.get("MASTER_GOOGLE_KEY")

# Список ключей пользователей
KEYS = {"av_user1": 100, "av_user2": 50}

@app.post("/ask")
async def ask(prompt: str, api_key: str = Header(...)):
    # Проверка ключа
    if api_key not in KEYS or KEYS[api_key] <= 0:
        raise HTTPException(status_code=403, detail="Ключ не активен или исчерпан")
    
    # Запрос к Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MASTER_KEY}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
    
    # Уменьшаем лимит
    KEYS[api_key] -= 1
    return response.json()
  
