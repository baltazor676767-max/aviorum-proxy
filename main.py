import os
from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI()

MASTER_KEY = os.environ.get("MASTER_GOOGLE_KEY")
KEYS = {"av_user1": 1000, "av_user2": 1000}

@app.post("/ask")
async def ask(prompt: str, api_key: str = Header(...)):
    if not MASTER_KEY:
        raise HTTPException(status_code=500, detail="MASTER_GOOGLE_KEY не задан")
    
    if api_key not in KEYS or KEYS[api_key] <= 0:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Используем проверенное имя модели
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MASTER_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        
        KEYS[api_key] -= 1
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Aviorum Server is running"}
    
