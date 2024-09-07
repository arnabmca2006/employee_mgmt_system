# employee-management-system

This project is to demonstrate how to develop Rest API using FastAPI, Uvicorn and SQLAlchemy with Authentication (Basic/Keycloak)


## Clone the project
```
git clone https://github.com/yasanthaniroshan/gfg-FastAPI_SQL_Databases.git
```

![Alt text](images/erd.png?raw=true "ER Diagram")

## Run application locally

### Install dependent libraries
```
pip install -r requirements.txt
```

Start the server
- for windows
```
  cd employee_mgmt_system
  pip install .
  set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application.yaml" & python ems/main.py
```
- for linux
```shell
  cd employee_mgmt_system
  pip install .
  export "PYTHONUNBUFFERED=1" && set "CONFIG_FILE=%cd%/ems/resources/application.yaml" && python ems/main.py
```

### To run the test cases

- run all the test case files
```
C:\employee_mgmt_system>set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" & pytest --verbose --color=yes
```
![Alt text](images/all_test_cases.png?raw=true "all_test_cases")

- run specific test case files
```
C:\employee_mgmt_system>set "PYTHONUNBUFFERED=1" & set "CONFIG_FILE=%cd%/ems/resources/application-local.yaml" & pytest ems/tests/test_department_service.py --verbose --color=yes
```
![Alt text](images/test_department_service.png?raw=true "test_department_service")


## To run pylint
```
pylint --rcfile .pylintrc ems/ -s y -r y --output pylint-report.txt
```



## Run in Docker

Start the application
```commandline
docker-compose up -d
```

Open the application in browser
```commandline
http://localhost:5000/docs
```

![Alt text](images/api_docs.png?raw=true "API Documentation")

![Alt text](images/api_docs_auth.png?raw=true "API Documentation with Auth")

Stop the application
```commandline
docker-compose stop
docker-compose rm
```



