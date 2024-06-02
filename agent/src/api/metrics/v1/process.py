from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetProcessResponseSchema,
    GetProcessListResponseSchema
)
from domain.services import ProcessService

process_router = APIRouter()

@process_router.get(
    "/processes",
    response_model=GetProcessListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_processes(request: Request) -> GetProcessListResponseSchema:
    """
    Route to get a list of processes.

    Args:
        request (Request): The incoming request.

    Returns:
        List[GetProcessResponseSchema]: A list of process data as per the response model.
    """
    return await ProcessService().get_processes(request.app.state.monitortask)


@process_router.get(
    "/process/{pid}",
    response_model=GetProcessResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_process_by_pid(request: Request, pid: int) -> GetProcessResponseSchema:
    """
    Route to get information about a specific process by its PID.

    Args:
        request (Request): The incoming request.
        pid (int): The process ID to search for.

    Returns:
        GetProcessResponseSchema: Process information as per the response model.
    """
    list_process = await ProcessService().get_processes(request.app.state.monitortask)
    for p in list_process.processes:
        if p.id == pid:
            return p
    raise HTTPException(status_code=404, detail="Item not found")
