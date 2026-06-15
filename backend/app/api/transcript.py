from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.call import Call
from app.models.transcript import Transcript
from app.schemas.transcript import TranscriptCreate


router = APIRouter(
    prefix="/transcripts",
    tags=["Transcripts"]
)


@router.post("/create")
def create_transcript(
    data: TranscriptCreate,
    db: Session = Depends(get_db)
):
    call = db.query(Call).filter(
        Call.id == data.call_id
    ).first()

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    transcript = Transcript(
        call_id=data.call_id,
        speaker=data.speaker,
        message=data.message
    )

    db.add(transcript)
    db.commit()
    db.refresh(transcript)

    return {
        "message": "Transcript created successfully",
        "transcript": transcript
    }


@router.get("/call/{call_id}")
def get_call_transcripts(
    call_id: int,
    db: Session = Depends(get_db)
):
    call = db.query(Call).filter(
        Call.id == call_id
    ).first()

    if not call:
        raise HTTPException(status_code=404, detail="Call not found")

    transcripts = db.query(Transcript).filter(
        Transcript.call_id == call_id
    ).order_by(Transcript.id.asc()).all()

    return {
        "call_id": call_id,
        "total_messages": len(transcripts),
        "transcripts": transcripts
    }


@router.delete("/delete/{transcript_id}")
def delete_transcript(
    transcript_id: int,
    db: Session = Depends(get_db)
):
    transcript = db.query(Transcript).filter(
        Transcript.id == transcript_id
    ).first()

    if not transcript:
        raise HTTPException(status_code=404, detail="Transcript not found")

    db.delete(transcript)
    db.commit()

    return {
        "message": "Transcript deleted successfully"
    }