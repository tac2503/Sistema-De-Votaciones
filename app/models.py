from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    has_voted = Column(Boolean, default=False)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    votes = Column(Integer, default=0)


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id"), nullable=False, index=True)
    candidate_id = Column(
        Integer, ForeignKey("candidates.id"), nullable=False, index=True
    )

    voter = relationship("Voter")
    candidate = relationship("Candidate")
