from functools import lru_cache
from typing import List, Any
from ems.entity.department_dto import DepartmentDTO
from ems.entity.employee_dto import EmployeeDTO
from ems.entity.salary_breakup_dto import SalaryBreakupDTO
from ems.repository.base_repository import BaseLayer


@lru_cache()
def department_repository():
    return DepartmentRepository()

class DepartmentRepository(BaseLayer):

    def __init__(self):
        super().__init__()


    def find_all(self) -> List[DepartmentDTO]:
        """
        This function returns all department details
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(DepartmentDTO, order_by=(DepartmentDTO.department_id.asc()))
        return db_out_put


    def find_by_id(self, id) -> DepartmentDTO:
        """
        This function returns department details by department id
        :param id:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(DepartmentDTO, where=(DepartmentDTO.department_id == id), limit=1)
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def find_by_name(self, name) -> DepartmentDTO:
        """
        This function returns department details by department name
        :param name:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(DepartmentDTO, where=(DepartmentDTO.name == name), limit=1)
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def find_by_department_wise_employee(self) -> List[Any]:
        """
        This function returns department details with associate employees
        :return:
        """
        db_out_put = self.db_ob.execute_raw_query(f"SELECT DISTINCT a.name AS department_name, a.location, b.first_name || ' ' || b.last_name AS employee_name, b.date_of_birth, b.gender, b.nationality, b.hire_date, b.job_title, b.email, b.phone_number, b.address, c.basic_salary, c.allowances, c.deductions, c.total_salary "
                                                  f"FROM {DepartmentDTO.__tablename__} a "
                                                  f"LEFT JOIN {EmployeeDTO.__tablename__} b ON b.department_id=a.department_id " +
                                                  f"LEFT JOIN {SalaryBreakupDTO.__tablename__} c ON c.employee_id=c.employee_id " +
                                                  f"ORDER BY a.name DESC"
                                                )
        return db_out_put


    def merge(self, department: dict, session=None) -> Any:
        """
        This function merge department details
        :param department:
        :param session:
        :return:
        """
        if department["employee_id"] is not None:
            db_out_put = self.find_by_id(department["department_id"])
            if db_out_put is None:
                result = self.db_ob.insert_data(DepartmentDTO, department, session=session)
            else:
                result = self.db_ob.update_data(DepartmentDTO, where=(DepartmentDTO.employee_id == department["department_id"]), values=department, session=session)
        else:
            result = self.db_ob.insert_data(DepartmentDTO, department, session=session)

        return result


    def delete_by_id(self, id) -> Any:
        """
        This function delete department details by department id
        :param id:
        :return:
        """
        result = self.db_ob.delete_data(DepartmentDTO, where=(DepartmentDTO.employee_id == id))
        return result
