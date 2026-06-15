import os
import uuid
import requests

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.config import settings
from app.services.voice_service import generate_ai_response


router = APIRouter(
    prefix="/voice",
    tags=["Voice AI"]
)


class VoiceRequest(BaseModel):
    message: str


@router.post("/text-to-speech")
def text_to_speech(data: VoiceRequest):
    try:
        ai_reply = generate_ai_response(data.message)

        voice_id = "EXAVITQu4vr4xnSDxMaL"

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": settings.ELEVENLABS_API_KEY
        }

        payload = {
            "text": ai_reply,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=response.text
            )

        filename = f"generated_audio/{uuid.uuid4()}.mp3"

        with open(filename, "wb") as audio_file:
            audio_file.write(response.content)

        return FileResponse(
            filename,
            media_type="audio/mpeg",
            filename="ai_response.mp3"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )