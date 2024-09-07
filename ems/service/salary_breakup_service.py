import logging
from functools import lru_cache
from http import HTTPStatus
from fastapi import HTTPException
from ems.model.response import Response
from ems.model.salary_breakup import SalaryBreakup, SalaryBreakupReq
from ems.repository.employee_repository import EmployeeRepository
from ems.repository.salary_breakup_repository import SalaryBreakupRepository
from ems.service.base_service import BaseLayer
from ems.util.utils import fetch_not_null_dict, get_current_time


@lru_cache()
def salary_breakup_service():
    return SalaryBreakupService()

class SalaryBreakupService(BaseLayer):

    def __init__(self):
        super().__init__()
        self.employee_repository = EmployeeRepository()
        self.salary_repository = SalaryBreakupRepository()


    def fetch_by_employee_id(self, employee_id) -> SalaryBreakup:
        """
        This function returns salary breakup details of a specific employee
        :param employee_id:
        :return:
        """
        logging.info("Fetch salary breakup by employee id")

        db_out_put = self.salary_repository.find_by_employee_id(employee_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Selected employee details not found")

        row = db_out_put
        return SalaryBreakup(
            salary_id=row.salary_id,
            effective_date=str(row.effective_date),
            basic_salary=row.basic_salary,
            allowances=row.allowances,
            deductions=row.deductions,
            total_salary=row.total_salary,
            created_on=str(row.created_on),
            created_by=row.created_by,
            updated_on=str(row.updated_on) if row.updated_on is not None else None,
            updated_by=row.updated_by if row.updated_by is not None else None,
            employee_id=row.employee_id
        )


    def add_by_employee_id(self, employee_id, salary_breakup, user) -> Response:
        """
        This function insert salary breakup details for a specific employee id
        :param employee_id:
        :param salary_breakup:
        :param user:
        :return:
        """
        logging.info("Add salary breakup by employee id")

        db_out_put = self.employee_repository.find_by_id(employee_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified employee id not found")

        db_out_put = self.salary_repository.find_by_employee_id(employee_id)
        if db_out_put is not None:
            raise HTTPException(status_code=HTTPStatus.FOUND, detail=f"Employee id already present")

        salary_breakup_dto = {
            "effective_date": salary_breakup.effective_date,
            "basic_salary": salary_breakup.basic_salary,
            "allowances": salary_breakup.allowances,
            "deductions": salary_breakup.deductions,
            "total_salary": (salary_breakup.basic_salary + salary_breakup.allowances) - salary_breakup.deductions,
            "created_on": get_current_time(),
            "created_by": user,
            "employee_id": employee_id
        }

        employee_dto = {"employee_id": employee_id, "salary": salary_breakup_dto["total_salary"], "updated_on": get_current_time(), "updated_by": user}

        with self.db_ob.Session() as session:
            try:
                self.employee_repository.merge(employee_dto, session)
                self.salary_repository.merge(salary_breakup_dto, session)
                session.commit()
                return Response(status_code=HTTPStatus.OK, message="Successfully added salary details")
            except Exception as e:
                logging.error(f"Error occurred during updating {e}", exc_info=True)
                session.rollback()
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


    def update_by_salary_id(self, salary_id, salary_breakup, user) -> Response:
        """
        This function update salary breakup details of a specific salary id
        :param salary_id:
        :param salary_breakup:
        :param user:
        :return:
        """
        logging.info("Update salary breakup details by salary id")

        db_out_put = self.salary_repository.find_by_id(salary_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified salary id not found")

        row = db_out_put
        employee_id = row.employee_id
        salary_breakup_req = SalaryBreakupReq(basic_salary=row.basic_salary, allowances=row.allowances, deductions=row.deductions)

        salary_breakup_dto = fetch_not_null_dict(salary_breakup)
        basic_salary = salary_breakup_dto["basic_salary"] if "basic_salary" in salary_breakup_dto else salary_breakup_req.basic_salary
        allowances = salary_breakup_dto["allowances"] if "allowances" in salary_breakup_dto else salary_breakup_req.allowances
        deductions = salary_breakup_dto["deductions"] if "deductions" in salary_breakup_dto else salary_breakup_req.deductions

        salary_breakup_dto["salary_id"] = salary_id
        salary_breakup_dto["total_salary"] = (basic_salary + allowances) - deductions
        salary_breakup_dto["updated_on"] = get_current_time()
        salary_breakup_dto["updated_by"] = user

        employee_dto = {"employee_id": employee_id, "salary": salary_breakup_dto["total_salary"], "updated_on": get_current_time(), "updated_by": user}

        with self.db_ob.Session() as session:
            try:
                self.employee_repository.merge(employee_dto, session)
                self.salary_repository.merge(salary_breakup_dto, session)
                session.commit()
                return Response(status_code=HTTPStatus.OK, message="Successfully updated salary details")
            except Exception as e:
                logging.error(f"Error occurred during updating {e}", exc_info=True)
                session.rollback()
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e))


    def delete_by_salary_id(self, salary_id) -> Response:
        """
        This function delete salary breakup details for a specific salary breakup id
        :param salary_id:
        :return:
        """
        logging.info("Delete salary breakup details by salary id")

        db_out_put = self.salary_repository.find_by_id(salary_id)
        if db_out_put is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Specified salary id not found")

        self.salary_repository.delete_by_id(salary_id)
        return Response(status_code=HTTPStatus.OK, message="Successfully deleted salary details")
