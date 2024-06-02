"""
This module defines API routes for handling RAM-related data.
"""
from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetRamResponseSchema,
)
from domain.services import RamService

ram_router = APIRouter()


@ram_router.get(
    "/usage",
    response_model=List[GetRamResponseSchema],
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_ram(request: Request) -> List[GetRamResponseSchema]:
    """
    Route to get a list of RAM data.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetRamResponseSchema]: A list of RAM data as per the response model.
    """
    return await RamService().get_ram(request.app.state.monitortask)
