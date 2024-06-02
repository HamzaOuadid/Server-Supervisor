from typing import List
from fastapi import APIRouter, Request
from domain.schemas import (
    ExceptionResponseSchema,
    GetAccessLogResponseSchema,
    AccessLogEntryResponseSchema
)
from domain.services import AccessLogService
from domain.models import AccessLog

accesslog_router = APIRouter()


@accesslog_router.get(
    "/entries",
    response_model=GetAccessLogResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_access_log_entries(request: Request) -> GetAccessLogResponseSchema:
    """
    Route to get a list of access log entries.

    Args:
        request (Request): The incoming request.

    Returns:
        GetAccessLogResponseSchema: A list of access log entries as per the response model.
    """

    access_log_entries = await AccessLogService().fetch_access_log(request.app.state.monitortask)
    return AccessLog(entries=access_log_entries)