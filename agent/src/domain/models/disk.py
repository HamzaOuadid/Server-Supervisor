from pydantic import BaseModel


# Disk data model
class Disk(BaseModel):
    """
    Pydantic data model for representing disk information.

    Attributes:
        id (int): The ID of the disk data.
        total_space (int): Total disk space in bytes.
        used_space (int): Used disk space in bytes.
        free_space (int): Free disk space in bytes.
        usage_percent (float): Disk usage percentage.
    """

    total_space: float
    used_space: float
    usage_percent: float
