from pydantic import BaseModel


class fileUploadResponse(BaseModel):
    original_name: str
    disk_name: str
    size: str
    url: str
