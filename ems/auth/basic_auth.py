from http import HTTPStatus
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

users = {
    "admin": {
        "password": "admin",
        "roles": ["admin"],
        "token": "",
        "priviliged": True
    }
}

def verification(creds: HTTPBasicCredentials = Depends(security), request: Request=Request):
    """

    :param creds:
    :param request:
    :return:
    """
    username = creds.username
    password = creds.password
    if username in users and password == users[username]["password"]:
        request.state.user_id = username
        request.state.auth_token = ""
        return username
    else:
        # From FastAPI
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Basic"})
