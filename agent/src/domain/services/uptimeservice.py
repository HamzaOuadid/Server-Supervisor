from domain.models import Uptime
from monitor import MonitorTask


class UptimeService:
    """
    Controller class to fetch uptime values from a monitoring task.
    """

    def __init__(self):
        pass

    async def get_uptime(self, monitor_task: MonitorTask) -> Uptime:
        """
        Get uptime value from the provided monitoring task and return it as an Uptime object.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch uptime data from.

        Returns:
            Uptime: An Uptime object containing uptime value.
        """
        # Extract uptime information from monitor_task and populate uptime object
        uptime_seconds = monitor_task.uptime
        uptime = Uptime(seconds=uptime_seconds)

        return uptime

    def __str__(self):
        return self.__class__.__name__
