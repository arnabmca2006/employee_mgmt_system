from functools import lru_cache
from typing import List, Any
from sqlalchemy import and_
from ems.entity.employee_dto import EmployeeDTO
from ems.entity.salary_breakup_dto import SalaryBreakupDTO
from ems.repository.base_repository import BaseLayer


@lru_cache()
def employee_repository():
    return EmployeeRepository()

class EmployeeRepository(BaseLayer):

    def __init__(self):
        super().__init__()


    def find_all(self) -> List[EmployeeDTO]:
        """
        This function returns all employee details
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(EmployeeDTO, order_by=(EmployeeDTO.employee_id.asc()))
        return db_out_put


    def find_by_id(self, id) -> EmployeeDTO:
        """
        This function returns employee details by employee id
        :param id:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(EmployeeDTO, where=(EmployeeDTO.employee_id == id), limit=1)
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def find_by_first_name_and_last_name(self, first_name, last_name) -> EmployeeDTO:
        """
        This function returns employee details by first name and last name
        :param first_name:
        :param last_name:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(EmployeeDTO, where=(
                                                                    and_(
                                                                       EmployeeDTO.first_name == first_name,
                                                                       EmployeeDTO.last_name == last_name
                                                                    )
                                                                 )
                                                               , limit=1
                                                    )
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def find_by_employee_wise_salary_breakup(self) -> List[Any]:
        """
        This function returns employee details with associate salary breakup
        :return:
        """
        db_out_put = self.db_ob.execute_raw_query(f"SELECT DISTINCT a.first_name || ' ' || a.last_name AS employee_name, a.date_of_birth, a.gender, a.nationality, a.hire_date, a.job_title, a.email, a.phone_number, a.address, b.basic_salary, b.allowances, b.deductions, b.total_salary "
                                                  f"FROM {EmployeeDTO.__tablename__} a " +
                                                  f"LEFT JOIN {SalaryBreakupDTO.__tablename__} b ON b.employee_id=a.employee_id " +
                                                  f"ORDER BY a.name DESC"
                                                )
        return db_out_put


    def merge(self, employee: dict, session=None) -> Any:
        """
        This function merge employee details
        :param employee:
        :param session:
        :return:
        """
        if employee["employee_id"] is not None:
            db_out_put = self.find_by_id(employee["employee_id"])
            if db_out_put is None:
                result = self.db_ob.insert_data(EmployeeDTO, employee, session=session)
            else:
                result = self.db_ob.update_data(EmployeeDTO, where=(EmployeeDTO.employee_id == employee["employee_id"]), values=employee, session=session)
        else:
            result = self.db_ob.insert_data(EmployeeDTO, employee, session=session)

        return result


    def delete_by_id(self, id) -> Any:
        """
        This function delete employee details by employee id
        :param id:
        :return:
        """
        result = self.db_ob.delete_data(EmployeeDTO, where=(EmployeeDTO.employee_id == id))
        return result
