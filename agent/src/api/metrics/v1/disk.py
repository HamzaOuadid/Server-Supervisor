from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetDiskResponseSchema,
)
from domain.services import DiskService

disk_router = APIRouter()


@disk_router.get(
    "/info",
    response_model=List[GetDiskResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_disk_info(request: Request) -> List[GetDiskResponseSchema]:
    """
    Route to get a list of disk information.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetDiskResponseSchema]: A list of disk information as per the response model.
    """
    return await DiskService().get_disk(request.app.state.monitortask)
