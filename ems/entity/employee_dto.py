from sqlalchemy import Column, String, Text, Date, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from ems.entity import Base
from ems.entity.department_dto import DepartmentDTO


class EmployeeDTO(Base):
    __tablename__ = "employee"

    employee_id = Column(String(25), primary_key=True, index=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(6), nullable=False)
    nationality = Column(String(20), nullable=False)
    hire_date = Column(Date, nullable=False)
    job_title = Column(String(20), nullable=False)
    email = Column(String(25), nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(50), nullable=False)
    salary = Column(Numeric, nullable=True, default=0.00)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False)
    created_by = Column(Text, nullable=False)
    updated_on = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_by = Column(Text, nullable=True)
    department_id = Column(String, ForeignKey(DepartmentDTO.department_id), nullable=False)
    department = relationship("DepartmentDTO", foreign_keys='EmployeeDTO.department_id')
