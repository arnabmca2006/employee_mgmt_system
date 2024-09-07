import logging
from typing import Optional
from fastapi import APIRouter, Depends, Request, Header
from ems.model.response import Response
from ems.model.salary_breakup import SalaryBreakup, SalaryBreakupReq
from ems.service.salary_breakup_service import SalaryBreakupService, salary_breakup_service

router = APIRouter()

@router.get(
     "/employee/{employeeId}",
     response_model=SalaryBreakup,
     summary="Fetch salary details by employee id",
     description="Fetch salary details by employee id.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_by_employee_id(
        request: Request,
        employeeId: str,
        service: SalaryBreakupService = Depends(salary_breakup_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> SalaryBreakup:
    user = request.state.user_id
    logging.info(f"User is {user}")
    return service.fetch_by_employee_id(employeeId)


@router.post(
     "/employee/{employeeId}",
     response_model=Response,
     summary="Add salary breakup details for specific employee",
     description="Add salary breakup details for specific employee.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        302: {"description": "Record already present"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def add_by_employee_id(
        request: Request,
        employeeId: str,
        salary_breakup: SalaryBreakupReq,
        service: SalaryBreakupService = Depends(salary_breakup_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.add_by_employee_id(employeeId, salary_breakup, user)


@router.put(
     "/{salaryId}",
     response_model=Response,
     summary="Update salary breakup details by salary breakup id",
     description="Update salary breakup details by salary breakup id.",
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
        salaryId: int,
        salary_breakup: SalaryBreakupReq,
        service: SalaryBreakupService = Depends(salary_breakup_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.update_by_salary_id(salaryId, salary_breakup, user)


@router.delete(
     "/{salaryId}",
     response_model=Response,
     summary="Delete salary breakup details by salary id",
     description="Delete salary breakup details by salary id.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def delete_by_salary_id(
        request: Request,
        salaryId: int,
        service: SalaryBreakupService = Depends(salary_breakup_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    return service.delete_by_salary_id(salaryId)
