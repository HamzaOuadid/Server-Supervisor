"""
This module defines a data transfer model for a GetCpuResponseSchema.
"""
from pydantic import BaseModel


class GetRamResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing RAM (Random Access Memory) information.

    Attributes:
        id (int): The ID of the RAM data.
        usage (str): The RAM usage in string format.
        capacity (int): The total capacity of RAM in megabytes.
    """

    usage: float
    capacity: float
    percent: float
