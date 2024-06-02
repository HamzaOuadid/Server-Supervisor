from typing import List
from domain.models import AccessLogEntry, AccessLog
import logging
logging.basicConfig(level=logging.DEBUG)
import re
from monitor import MonitorTask

class AccessLogService:
    """
    Controller class to fetch access log data from a remote server through SSH.
    """

    def __init__(self):

        ...

    async def fetch_access_log(self, monitor_task: MonitorTask) -> AccessLog:
        """
        Fetch access log data from the remote server and return them as a list of AccessLog objects.

        Returns:
            List[AccessLog]: A list of AccessLog objects containing access log data.
        """
        access_log_list = []
        regex = r'(.*?):(\d+) ((\d+\.)+(\d+)) - - \[(.*?)\] "(.*?) (.*?) (HTTP\/\d.\d)" (\d+) (\d+)\s("(.*?)"\s?)+'
        
        try:
            # Open the local log file and read its contents
            with open(monitor_task.logs_path, 'r') as log_file:
                for line in log_file:
                    match = re.search(regex,line)
                    access_log_list.append(AccessLogEntry(host=match.groups()[0],port=match.groups()[1],ip_address=match.groups()[2],
                        timestamp=match.groups()[5],request_method=match.groups()[6],resource_access=match.groups()[7],http_version=match.groups()[8],
                        server_response_code=match.groups()[9],number_of_byte_transferred=match.groups()[10],browser=match.groups()[11][1:-2]))

        except Exception as e:
            logging.error(f"Error reading access log: {e}")

        return access_log_list

    def __str__(self):
        return self.__class__.__name__

