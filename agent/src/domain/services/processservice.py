from typing import List
from domain.models import Process, ProcessList
from domain.models import Process, ProcessList
from monitor import MonitorTask



class ProcessService:
    """
    Controller class to fetch process values from a monitoring task.
    """
    def __init__(self):
        # You can initialize any necessary attributes here
        pass
        # You can initialize any necessary attributes here
        pass

    async def get_processes(self, monitor_task: MonitorTask) -> ProcessList:
        """
        Get process values from the provided monitoring task and return them as a ProcessList object.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch process data from.

        Returns:
            ProcessList: A ProcessList object containing a list of Process objects.
        """
        process_list = []

        # Assuming `monitor_task.process_info` is a list of process information
        for process_info in monitor_task.process_info:
            process = Process(
                id=process_info['pid'],  # Assuming 'pid' is a key in process_info
                name=process_info['name'],  # Assuming 'name' is a key in process_info
                cpu_percent=process_info['cpu_percent'],  # Assuming 'cpu_percent' is a key in process_info
                memory_percent=process_info['memory_percent'],  # Assuming 'memory_percent' is a key in process_info
            )
            process_list.append(process)

        return ProcessList(processes=process_list)

    def __str__(self):
        return self.__class__.__name__
