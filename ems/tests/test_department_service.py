from unittest.mock import MagicMock
from http import HTTPStatus
import pytest
from ems.entity.department_dto import DepartmentDTO
from ems.model.department import Department, DepartmentReq, CustomDepartment
from ems.model.response import Response
from ems.service.department_service import DepartmentService
from ems.util.utils import get_current_time


class TestDepartmentService:

    department_id = 'D001'
    current_time = get_current_time()
    user = 'admin'


    @pytest.fixture
    def department_service(self):
        instance = DepartmentService()
        instance.department_repository = MagicMock()
        return instance


    def test_fetch_all(self, department_service):
        """
        Test case for fetch_all method
        :param department_service:
        :return:
        """
        mock_data = [
            DepartmentDTO(department_id='D001', name='Engineering', location='Springfield', created_on=self.current_time, created_by='admin'),
            DepartmentDTO(department_id='D002', name='CS-AIR', location='Springfield', created_on=self.current_time, created_by='admin')
        ]
        expected_result = [
            Department(department_id='D001', name='Engineering', location='Springfield', created_on=str(self.current_time), created_by=self.user),
            Department(department_id='D002', name="CS-AIR", location='Springfield', created_on=str(self.current_time), created_by=self.user)
        ]

        department_service.department_repository.find_all.return_value = mock_data
        result = department_service.fetch_all()

        assert result == expected_result


    def test_fetch_by_department_id(self, department_service):
        """
        Test case for fetch_by_department_id method
        :param department_service:
        :return:
        """
        mock_data = DepartmentDTO(department_id='D001', name='Engineering', location='Springfield', created_on=self.current_time, created_by=self.user)
        expected_result = Department(department_id='D001', name='Engineering', location='Springfield', created_on=str(self.current_time), created_by=self.user)

        department_service.department_repository.find_by_id.return_value = mock_data
        result = department_service.fetch_by_department_id(self.department_id)

        assert result == expected_result


    def test_fetch_department_wise_employees(self, department_service):
        """
        Test case for fetch_department_wise_employees method
        :param department_service:
        :return:
        """
        mock_data = [
            CustomDepartment(department_name="Engineering", location="Springfield", employee_name="Alice Johnson", date_of_birth="1985-02-15", gender="Female", nationality="American", hire_date="2010-05-01", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address= "123 Elm St, Springfield", basic_salary=0, allowances=0, deductions=0, total_salary=0)
        ]
        expected_result = [
            CustomDepartment(department_name="Engineering", location="Springfield", employee_name="Alice Johnson", date_of_birth="1985-02-15", gender="Female", nationality="American", hire_date="2010-05-01", job_title="Software Engineer", email="alice.johnson@example.com", phone_number="555-1234", address= "123 Elm St, Springfield", basic_salary=0, allowances=0, deductions=0, total_salary=0)
        ]

        department_service.department_repository.find_by_department_wise_employee.return_value = mock_data
        result = department_service.fetch_department_wise_employees()

        assert result == expected_result


    def test_add_record(self, department_service):
        """
        Test case for add_record method
        :param department_service:
        :return:
        """
        department = DepartmentReq(department_id='D001', name='Engineering', location='Springfield')
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully added department details")

        department_service.department_repository.find_by_id.return_value = None
        department_service.department_repository.find_by_name.return_value = None
        department_service.department_repository.merge.return_value = None

        result = department_service.add_record(department, self.user)
        assert result == expected_result


    def test_update_by_department_id(self, department_service):
        """
        Test case for update_by_department_id method
        :param department_service:
        :return:
        """
        department_dto = DepartmentDTO(department_id='D001', name='Engineering', location='Springfield', created_on=self.current_time, created_by=self.user)
        department = DepartmentReq(department_id='D001', name='Engineering', location='Springfield')
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully updated department details")

        department_service.department_repository.find_by_id.return_value = department_dto
        department_service.department_repository.find_by_name.return_value = None
        department_service.department_repository.merge.return_value = None

        result = department_service.update_by_department_id(self.department_id, department, self.user)
        assert result == expected_result


    def test_delete_by_department_id(self, department_service):
        """
        Test case for delete_by_department_id method
        :param department_service:
        :return:
        """
        mock_data = DepartmentDTO(department_id='D001', name='Engineering', location='Springfield')
        expected_result = Response(status_code=HTTPStatus.OK, message="Successfully deleted department details")

        department_service.department_repository.find_by_id.return_value = mock_data
        department_service.department_repository.delete_by_id.return_value = None

        result = department_service.delete_by_department_id(self.department_id)
        assert result == expected_result


if __name__ == "__main__":
    pytest.main()
