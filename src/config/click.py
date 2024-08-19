from pydantic import BaseModel


class ClickConfig(BaseModel):
    view: str
    sleep: int