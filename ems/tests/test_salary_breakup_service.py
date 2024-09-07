from unittest.mock import MagicMock
from datetime import datetime
from http import HTTPStatus
import pytest
from ems.entity.employee_dto import EmployeeDTO
from ems.entity.salary_breakup_dto import SalaryBreakupDTO
from ems.model.salary_breakup import SalaryBreakup, SalaryBreakupReq
from ems.model.response import Response
from ems.service.salary_breakup_service import SalaryBreakupService
from ems.util.utils import get_current_time


class TestSalaryBreakupService:

    employee_id = 'E001'
    salary_id = 1
    current_time = get_current_time()
    user = 'admin'

    @pytest.fixture
    def salary_breakup_service(self):
        instance = SalaryBreakupService()
        instance.db_ob = MagicMock()
        instance.employee_repository = MagicMock()
        instance.salary_repository = MagicMock()
        return instance

    def test_fetch_by_employee_id(self, salary_breakup_service):
        """
        Test case for fetch_by_employee_id method
        :param salary_breakup_service:
        :return:
        """
        salary_dto = SalaryBreakupDTO(salary_id=1, effective_date=datetime(2024, 1, 1), basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary= 54000.00, created_on=self.current_time, created_by=self.user, employee_id="E001")
        expected_result = SalaryBreakup(salary_id=1, effective_date="2024-01-01 00:00:00", basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary= 54000.00, created_on=str(self.current_time), created_by=self.user, employee_id="E001")

        salary_breakup_service.salary_repository.find_by_employee_id.return_value = salary_dto
        result = salary_breakup_service.fetch_by_employee_id(self.employee_id)

        assert result == expected_result


    def test_add_by_employee_id(self, salary_breakup_service):
        """
        Test case for add_by_employee_id method
        :param salary_breakup_service:
        :return:
        """
        employee_dto = EmployeeDTO(employee_id="E001", first_name="Alice", last_name="Johnson", date_of_birth=datetime(1985, 2, 15), gender="Female", nationality="American", hire_date=datetime(2010, 5, 1), job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address="123 Elm St, Springfield", salary=90000, created_on=str(self.current_time), created_by=self.user, department_id="D001")
        salary_breakup = SalaryBreakupReq(salary_id=1, effective_date="2024-01-01", basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary= 54000.00)
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully added salary details")

        salary_breakup_service.employee_repository.find_by_id.return_value = employee_dto
        salary_breakup_service.salary_repository.find_by_employee_id.return_value = None
        salary_breakup_service.employee_repository.merge.return_value = None
        salary_breakup_service.salary_repository.merge.return_value = None

        result = salary_breakup_service.add_by_employee_id(self.employee_id, salary_breakup, self.user)
        assert result == expected_result


    def test_update_by_salary_id(self, salary_breakup_service):
        """
        Test case for update_by_salary_id method
        :param salary_breakup_service:
        :return:
        """
        salary_dto = SalaryBreakupDTO(salary_id=1, effective_date=datetime(2024, 1, 1), basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary=54000.00, created_on=self.current_time, created_by=self.user, employee_id="E001")
        salary_breakup = SalaryBreakupReq(salary_id=1, effective_date="2024-01-01", basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary= 54000.00)
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully updated salary details")

        salary_breakup_service.salary_repository.find_by_id.return_value = salary_dto
        salary_breakup_service.employee_repository.merge.return_value = None
        salary_breakup_service.salary_repository.merge.return_value = None

        result = salary_breakup_service.update_by_salary_id(self.salary_id, salary_breakup, self.user)
        assert result == expected_result


    def test_delete_by_salary_id(self, salary_breakup_service):
        """
        Test case for delete_by_salary_id method
        :param salary_breakup_service:
        :return:
        """
        salary_dto = SalaryBreakupDTO(salary_id=1, effective_date=datetime(2024, 1, 1), basic_salary=50000.00, allowances=5000.00, deductions=1000.00, total_salary=54000.00, created_on=self.current_time, created_by=self.user, employee_id="E001")
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully deleted salary details")

        salary_breakup_service.salary_repository.find_by_id.return_value = salary_dto
        salary_breakup_service.salary_repository.delete_by_id.return_value = None

        result = salary_breakup_service.delete_by_salary_id(self.salary_id)
        assert result == expected_result


if __name__ == "__main__":
    pytest.main()
