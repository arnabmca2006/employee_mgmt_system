from functools import lru_cache
from typing import Any
from ems.entity.salary_breakup_dto import SalaryBreakupDTO
from ems.repository.base_repository import BaseLayer


@lru_cache()
def salary_breakup_repository():
    return SalaryBreakupRepository()

class SalaryBreakupRepository(BaseLayer):

    def __init__(self):
        super().__init__()


    def find_by_id(self, id) -> SalaryBreakupDTO:
        """
        This function returns salary breakup details by salary breakup id
        :param id:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(SalaryBreakupDTO, where=(SalaryBreakupDTO.salary_id == id), limit=1)
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def find_by_employee_id(self, employee_id) -> SalaryBreakupDTO:
        """
        This function returns salary breakup details by employee id
        :param id:
        :return:
        """
        db_out_put = self.db_ob.execute_orm_query(SalaryBreakupDTO, where=(SalaryBreakupDTO.employee_id == employee_id), limit=1)
        return db_out_put[0] if db_out_put is not None and len(db_out_put) > 0 else None


    def merge(self, salary_breakup: dict, session=None) -> Any:
        """
        This function merge salary breakup details
        :param salary_breakup:
        :param session:
        :return:
        """
        if salary_breakup["salary_id"] is not None:
            db_out_put = self.find_by_id(salary_breakup["salary_id"])
            if db_out_put is None:
                result = self.db_ob.insert_data(SalaryBreakupDTO, salary_breakup, session=session)
            else:
                result = self.db_ob.update_data(SalaryBreakupDTO, where=(SalaryBreakupDTO.salary_id == salary_breakup["salary_id"]), values=salary_breakup, session=session)
        else:
            result = self.db_ob.insert_data(SalaryBreakupDTO, salary_breakup, session=session)

        return result


    def delete_by_id(self, id) -> Any:
        """
        This function delete salary breakup details by salary breakup id
        :param id:
        :return:
        """
        result = self.db_ob.delete_data(SalaryBreakupDTO, where=(SalaryBreakupDTO.salary_id == id))
        return result
