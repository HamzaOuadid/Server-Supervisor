from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetUptimeResponseSchema,
)
from domain.services import UptimeService

uptime_router = APIRouter()


@uptime_router.get(
    "/info",
    response_model=GetUptimeResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_uptime_info(request: Request) -> GetUptimeResponseSchema:
    """
    Route to get information about system uptime.

    Args:
        request (Request): The incoming request.

    Returns:
        GetUptimeResponseSchema: Information about system uptime.
    """
    return await UptimeService().get_uptime(request.app.state.monitortask)
