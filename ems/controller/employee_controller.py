import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Header
from ems.model.employee import Employee, EmployeeReq, CustomEmployee
from ems.model.response import Response
from ems.service.employee_service import EmployeeService, employee_service

router = APIRouter()

@router.get(
     "/",
     response_model=List[Employee],
     summary="Fetch all available employees",
     description="Fetch all available domains.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_all(
        request: Request,
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> List[Employee]:
    user = request.state.user_id
    logging.info(f"User is {user}")
    return service.fetch_all()


@router.get(
     "/{employeeId}",
     response_model=Employee,
     summary="Fetch by employee id",
     description="Fetch by specific employee id.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found -record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_by_employee_id(
        employeeId: str,
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Employee:
    return service.fetch_by_employee_id(employeeId)


@router.get(
     "/salary-breakup",
     response_model=List[CustomEmployee],
     summary="Fetch employee wise salary breakup details",
     description="Fetch employee wise salary breakup details.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_department_wise_employees(
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> List[CustomEmployee]:
    return service.fetch_employee_wise_salary_breakup()


@router.post(
     "/department/{departmentId}",
     response_model=Response,
     summary="Add employee details for specific department",
     description="Add employee details for specific department.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        302: {"description": "Record already present"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def add_by_department_id(
        request: Request,
        departmentId: str,
        employee: EmployeeReq,
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.add_by_department_id(departmentId, employee, user)


@router.put(
     "/{employeeId}",
     response_model=Response,
     summary="Update employee details by employee id",
     description="Update employee details by employee id.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        302: {"description": "Record already present"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def update_by_employee_id(
        request: Request,
        employeeId: str,
        employee: EmployeeReq,
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.update_by_employee_id(employeeId, employee, user)


@router.delete(
     "/{employeeId}",
     response_model=Response,
     summary="Delete employee details by employee id",
     description="Delete employee details by employee id.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def delete_by_employee_id(
        employeeId: str,
        service: EmployeeService = Depends(employee_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    return service.delete_by_employee_id(employeeId)
