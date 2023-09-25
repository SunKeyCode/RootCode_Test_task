import datetime

from pydantic import BaseModel, field_validator


class ReportModel(BaseModel):
    date: datetime.datetime
    plan: float | None = None
    fact: float | None = None

    @field_validator("plan")
    def round_plan(cls, plan: float) -> float:
        return round(plan, 2)

    @field_validator("fact")
    def round_fact(cls, fact: float) -> float:
        return round(fact, 2)

    class from_attributes:
        orm_mode = True
