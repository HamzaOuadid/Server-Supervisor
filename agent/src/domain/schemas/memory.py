from pydantic import BaseModel


class GetMemoryResponseSchema(BaseModel):

    usage: float
    total: float
    percent: float
