from pydantic import BaseModel


# Uptime data model
class Uptime(BaseModel):
    """
    Pydantic data model for representing system uptime information.

    Attributes:
        id (int): The ID of the uptime data.
        seconds (int): Uptime in seconds.
    """

    seconds: float
