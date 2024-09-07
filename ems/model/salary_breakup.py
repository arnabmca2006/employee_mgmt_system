from typing import Optional
from pydantic import Field
from ems.model import EMSBaseModel


class SalaryBreakupReq(EMSBaseModel):
    effective_date: Optional[str] = Field(None, alias="effectiveDate")
    basic_salary: Optional[float] = Field(0.0, alias="basicSalary")
    allowances: Optional[float] = 0.0
    deductions: Optional[float] = 0.0

class SalaryBreakup(EMSBaseModel):
    salary_id: int = Field(alias="salaryId")
    effective_date: str = Field(alias="effectiveDate")
    basic_salary: float = Field(alias="basicSalary")
    allowances: float
    deductions: float
    total_salary: float = Field(alias="totalSalary")
    created_on: str = Field(alias="createdOn")
    created_by: str = Field(alias="createdBy")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    employee_id: str = Field(alias="employeeId")
