"""
This module defines a controller class for fetching RAM values from a monitoring task.
"""
from typing import List
from domain.models import Ram
from monitor import MonitorTask


# Controller class to fetch RAM values from monitoring task
class RamService:
    """
    Controller class to fetch RAM values from a monitoring task.
    """

    def __init__(self):
        ...

    async def get_ram(self, monitor_task: MonitorTask) -> List[Ram]:
        """
        Get RAM values from the provided monitoring task and return them as a list of Ram objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch RAM data from.

        Returns:
            List[Ram]: A list of Ram objects containing RAM values.
        """
        ram_list = [Ram(usage=monitor_task.ram_used,
                        capacity=monitor_task.ram_total, percent=monitor_task.ram_percent)]
        return ram_list

    def __str__(self):
        return self.__class__.__name__
