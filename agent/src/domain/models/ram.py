"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel


class Ram(BaseModel):
    """
    Pydantic data model for representing RAM (Random Access Memory) information.

    Attributes:
        id (int): The ID of the RAM data.
        usage (str): The RAM usage in string format.
        capacity (int): The total capacity of RAM in megabytes.
    """

    usage: float
    capacity: float
    percent: float
