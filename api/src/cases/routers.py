from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.cases.schemas import CasesCreateSchema, CasesUpdateSchema, CasesResponseSchema
from src.db.connect import get_db
from src.db.models import Case
from typing import List

router = APIRouter(prefix="/v1/cases", tags=["Cases"])


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=CasesResponseSchema
)
def create_cases(request: CasesCreateSchema, db: Session = Depends(get_db)):
    new_case = Case(**request.model_dump())
    if not new_case:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case


@router.get(
    "/list", status_code=status.HTTP_200_OK, response_model=List[CasesResponseSchema]
)
def get_all_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).all()
    if not cases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cases not found"
        )
    return cases


@router.get("/{case_id}", status_code=status.HTTP_200_OK)
def get_case_by_id(case_id: str, db: Session = Depends(get_db)):
    cases = db.query(Case).filter(Case.case_id == case_id).first()
    if not cases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Case not found"
        )
    return cases


@router.put(
    "/update/{case_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CasesResponseSchema,
)
def update_cases(
    case_id: str, request: CasesUpdateSchema, db: Session = Depends(get_db)
):
    cases = db.query(Case).filter(Case.case_id == case_id)
    if not cases.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Case not found"
        )
    cases.update(request.model_dump(), synchronize_session=False)
    db.commit()
    updated_case = cases.first()
    return updated_case


@router.delete("/delete/{case_id}", status_code=status.HTTP_200_OK)
def delete_cases(case_id: str, db: Session = Depends(get_db)):
    cases = db.query(Case).filter(Case.case_id == case_id)
    if not cases.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Case not found"
        )
    cases.delete(synchronize_session=False)
    db.commit()
    return {"response": "Successfull"}
