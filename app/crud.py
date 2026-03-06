from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas


def get_voter_by_email(db: Session, email: str):
    return db.query(models.Voter).filter(models.Voter.email == email).first()


def get_voter_by_name(db: Session, name: str):
    return (
        db.query(models.Voter)
        .filter(func.lower(models.Voter.name) == name.lower())
        .first()
    )


def get_voter_by_id(db: Session, voter_id: int):
    return db.query(models.Voter).filter(models.Voter.id == voter_id).first()


def get_candidate_by_name(db: Session, name: str):
    return (
        db.query(models.Candidate)
        .filter(func.lower(models.Candidate.name) == name.lower())
        .first()
    )


def get_candidate_by_id(db: Session, candidate_id: int):
    return (
        db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    )


def get_candidates(db: Session):
    return db.query(models.Candidate).all()


def create_voter(db: Session, voter: schemas.VoterCreate):
    new_voter = models.Voter(name=voter.name, email=voter.email)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return new_voter


def delete_voter(db: Session, voter_id: int):
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    if not voter:
        return False
    db.delete(voter)
    db.commit()
    return True


def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    new_candidate = models.Candidate(name=candidate.name, party=candidate.party)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate


def create_vote(db: Session, vote: schemas.VoteCreate):
    new_vote = models.Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
    db.add(new_vote)

    candidate = (
        db.query(models.Candidate)
        .filter(models.Candidate.id == vote.candidate_id)
        .first()
    )
    if candidate:
        candidate.votes += 1

    db.commit()
    db.refresh(new_vote)
    return new_vote


def get_votes(db: Session):
    rows = (
        db.query(
            models.Vote.id,
            models.Vote.voter_id,
            models.Voter.name.label("voter_name"),
            models.Vote.candidate_id,
            models.Candidate.name.label("candidate_name"),
        )
        .join(models.Voter, models.Vote.voter_id == models.Voter.id)
        .join(models.Candidate, models.Vote.candidate_id == models.Candidate.id)
        .all()
    )

    return [
        schemas.VoteListResponse(
            id=row.id,
            voter_id=row.voter_id,
            voter_name=row.voter_name,
            candidate_id=row.candidate_id,
            candidate_name=row.candidate_name,
        )
        for row in rows
    ]


def get_vote_statistics(db: Session):

    total_voters_voted = (
        db.query(models.Voter).filter(models.Voter.has_voted == True).count()
    )

    total_votes = db.query(models.Vote).count()

    candidates_stats = (
        db.query(
            models.Candidate.id,
            models.Candidate.name,
            func.count(models.Vote.id).label("total_votes"),
        )
        .outerjoin(models.Vote)
        .group_by(models.Candidate.id, models.Candidate.name)
        .all()
    )

    candidates_statistics = []
    for candidate_id, candidate_name, votes_count in candidates_stats:
        votes_count = votes_count or 0
        percentage = (votes_count / total_votes * 100) if total_votes > 0 else 0

        candidates_statistics.append(
            schemas.CandidateStatistic(
                candidate_id=candidate_id,
                candidate_name=candidate_name,
                total_votes=votes_count,
                percentage=round(percentage, 2),
            )
        )

    return schemas.VoteStatisticsResponse(
        total_voters_voted=total_voters_voted,
        total_votes=total_votes,
        candidates_statistics=candidates_statistics,
    )


def get_candidates_votes_for_chart(db: Session):
    candidates_votes = (
        db.query(models.Candidate.name, func.count(models.Vote.id).label("votes"))
        .outerjoin(models.Vote)
        .group_by(models.Candidate.id, models.Candidate.name)
        .order_by(models.Candidate.name)
        .all()
    )

    return candidates_votes
