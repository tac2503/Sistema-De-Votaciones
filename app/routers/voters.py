from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(prefix="/voters", tags=["Voters"])


@router.post(
    "/", response_model=schemas.VoterResponse, status_code=status.HTTP_201_CREATED,summary="Crear votante", description="Crea un nuevo votante en el sistema, no debe ser candidato."
)
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    
    exists_voter = crud.get_voter_by_email(db, voter.email)
    if exists_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un votante con ese email",
        )
    
    
    exists_candidate = crud.get_candidate_by_name(db, voter.name)
    if exists_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este nombre ya está registrado como candidato",
        )

    new_voter = crud.create_voter(db, voter)
    return new_voter


@router.delete(
    "/{voter_id}",
    response_model=schemas.DeleteVoterResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar votante",
    description="Elimina un votante del sistema."
)
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = crud.get_voter_by_id(db, voter_id)
    if not voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Votante no encontrado",
        )
    voter_deleted = crud.delete_voter(db, voter_id)
    if voter_deleted:
        return schemas.DeleteVoterResponse(message="Votante eliminado exitosamente")
