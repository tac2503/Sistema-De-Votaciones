from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "/",
    response_model=schemas.VoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar voto",
    description="Registra un voto emitido por un votante para un candidato específico.",
)
def register_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    voter = crud.get_voter_by_id(db, vote.voter_id)
    if not voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Votante no encontrado",
        )
    if voter.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El votante ya ha emitido su voto",
        )

    candidate = crud.get_candidate_by_id(db, vote.candidate_id)
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidato no encontrado",
        )

    new_vote = crud.create_vote(db, vote)

    voter.has_voted = True
    db.commit()

    return new_vote


@router.get(
    "/", response_model=list[schemas.VoteListResponse], status_code=status.HTTP_200_OK
)
def list_votes(db: Session = Depends(get_db)):
    votes = crud.get_votes(db)
    return votes


@router.get(
    "/statistics",
    response_model=schemas.VoteStatisticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Estadísticas de votos",
    description="Obtiene estadísticas detalladas sobre los votos emitidos, incluyendo el total de votantes que han votado, el total de votos emitidos, y un desglose de votos por candidato con su porcentaje correspondiente.",
)
def get_statistics(db: Session = Depends(get_db)):
    statistics = crud.get_vote_statistics(db)
    return statistics
