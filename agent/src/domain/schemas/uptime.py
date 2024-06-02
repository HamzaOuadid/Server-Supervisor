from pydantic import BaseModel


class GetUptimeResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing system uptime information.

    Attributes:
        id (int): The ID of the uptime data.
        seconds (int): Uptime in seconds.
    """

    seconds: float
