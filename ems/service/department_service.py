import logging
from functools import lru_cache
from http import HTTPStatus
from typing import List
from fastapi import HTTPException
from ems.model.department import Department, CustomDepartment
from ems.model.response import Response
from ems.repository.department_repository import DepartmentRepository
from ems.service.base_service import BaseLayer
from ems.util.utils import fetch_not_null_dict, get_current_time


@lru_cache()
def department_service():
    return DepartmentService()

class DepartmentService(BaseLayer):

    def __init__(self):
        super().__init__()
        self.department_repository = DepartmentRepository()


    def fetch_all(self) -> List[Department]:
        """
        This function returns all department details
        :return:
        """
        logging.info("Fetch all departments")

        res = []
        db_out_put = self.department_repository.find_all()
        if db_out_put is not None and len(db_out_put) > 0:
            for row in db_out_put:
                res.append(
                    Department(
                        department_id=row.department_id,
                        name=row.name, location=row.location,
                        created_on=str(row.created_on),
                        created_by=row.created_by,
                        updated_on=str(row.updated_on) if row.updated_on is not None else None,
                        updated_by=row.updated_by if row.updated_by is not None else None
                    )
                )

        return res


    def fetch_by_department_id(self, department_id) -> Department:
        """
        This function returns department details of a specific department id
        :param department_id:
        :return:
        """
        logging.info("Fetch department by department id")

        db_out_put = self.department_repository.find_by_id(department_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Selected department details not found")

        row = db_out_put
        return Department(
            department_id=row.department_id,
            name=row.name,
            location=row.location,
            created_on=str(row.created_on),
            created_by=row.created_by,
            updated_on=str(row.updated_on) if row.updated_on is not None else None,
            updated_by=row.updated_by if row.updated_by is not None else None
        )


    def fetch_department_wise_employees(self) -> List[CustomDepartment]:
        """
        This function returns department details with associate employee and salary breakup
        :return:
        """
        logging.info("Fetch department wise employees")

        res = []
        db_out_put = self.department_repository.find_by_department_wise_employee()
        if db_out_put is not None and len(db_out_put) > 0:
            for row in db_out_put:
                res.append(
                    CustomDepartment(
                        department_name=row.department_name,
                        location=row.location,
                        employee_name=row.employee_name,
                        date_of_birth=str(row.date_of_birth) if row.date_of_birth is not None else None,
                        gender=row.gender, nationality=row.nationality,
                        hire_date=str(row.hire_date) if row.hire_date is not None else None,
                        job_title=row.job_title,
                        email=row.email,
                        phone_number=row.phone_number,
                        address=row.address,
                        basic_salary=row.basic_salary if row.basic_salary is not None else 0.0,
                        allowances=row.allowances if row.allowances is not None else 0.0,
                        deductions=row.deductions if row.deductions is not None else 0.0,
                        total_salary=row.total_salary if row.total_salary is not None else 0.0
                    )
                )

        return res


    def add_record(self, department, user) -> Response:
        """
        This function insert department details
        :param department:
        :param user:
        :return:
        """
        logging.info("Add department by department id")

        db_out_put = self.department_repository.find_by_id(department.department_id)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Department id already present")

        db_out_put = self.department_repository.find_by_name(department.name)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Department name already present")

        department_dto = {
            "department_id": department.department_id,
            "name": department.name,
            "location": department.location,
            "created_on": get_current_time(),
            "created_by": user
        }

        self.department_repository.merge(department_dto)
        return Response(status_code=HTTPStatus.OK, message="Successfully added department details")


    def update_by_department_id(self, department_id, department, user) -> Response:
        """
        This function update department details for a specific department id
        :param department_id:
        :param department:
        :param user:
        :return:
        """
        logging.info("Update department details by department id")

        db_out_put = self.department_repository.find_by_id(department_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified department id not found")

        db_out_put = self.department_repository.find_by_name(department.name)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Department name already present")

        department_dto = fetch_not_null_dict(department)
        department_dto["department_id"] = department_id
        department_dto["updated_on"] = get_current_time()
        department_dto["updated_by"] = user

        self.department_repository.merge(department_dto)
        return Response(status_code=HTTPStatus.OK, message="Successfully updated department details")


    def delete_by_department_id(self, department_id) -> Response:
        """
        This function delete department details for a specific department id
        :param department_id:
        :return:
        """
        logging.info("Delete department details by department id")

        db_out_put = self.department_repository.find_by_id(department_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified department id not found")

        self.department_repository.delete_by_id(department_id)
        return Response(status_code=HTTPStatus.OK, message="Successfully deleted department details")
