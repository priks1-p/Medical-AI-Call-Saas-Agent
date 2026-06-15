from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.knowledge_base import KnowledgeBase
from app.models.clinic import Clinic
from app.schemas.knowledge_base import KnowledgeBaseCreate, KnowledgeBaseUpdate


router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base"]
)


@router.post("/create")
def create_knowledge_base(
    data: KnowledgeBaseCreate,
    db: Session = Depends(get_db)
):
    clinic = db.query(Clinic).filter(
        Clinic.id == data.clinic_id
    ).first()

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    kb = KnowledgeBase(
        clinic_id=data.clinic_id,
        question=data.question,
        answer=data.answer,
        category=data.category
    )

    db.add(kb)
    db.commit()
    db.refresh(kb)

    return {
        "message": "Knowledge base item created successfully",
        "knowledge_base": kb
    }


@router.get("/all/{clinic_id}")
def get_all_knowledge_base(
    clinic_id: int,
    db: Session = Depends(get_db)
):
    items = db.query(KnowledgeBase).filter(
        KnowledgeBase.clinic_id == clinic_id
    ).all()

    return {
        "clinic_id": clinic_id,
        "total_items": len(items),
        "knowledge_base": items
    }


@router.get("/{kb_id}")
def get_knowledge_base_item(
    kb_id: int,
    db: Session = Depends(get_db)
):
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id
    ).first()

    if not kb:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base item not found"
        )

    return kb


@router.put("/update/{kb_id}")
def update_knowledge_base_item(
    kb_id: int,
    data: KnowledgeBaseUpdate,
    db: Session = Depends(get_db)
):
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id
    ).first()

    if not kb:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base item not found"
        )

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(kb, key, value)

    db.commit()
    db.refresh(kb)

    return {
        "message": "Knowledge base item updated successfully",
        "knowledge_base": kb
    }


@router.delete("/delete/{kb_id}")
def delete_knowledge_base_item(
    kb_id: int,
    db: Session = Depends(get_db)
):
    kb = db.query(KnowledgeBase).filter(
        KnowledgeBase.id == kb_id
    ).first()

    if not kb:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base item not found"
        )

    db.delete(kb)
    db.commit()

    return {
        "message": "Knowledge base item deleted successfully"
    }