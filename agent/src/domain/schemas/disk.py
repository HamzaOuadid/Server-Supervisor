from pydantic import BaseModel


class GetDiskResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing disk information.

    Attributes:
        id (int): The ID of the disk data.
        total_space (int): Total disk space in bytes.
        used_space (int): Used disk space in bytes.
        free_space (int): Free disk space in bytes.
        usage_percent (float): Disk usage percentage.
    """

    total_space: int
    used_space: int
    usage_percent: float
