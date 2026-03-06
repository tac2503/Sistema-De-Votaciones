from pydantic import BaseModel, EmailStr, Field


class VoterCreate(BaseModel):
    name: str = Field(..., example="Juan Perez")
    email: EmailStr = Field(..., example="hola@gmail.com")


class VoterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    class Config:
        from_attributes = True


class DeleteVoterResponse(BaseModel):
    message: str


class CandidateCreate(BaseModel):
    name: str = Field(..., example="Juan Perez")
    party: str | None = None


class CandidateResponse(BaseModel):
    id: int
    name: str
    party: str | None = None
    votes: int

    class Config:
        from_attributes = True


class VoteCreate(BaseModel):
    voter_id: int = Field(..., example="Id del votante")
    candidate_id: int = Field(..., example="Id del candidato")


class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int

    class Config:
        from_attributes = True


class VoteListResponse(BaseModel):
    id: int
    voter_id: int
    voter_name: str
    candidate_id: int
    candidate_name: str


class CandidateStatistic(BaseModel):
    candidate_id: int
    candidate_name: str
    total_votes: int
    percentage: float


class VoteStatisticsResponse(BaseModel):
    total_voters_voted: int
    total_votes: int
    candidates_statistics: list[CandidateStatistic]
