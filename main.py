import os
from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

# Ваш ключ от DeepSeek теперь будет лежать в этой переменной
MASTER_KEY = os.environ.get("MASTER_GOOGLE_KEY")
KEYS = {"av_user1": 1000, "av_user2": 1000}

@app.post("/ask")
async def ask(prompt: str, api_key: str = Header(...)):
    if not MASTER_KEY:
        raise HTTPException(status_code=500, detail="Ключ не задан")
    
    if api_key not in KEYS:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # URL API DeepSeek
    url = "https://api.deepseek.com/v1/chat/completions"
    
    # Заголовки с авторизацией через Bearer
    headers = {
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    }
    
    # Формат запроса для DeepSeek
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Aviorum DeepSeek Proxy is running"}
    
