from pydantic import BaseModel

class DeviceVariant(BaseModel):
    id: str
    model: str
    storage_gb: int
    color: str
    active: bool