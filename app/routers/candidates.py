from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post(
    "/", response_model=schemas.CandidateResponse, status_code=status.HTTP_201_CREATED, summary="Crear candidato", description="Crea un nuevo candidato en el sistema, no debe ser votante."
)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    
    exists_candidate = crud.get_candidate_by_name(db, candidate.name)
    if exists_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un candidato con ese nombre",
        )
    
    
    exists_voter = crud.get_voter_by_name(db, candidate.name)
    if exists_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nombre ya está registrado como votante",
        )
    
    new_candidate = crud.create_candidate(db, candidate)
    return new_candidate


@router.get(
    "/", response_model=list[schemas.CandidateResponse], status_code=status.HTTP_200_OK, summary="Listar candidatos", description="Obtiene una lista de todos los candidatos registrados en el sistema."
)
def list_candidates(db: Session = Depends(get_db)):
    candidates = crud.get_candidates(db)
    return candidates
