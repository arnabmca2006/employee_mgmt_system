import logging
from http import HTTPStatus
import sys
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID, KeycloakConnectionError
from ems.util.configuration import Configuration

app_config = Configuration()

class KeyCloakAuth:
    """
    This class intercept all API calls between HTTP APIs and all service routers. Extract the token and introspect the token
    to get the user information and user role.
    """

    def __init__(self):
        """
        Load all required configuration for accessing key-cloak APIs
        The mandatory parameters are keycloak.url, keycloak.realm & keycloak.client_id
        """
        kck_server = app_config.configuration["keycloak"]["url"]
        kck_realm = app_config.configuration["keycloak"]["realm"]
        kck_client = app_config.configuration["keycloak"]["client_id"]
        kck_client_secret = app_config.configuration["keycloak"]["client_secret"]
        #Checking for key-cloak certificate
        kc_cert = False
        if len(app_config.configuration["keycloak"]["https_cert"]) > 0 and str(app_config.configuration["keycloak"]["https_cert"]).lower() != "false" :
            kc_cert = app_config.configuration["keycloak"]["https_cert"]
            logging.info('key-cloak certificate available in : [%s]', kc_cert)
        else:
            logging.warning('no key-cloak certificate available in : [%s]', app_config.configuration["keycloak"]["https_cert"])
        logging.info('--Initializing KeyCloak--')
        logging.info("KeyCloak Server: %s", kck_server)
        logging.info("KeyCloak Realm: %s", kck_realm)
        logging.info("KeyCloak Client: %s", kck_client)
        logging.info("KeyCloak Certificate: %s", kc_cert)
        logging.info("KeyCloak Client-Secret: %s", kck_client_secret)

        if not kck_server or len(kck_server) == 0:
            logging.error('Key-Cloak URL can not be null or empty if KeyCloakAuth is enable')
            sys.exit(1)

        if not kck_realm or len(kck_realm) == 0:
            logging.error('Key-Cloak realm can not be null or empty if KeyCloakAuth is enable')
            sys.exit(1)

        if not kck_client or len(kck_client) == 0:
            logging.error('Key-Cloak client can not be null or empty if KeyCloakAuth is enable')
            sys.exit(1)
        self.kck_open_id = KeycloakOpenID(server_url=kck_server, client_id=kck_client, realm_name=kck_realm, client_secret_key=kck_client_secret, verify=kc_cert)

    @staticmethod
    def has_access(credentials: HTTPAuthorizationCredentials=Depends(HTTPBearer()), request: Request=Request):
        """
        This static method invoked for every call intercepted before going to router services.
        With successful validation it allows to process to router service, or else it raises HTTP UNAUTHORIZED error.
        Arguments:
            credentials - The access token pass by client.
            request - the http request object holding all call details.
        """
        access_token = None
        try:
            access_token = credentials.credentials.strip()
        except Exception as data_error:
            logging.error("Invalid Token - %s", str(access_token))
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value, detail="Failed to extract access token or token is null") from data_error

        logging.debug("KeyCloak Interceptor start. Token: %s", access_token)
        try:
            userinfo = request.app.authenticator.kck_open_id.userinfo(access_token)
            request.state.user_id = userinfo['preferred_username']
            logging.debug('User-Info: %s', str(userinfo))
            logging.debug("User authenticated: %s", userinfo['preferred_username'])
        except KeycloakConnectionError as connection_error:
            logging.error("Unable to connect Keycloak service. Error - %s", str(connection_error))
            raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE.value, detail='Unable to connect Keycloak service ' + str(connection_error)) from connection_error
        except Exception as validation_error:
            logging.error("Invalid Token/User details. Error - %s", str(validation_error))
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED.value, detail='Invalid User / Access Token ' + str(validation_error)) from validation_error

        try:
            token_info = request.app.authenticator.kck_open_id.introspect(access_token)
            request.state.user_roles = token_info['realm_access']['roles']
            logging.debug("User Roles: %s", str(token_info['realm_access']['roles']))
        except KeycloakConnectionError as connection_error:
            logging.error("Unable to connect Keycloak service. Error - %s", str(connection_error))
        except Exception as validation_error:
            logging.warning("Failed to get user-role from token, Setting default-role, Error %s", str(validation_error))
