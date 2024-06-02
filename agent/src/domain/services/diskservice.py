from typing import List
from domain.models import Disk
from monitor import MonitorTask


class DiskService:
    """
    Controller class to fetch disk values from a monitoring task.
    """

    def __init__(self):
        # You can initialize any necessary attributes here
        pass

    async def get_disk(self, monitor_task: MonitorTask) -> List[Disk]:
        """
        Get disk values from the provided monitoring task and return them as a list of Disk objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch disk data from.

        Returns:
            List[Disk]: A list of Disk objects containing disk values.
        """
        disk_list = []

        # Assuming `monitor_task.disk_info` is a dictionary containing disk information
        disk_info = monitor_task.disk_info

        # Extract disk information
        total_space = disk_info.get('total_space', 0)
        used_space = disk_info.get('used_space', 0)
        usage_percent = disk_info.get('usage_percent', 0)

        disk = Disk(
            total_space=total_space,
            used_space=used_space,
            usage_percent=usage_percent,
        )
        disk_list.append(disk)

        return disk_list

    def __str__(self):
        return self.__class__.__name__
