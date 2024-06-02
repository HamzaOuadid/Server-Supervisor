from pydantic import BaseModel
from typing import List

from typing import List


class GetProcessResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing process information.

    Attributes:
        id (int): The ID of the process data.
        id (int): The ID of the process data.
        name (str): The name of the process.
        cpu_percent (float): CPU usage percentage by the process.
        memory_percent (float): Memory usage percentage by the process.
        cpu_percent (float): CPU usage percentage by the process.
        memory_percent (float): Memory usage percentage by the process.
    """
    id: int
    name: str
    cpu_percent: float
    memory_percent: float

class GetProcessListResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing a list of processes.

    Attributes:
        processes (List[GetProcessResponseSchema]): List of process response schemas.
    """
    processes: List[GetProcessResponseSchema]
