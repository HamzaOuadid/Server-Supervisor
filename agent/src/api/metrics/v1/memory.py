from typing import List
from fastapi import APIRouter, Request
from domain.schemas import GetMemoryResponseSchema
from domain.services import MemoryService

memory_router = APIRouter()


@memory_router.get(
    "/usage",
    response_model=GetMemoryResponseSchema)
async def get_ram(request: Request) -> GetMemoryResponseSchema:
    return await MemoryService().get_memory(request.app.state.monitortask)
