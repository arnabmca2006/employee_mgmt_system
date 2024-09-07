from typing import Optional
from pydantic import Field
from ems.model import EMSBaseModel


class EmployeeReq(EMSBaseModel):
    employee_id: Optional[str] = Field(None, alias="employeeId")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    gender: Optional[str] = None
    nationality: Optional[str] = None
    hire_date: Optional[str] = Field(None, alias="hireDate")
    job_title: Optional[str] = Field(None, alias="jobTitle")
    email: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    address: Optional[str] = None

class Employee(EMSBaseModel):
    employee_id: str = Field(alias="employeeId")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    date_of_birth: str = Field(alias="dateOfBirth")
    gender: str = None
    nationality: str
    hire_date: str = Field(alias="hireDate")
    job_title: str = Field(alias="jobTitle")
    email: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    address: str
    salary: float
    created_on: str = Field(alias="createdOn")
    created_by: str = Field(alias="createdBy")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    department_id: Optional[str] = Field(None, alias="departmentId")

class CustomEmployee(EMSBaseModel):
    employee_name: str = Field(alias="firstName")
    date_of_birth: str = Field(alias="dateOfBirth")
    gender: str = None
    nationality: str
    hire_date: str = Field(alias="hireDate")
    job_title: str = Field(alias="jobTitle")
    email: Optional[str] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    address: str
    basic_salary: float = Field(alias="basicSalary")
    allowances: float
    deductions: float
    total_salary: float = Field(alias="totalSalary")
