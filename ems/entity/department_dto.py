from sqlalchemy import Column, String, Text, TIMESTAMP
from ems.entity import Base


class DepartmentDTO(Base):
    __tablename__ = "department"

    department_id = Column(String(25), primary_key=True, index=True)
    name = Column(String(25), nullable=False, unique=True)
    location = Column(String(50), nullable=False)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False)
    created_by = Column(Text, nullable=False)
    updated_on = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_by = Column(Text, nullable=True)
