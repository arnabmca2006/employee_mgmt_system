import logging
from functools import lru_cache
from http import HTTPStatus
from typing import List
from fastapi import HTTPException
from ems.model.employee import Employee, CustomEmployee
from ems.model.response import Response
from ems.repository.department_repository import DepartmentRepository
from ems.repository.employee_repository import EmployeeRepository
from ems.service.base_service import BaseLayer
from ems.util.utils import fetch_not_null_dict, get_current_time


@lru_cache()
def employee_service():
    return EmployeeService()

class EmployeeService(BaseLayer):

    def __init__(self):
        super().__init__()
        self.department_repository = DepartmentRepository()
        self.employee_repository = EmployeeRepository()


    def fetch_all(self) -> List[Employee]:
        """
        This function returns all employee details
        :return:
        """
        logging.info("Fetch all employees")

        res = []
        db_out_put = self.employee_repository.find_all()
        if db_out_put is not None and len(db_out_put) > 0:
            for row in db_out_put:
                res.append(
                    Employee(
                        employee_id=row.employee_id,
                        first_name=row.first_name,
                        last_name=row.last_name,
                        date_of_birth=str(row.date_of_birth),
                        gender=row.gender,
                        nationality=row.nationality,
                        hire_date=str(row.hire_date),
                        job_title=row.job_title,
                        email=row.email,
                        phone_number=row.phone_number,
                        address=row.address,
                        salary=row.salary,
                        created_on=str(row.created_on),
                        created_by=row.created_by,
                        updated_on=str(row.updated_on) if row.updated_on is not None else None,
                        updated_by=row.updated_by if row.updated_by is not None else None,
                        department_id=row.department_id
                    )
                )

        return res


    def fetch_by_employee_id(self, employee_id) -> Employee:
        """
        This function returns employee details of a specific deployee id
        :param employee_id:
        :return:
        """
        logging.info("Fetch employee by employee id")

        db_out_put = self.employee_repository.find_by_id(employee_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Selected employee details not found")

        row = db_out_put
        return Employee(
            employee_id=row.employee_id,
            first_name=row.first_name,
            last_name=row.last_name,
            date_of_birth=str(row.date_of_birth),
            gender=row.gender,
            nationality=row.nationality,
            hire_date=str(row.hire_date),
            job_title=row.job_title,
            email=row.email,
            phone_number=row.phone_number,
            address=row.address,
            salary=row.salary,
            created_on=str(row.created_on),
            created_by=row.created_by,
            updated_on=str(row.updated_on) if row.updated_on is not None else None,
            updated_by=row.updated_by if row.updated_by is not None else None,
            department_id=row.department_id
        )


    def fetch_employee_wise_salary_breakup(self) -> List[CustomEmployee]:
        """
        This function returns employee details with associate salary breakup
        :return:
        """
        logging.info("Fetch department wise employees")

        res = []
        db_out_put = self.employee_repository.find_by_employee_wise_salary_breakup()
        if db_out_put is not None and len(db_out_put) > 0:
            for row in db_out_put:
                res.append(
                    CustomEmployee(
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


    def add_by_department_id(self, department_id, employee, user) -> Response:
        """
        This function insert employee details under specific department
        :param department_id:
        :param employee:
        :param user:
        :return:
        """
        logging.info("Add employee by department id")

        db_out_put = self.department_repository.find_by_id(department_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified department id not found")

        db_out_put = self.employee_repository.find_by_id(employee.employee_id)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Employee id already present")

        db_out_put = self.employee_repository.find_by_first_name_and_last_name(employee.first_name, employee.last_name)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Employee name already present")

        employee_dto = {
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "date_of_birth": str(employee.date_of_birth),
            "gender": employee.gender,
            "nationality": employee.nationality,
            "hire_date": str(employee.hire_date),
            "job_title": employee.job_title,
            "email": employee.email,
            "phone_number": employee.phone_number,
            "address": employee.address,
            "created_on": get_current_time(),
            "created_by": user,
            "department_id": department_id
        }

        self.employee_repository.merge(employee_dto)
        return Response(status_code=HTTPStatus.OK, message="Successfully added employee details")


    def update_by_employee_id(self, employee_id, employee, user) -> Response:
        """
        This function update employee details for a specific employee id
        :param employee_id:
        :param employee:
        :param user:
        :return:
        """
        logging.info("Update employee details by employee id")

        db_out_put = self.employee_repository.find_by_id(employee_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified employee id not found")

        db_out_put = self.employee_repository.find_by_first_name_and_last_name(employee.first_name, employee.last_name)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Employee name already present")

        employee_dto = fetch_not_null_dict(employee)
        employee_dto["employee_id"] = employee_id
        employee_dto["updated_on"] = get_current_time()
        employee_dto["updated_by"] = user

        self.employee_repository.merge(employee_dto)
        return Response(status_code=HTTPStatus.OK, message="Successfully updated employee details")


    def delete_by_employee_id(self, employee_id) -> Response:
        """
        This function delete department details for a specific employee id
        :param employee_id:
        :return:
        """
        logging.info("Delete employee details by employee id")

        db_out_put = self.employee_repository.find_by_id(employee_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified employee id not found")

        self.employee_repository.delete_by_id((employee_id))
        return Response(status_code=HTTPStatus.OK, message="Successfully deleted employee details")
