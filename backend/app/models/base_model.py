from sqlalchemy import Integer, Identity
from sqlalchemy.orm import mapped_column

from db.base_class import Base


class ORMBaseModel(Base):
    id = mapped_column(Integer, Identity(always=True), primary_key=True)
