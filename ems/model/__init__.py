from pydantic import BaseModel, ConfigDict

class EMSBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
