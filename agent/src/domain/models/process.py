from pydantic import BaseModel
from typing import List


# Process data model
class Process(BaseModel):
    """
    Pydantic data model for representing process information.

    Attributes:
        id (int): The ID of the process data.
        name (str): The name of the process.
        cpu_percent (float): CPU usage percentage by the process.
        memory_percent (float): Memory usage percentage by the process.
    """

    id: int
    name: str
    cpu_percent: float
    memory_percent: float

# ProcessList data model
class ProcessList(BaseModel):
    """
    Pydantic data model for representing a list of processes.

    Attributes:
        processes (List[Process]): List of Process objects.
    """

    processes: List[Process]
