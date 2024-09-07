import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Header
from ems.model.department import Department, DepartmentReq, CustomDepartment
from ems.model.response import Response
from ems.service.department_service import DepartmentService, department_service

router = APIRouter()

@router.get(
     "/",
     response_model=List[Department],
     summary="Fetch all available departments",
     description="Fetch all available domains.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_all(
        request: Request,
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> List[Department]:
    user = request.state.user_id
    logging.info(f"User is {user}")
    return service.fetch_all()


@router.get(
     "/{departmentId}",
     response_model=Department,
     summary="Fetch by department id",
     description="Fetch by specific employee id.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_by_department_id(
        departmentId: str,
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Department:
    return service.fetch_by_department_id(departmentId)


@router.get(
     "/employee/all",
     response_model=List[CustomDepartment],
     summary="Fetch department wise employee and salary breakup details",
     description="Fetch department wise employee and salary breakup details.",
     responses={
        200: {"description": "OK - Successfully fetch data"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def fetch_department_wise_employees(
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> List[CustomDepartment]:
    return service.fetch_department_wise_employees()


@router.post(
     "/",
     response_model=Response,
     summary="Add department details",
     description="Add department details.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        302: {"description": "Record already present"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        500: {"description": "Internal Server Error"}
    }
)
async def add_record(
        request: Request,
        department: DepartmentReq,
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.add_record(department, user)


@router.put(
     "/{departmentId}",
     response_model=Response,
     summary="Update department details by department id",
     description="Update department details by department id.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        302: {"description": "Record already present"},
        400: {"description": "Bad Request - Input data validation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def update_by_department_id(
        request: Request,
        departmentId: str,
        department: DepartmentReq,
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    user = request.state.user_id
    return service.update_by_department_id(departmentId, department, user)


@router.delete(
     "/{departmentId}",
     response_model=Response,
     summary="Delete department details by department id",
     description="Delete department details by department id.",
     responses={
        200: {"description": "OK - Successfully perform operation"},
        401: {"description": "Unauthorized access"},
        404: {"description": "Not Found - Record not found"},
        500: {"description": "Internal Server Error"}
    }
)
async def delete_by_department_id(
        request: Request,
        departmentId: str,
        service: DepartmentService = Depends(department_service),
        Accept: Optional[str] = Header("application/json", description="Accepted content types"),
        Content_Type: Optional[str] = Header("application/json", description="Accepted content types")
    ) -> Response:
    return service.delete_by_department_id(departmentId)
