import uuid
from datetime import datetime
from typing import Callable
from ems.util.configuration import Configuration

app_config = Configuration()

def get_uuid():
    return uuid.uuid4()

def get_current_time():
    """
    This function returns current date and time
    :return:
    """
    return datetime.now()


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """
    This function customized openapi documentation
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs) -> dict:
        res = func(*args, **kwargs)
        if "info" in res:
            res["info"]["x-api-id"] = str(get_uuid())
            res["info"]["x-audience"] = "poc-application"

        for _, method_item in res.get("paths", {}).items():
            for _, param in method_item.items():
                responses = param.get("responses")
                # remove default 422 - the default 422 schema is HTTPValidationError
                if "422" in responses and responses["422"]["content"]["application/json"]["schema"]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]
        return res

    return wrapper


def fetch_not_null_dict(map_obj) -> dict:
    """
    This function returns modified dictionary where value is not null and length is non-zero
    :param map_obj:
    :return:
    """
    new_dict: dict = {}
    for attr, value in map_obj.__dict__.items():
        if value is not None:
            if isinstance(value, str) and len(value) > 0:
                new_dict[attr] = value
            elif isinstance(value, int) and value != 0:
                new_dict[attr] = value
            elif isinstance(value, float) and value != 0.0:
                new_dict[attr] = value

    return new_dict
