from pydantic import BaseModel
from .cpu import GetCpuResponseSchema, GetCpuCoreResponseSchema
from .ram import GetRamResponseSchema
from .disk import GetDiskResponseSchema
from .process import GetProcessResponseSchema , GetProcessListResponseSchema
from .uptime import GetUptimeResponseSchema
from .accesslog import AccessLogEntryResponseSchema,GetAccessLogResponseSchema


class ExceptionResponseSchema(BaseModel):
    error: str

__all__ = [
    "GetCpuResponseSchema",
    "GetCpuCoreResponseSchema",
    "GetRamResponseSchema",
    "GetDiskResponseSchema",
    "GetProcessResponseSchema",
    "GetProcessListResponseSchema",
    "GetProcessListResponseSchema",
    "GetUptimeResponseSchema",
    "GetAccessLogResponseSchema",
    "AccessLogEntryResponseSchema",
    "ExceptionResponseSchema"

]
