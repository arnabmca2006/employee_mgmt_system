from sqlalchemy import Column, String, Text, Date, BigInteger, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from ems.entity import Base
from ems.entity.employee_dto import EmployeeDTO


class SalaryBreakupDTO(Base):
    __tablename__ = "salary_breakup"

    salary_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    effective_date = Column(Date, nullable=False)
    basic_salary = Column(Numeric, nullable=False, default=0.00)
    allowances = Column(Numeric, nullable=False, default=0.00)
    deductions = Column(Numeric, nullable=False, default=0.00)
    total_salary = Column(Numeric, nullable=False, default=0.00)
    created_on = Column(TIMESTAMP(timezone=True), nullable=False)
    created_by = Column(Text, nullable=False)
    updated_on = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_by = Column(Text, nullable=True)
    employee_id = Column(String(25), ForeignKey(EmployeeDTO.employee_id), nullable=False)
    employee = relationship("EmployeeDTO", foreign_keys='SalaryBreakupDTO.employee_id')
