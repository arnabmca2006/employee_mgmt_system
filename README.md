# employee-management-system

This sample application demonstrate how to develop Rest API using FastAPI, Uvicorn and SQLAlchemy with Authentication (Basic/Keycloak)


## Clone the sample code of the application
```
git clone https://github.com/arnabmca2006/employee_mgmt_system.git
```


## ER diagram for database tables
![Alt text](images/erd.png?raw=true "ER Diagram")


## Run application locally

### Install dependent libraries
```
pip install -r requirements.txt
```

### Start the server
- for windows
```
  cd employee_mgmt_system
  pip install .
  set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" & python ems/main.py
```
- for linux
```
  cd employee_mgmt_system
  pip install .
  export "PYTHONUNBUFFERED=1" && set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" && python ems/main.py
```

### Open the application in browser
For basic authentication, ter Username and password as admin
```
http://localhost:5000/docs
```
![Alt text](images/api_docs.png?raw=true "API Documentation")
![Alt text](images/api_docs_auth.png?raw=true "API Documentation with Auth")

### To run the test cases
- Run all the test case files
```
C:\employee_mgmt_system>set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" & pytest --verbose --color=yes
```
![Alt text](images/all_test_cases.png?raw=true "all_test_cases")
- Run specific test case files
```
C:\employee_mgmt_system>set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" & pytest ems/tests/test_department_service.py --verbose --color=yes
```
![Alt text](images/test_department_service.png?raw=true "test_department_service")

### To run pylint
```
pylint --rcfile .pylintrc ems/ -s y -r y --output pylint-report.txt
```


## Run as Docker container

- Start the application
```
docker-compose up -d
```

- Stop and remove all containers of the application
```
docker-compose stop
docker-compose rm
```

