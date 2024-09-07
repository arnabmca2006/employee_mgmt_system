from typing import Optional
from pydantic import Field
from ems.model import EMSBaseModel


class Response(EMSBaseModel):
    status_code: int = Field(alias="statusCode")
    message: Optional[str] = ""
