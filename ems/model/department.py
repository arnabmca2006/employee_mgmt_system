from typing import Optional
from pydantic import Field
from ems.model import EMSBaseModel


class DepartmentReq(EMSBaseModel):
    department_id: Optional[str] = Field(None, alias="departmentId")
    name: Optional[str] = None
    location: Optional[str] = None

class Department(EMSBaseModel):
    department_id: str = Field(alias="departmentId")
    name: str
    location: str
    created_on: str = Field(alias="createdOn")
    created_by: str = Field(alias="createdBy")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    updated_by: Optional[str] = Field(None, alias="updatedBy")

class CustomDepartment(EMSBaseModel):
    department_name: str = Field(alias="departmentName")
    location: str
    employee_name: str = Field(alias="employeeName")
    date_of_birth: str = Field(alias="dateOfBirth")
    gender: str
    nationality: str
    hire_date: str = Field(alias="hireDate")
    job_title: str = Field(alias="jobTitle")
    email: str
    phone_number: str = Field(alias="phoneNumber")
    address: str
    basic_salary: float = Field(0.0, alias="basicSalary")
    allowances: float = 0.0
    deductions: float = 0.0
    total_salary: float = Field(0.0, alias="totalSalary")
