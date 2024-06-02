from pydantic import BaseModel


class Memory(BaseModel):

    usage: float
    total: float
    percent: float
