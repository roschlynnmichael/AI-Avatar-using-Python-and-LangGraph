import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from livekit.api import AccessToken, VideoGrants
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenRequest(BaseModel):
    room_name: str
    participant_name: str

@app.post("/api/get-token")
async def get_token(req: TokenRequest):
    api_key = os.getenv("LIVE_KIT_API_KEY") 
    api_secret = os.getenv("LIVE_KIT_API_SECRET") 
    livekit_url = os.getenv("LIVE_KIT_WEBSOCKET_URL")

    if not api_key or not api_secret or not livekit_url:
        raise HTTPException(status_code=500, detail="Missing configuration")

    token = (
        AccessToken(api_key, api_secret)
        .with_identity(req.participant_name)
        .with_grants(VideoGrants(room_join=True, room=req.room_name))
    )
    
    return {
        "token": token.to_jwt(),
        "url": livekit_url
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)