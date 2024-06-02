import time
import psutil
from typing import List


class MonitorTask:
    """A class for monitoring metrics."""

    interval: int
    cpu_percent: List[float]
    num_cores: int
    ram_percent: float
    ram_total: float
    ram_used: float
    disk_info: dict
    network_info: dict
    process_info: List[dict]
    uptime: float
    logs_path: str

    def __init__(self) -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks.
        The monitoring interval is 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.ram_total = psutil.virtual_memory().total
        self.network_info = {}
        self.uptime = 0.0
        self.logs_path = '/var/log/apache2/other_vhosts_access.log'

    def monitor(self):
        """Continuously monitor CPU, RAM, disk, network, process info, and uptime."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.ram_percent = psutil.virtual_memory().percent
            self.ram_used = psutil.virtual_memory().used
            self.disk_info = {
                'total_space': psutil.disk_usage('/').total,
                'used_space': psutil.disk_usage('/').used,
                'usage_percent': psutil.disk_usage('/').percent,
            }
            self.process_info = [
                {'pid': process.info['pid'], 'name': process.info['name'],
                    'cpu_percent': process.info['cpu_percent'], 'memory_percent': process.info['memory_percent']}
                for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
            ]
            self.uptime = time.time() - psutil.boot_time()
            time.sleep(self.interval)

    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
