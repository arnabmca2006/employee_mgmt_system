import logging
import os
from http import HTTPStatus
import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ems.auth.keycloak_service import KeyCloakAuth
from ems.auth.basic_auth import verification
from ems.util.utils import customize_openapi
from ems.util.configuration import Configuration

from ems.controller.default_controller import router as DefaultController
from ems.controller.department_controller import router as DepartmentController
from ems.controller.employee_controller import router as EmployeeController
from ems.controller.salary_breakup_controller import router as SalaryController


version = os.environ.get('APP_VERSION', '1.0.0')
contact = {"name": "Support Team", "email": "support@test.com"}
license_info = {"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html"}
servers = [
    {"url": "http://localhost:5000", "description": "Local application server"},
]
tags_metadata = [
    {"name": "default", "description": "**Operations related to default services**"},
    {"name": "department-service", "description": "**Operations related to department services**"},
    {"name": "employee-service", "description": "**Operations related to employee services**"},
    {"name": "salary-breakup-service", "description": "**Operations related to salary breakup services**"},
]

app = FastAPI(
    title="employee management system",
    description="API for employee management system",
    version=version,
    contact=contact,
    license_info=license_info,
    servers=servers,
    openapi_tags=tags_metadata,
    debug=False)

# Read resources
CONFIG_FILE_LOCATION = os.environ.get('CONFIG_FILE', "resources/application.yaml")
app.config = Configuration()
WEB_SERVER_PORT = app.config.configuration["server.port"]
WEB_SERVER_IP = os.environ.get('WEB_SERVER_IP', '0.0.0.0')

AUTH_LIST = []
if app.config.configuration["auth.method"] and app.config.configuration["auth.method"].lower().strip() == 'basic':
    AUTH_LIST.append(Depends(verification))
elif app.config.configuration["auth.method"] and app.config.configuration["auth.method"].lower().strip() == 'keycloak':
    app.authenticator = KeyCloakAuth()
    AUTH_LIST.append(Depends(app.authenticator.has_access))


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={"detail": "Validation error", "errors": exc.errors()[0]['msg']}
    )
app.openapi = customize_openapi(app.openapi)


app.include_router(DefaultController, prefix="", tags=["default"])
app.include_router(DepartmentController, prefix="/api/v1/department", tags=["department-service"], dependencies=AUTH_LIST)
app.include_router(EmployeeController, prefix="/api/v1/employee", tags=["employee-service"], dependencies=AUTH_LIST)
app.include_router(SalaryController, prefix="/api/v1/salary-breakup", tags=["salary-breakup-service"], dependencies=AUTH_LIST)

def main():
    config = uvicorn.Config("main:app", host=WEB_SERVER_IP, port=WEB_SERVER_PORT, use_colors=False, reload=False)
    server = uvicorn.Server(config)
    try:
        server.run()
    except KeyboardInterrupt:
        logging.info("Caught Ctrl+C. Exiting gracefully.")


if __name__ == '__main__':
    main()
