from typing import List
from domain.models import Memory

from monitor import MonitorTask


class MemoryService:

    def __init__(self):
        ...

    async def get_memory(self, monitor_task: MonitorTask) -> Memory:
        return Memory(usage=monitor_task.memory_used, total=monitor_task.memory_total, percent=monitor_task.memory_percent)

    def __str__(self):
        return self.__class__.__name__
