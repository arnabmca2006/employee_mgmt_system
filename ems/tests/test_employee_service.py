from unittest.mock import MagicMock
from http import HTTPStatus
from datetime import datetime
import pytest
from ems.entity.department_dto import DepartmentDTO
from ems.entity.employee_dto import EmployeeDTO
from ems.model.employee import Employee, EmployeeReq, CustomEmployee
from ems.model.response import Response
from ems.service.employee_service import EmployeeService
from ems.util.utils import get_current_time


class TestEmployeeService:

    department_id = 'D001'
    employee_id = 'E001'
    current_time = get_current_time()
    user = 'admin'

    @pytest.fixture
    def employee_service(self):
        instance = EmployeeService()
        instance.department_repository = MagicMock()
        instance.employee_repository = MagicMock()
        return instance

    def test_fetch_all(self, employee_service):
        """
        Test case for fetch_all method
        :param employee_service:
        :return:
        """
        mock_data = [
            EmployeeDTO(employee_id="E001", first_name="Alice", last_name="Johnson", date_of_birth=datetime(1985,2,15), gender="Female", nationality="American", hire_date=datetime(2010,5,1), job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address="123 Elm St, Springfield", salary=90000, created_on=str(self.current_time), created_by=self.user, department_id="D001"),
            EmployeeDTO(employee_id="E002", first_name="Bob", last_name="Smith", date_of_birth=datetime(1990,6,20), gender="Male", nationality="American", hire_date=datetime(2012,8,15), job_title="Project Manager", email="bob.smith@example.com", phone_number="555-5678", address="456 Oak St, Springfield", salary=110000, created_on=str(self.current_time), created_by=self.user, department_id="D001")
        ]
        expected_result = [
            Employee(employee_id="E001", first_name="Alice", last_name="Johnson", date_of_birth="1985-02-15 00:00:00", gender="Female", nationality="American", hire_date="2010-05-01 00:00:00", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address="123 Elm St, Springfield", salary=90000, created_on=str(self.current_time), created_by=self.user, department_id="D001"),
            Employee(employee_id="E002", first_name="Bob", last_name="Smith", date_of_birth="1990-06-20 00:00:00", gender="Male", nationality="American", hire_date="2012-08-15 00:00:00", job_title="Project Manager", email="bob.smith@example.com", phone_number="555-5678", address="456 Oak St, Springfield", salary=110000, created_on=str(self.current_time), created_by=self.user, department_id="D001")
        ]

        employee_service.employee_repository.find_all.return_value = mock_data
        result = employee_service.fetch_all()

        assert result == expected_result


    def test_fetch_by_employee_id(self, employee_service):
        """
        Test case for fetch_by_employee_id method
        :param employee_service:
        :return:
        """
        employee_dto = EmployeeDTO(employee_id="E001", first_name="Alice", last_name="Johnson", date_of_birth=datetime(1985,2,15), gender="Female", nationality="American", hire_date=datetime(2010,5,1), job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address="123 Elm St, Springfield", salary=90000, created_on=str(self.current_time), created_by=self.user, department_id="D001")
        expected_result = Employee(employee_id="E001", first_name="Alice", last_name="Johnson", date_of_birth="1985-02-15 00:00:00", gender="Female", nationality="American", hire_date="2010-05-01 00:00:00", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address="123 Elm St, Springfield", salary=90000, created_on=str(self.current_time), created_by=self.user, department_id="D001")

        employee_service.employee_repository.find_by_id.return_value = employee_dto
        result = employee_service.fetch_by_employee_id(self.employee_id)

        assert result == expected_result


    def test_fetch_employee_wise_salary_breakup(self, employee_service):
        """
        Test case for fetch_employee_wise_salary_breakup method
        :param employee_service:
        :return:
        """
        mock_data = [
            CustomEmployee(employee_name="Alice Johnson", date_of_birth="1985-02-15", gender="Female", nationality="American", hire_date="2010-05-01", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address= "123 Elm St, Springfield", basic_salary=0, allowances=0, deductions=0, total_salary=0)
        ]
        expected_result = [
            CustomEmployee(employee_name="Alice Johnson", date_of_birth="1985-02-15", gender="Female", nationality="American", hire_date="2010-05-01", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address= "123 Elm St, Springfield", basic_salary=0, allowances=0, deductions=0, total_salary=0)
        ]

        employee_service.employee_repository.find_by_employee_wise_salary_breakup.return_value = mock_data
        result = employee_service.fetch_employee_wise_salary_breakup()

        assert result == expected_result


    def test_add_by_department_id(self, employee_service):
        """
        Test case for add_by_department_id method
        :param employee_service:
        :return:
        """
        department_dto = DepartmentDTO(department_id='D001', name='Engineering', location='Springfield', created_on=self.current_time, created_by=self.user)
        employee = EmployeeReq(employee_id="E003", first_name="Carol", last_name="Davis", date_of_birth="11987-11-10", gender="Female", nationality="American", hire_date="2015-01-25", job_title="QA Analyst", email="carol.davis@example.com", phone_number="555-8765", address="789 Pine St, Springfield")
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully added employee details")

        employee_service.department_repository.find_by_id.return_value = department_dto
        employee_service.employee_repository.find_by_id.return_value = None
        employee_service.employee_repository.find_by_first_name_and_last_name.return_value = None
        employee_service.employee_repository.merge.return_value = None

        result = employee_service.add_by_department_id(self.department_id, employee, self.user)
        assert result == expected_result


    def test_update_by_employee_id(self, employee_service):
        """
        Test case for update_by_employee_id method
        :param employee_service:
        :return:
        """
        employee_dto = EmployeeDTO(employee_id="E003", first_name="Carol", last_name="Davis", date_of_birth=datetime(1987,11,10), gender="Female", nationality="American", hire_date=datetime(2015,1,25), job_title="QA Analyst", email="carol.davis@example.com", phone_number="555-8765", address="789 Pine St, Springfield", salary=85000, created_on=str(self.current_time), created_by=self.user, department_id="D002")
        employee = EmployeeReq(employee_id="E003", first_name="Carol", last_name="Davis", date_of_birth="11987-11-10", gender="Female", nationality="American", hire_date="2015-01-25", job_title="QA Analyst", email="carol.davis@example.com", phone_number="555-8765", address="789 Pine St, Springfield")
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully updated employee details")

        employee_service.employee_repository.find_by_id.return_value = employee_dto
        employee_service.employee_repository.find_by_first_name_and_last_name.return_value = None
        employee_service.employee_repository.merge.return_value = None

        result = employee_service.update_by_employee_id(self.employee_id, employee, self.user)
        assert result == expected_result


    def test_delete_by_employee_id(self, employee_service):
        """
        Test case for delete_by_employee_id method
        :param employee_service:
        :return:
        """
        employee_dto = EmployeeDTO(employee_id="E003", first_name="Carol", last_name="Davis", date_of_birth=datetime(1987,11,10), gender="Female", nationality="American", hire_date=datetime(2015,1,25), job_title="QA Analyst", email="carol.davis@example.com", phone_number="555-8765", address="789 Pine St, Springfield", salary=85000, created_on=str(self.current_time), created_by=self.user, department_id="D002")
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully deleted employee details")

        employee_service.employee_repository.find_by_id.return_value = employee_dto
        employee_service.employee_repository.delete_by_id.return_value = None

        result = employee_service.delete_by_employee_id(self.employee_id)
        assert result == expected_result


if __name__ == "__main__":
    pytest.main()
