"""This module defines an exemple of test"""
import threading
from fastapi.testclient import TestClient
from server import app
from monitor import MonitorTask
import time
from domain.models import Process, ProcessList
import os


class MonitorTaskFake(MonitorTask):
    """
    Monitor class to mock the real monitor
    Instead of using the real monitor that fetch data on the host
    we use a monitor that provide "fake" values to control the output
    and make deterministic test (deterministic = repeatable and known values)
    """
    interval: int = 0
    cpu_percent: list[float] = ["10", "12"]
    num_cores: int = 3
    ram_used: float = 9893027840
    ram_total: float = 17031098368
    ram_percent: float = 58.1
    uptime : float
    disk_info : dict = {"total_space":474736148480,"used_space":378323877888,"usage_percent":79.7}
    process_info: list[dict] = [{"pid": 4,"name": "System","cpu_percent": 0,"memory_percent": 0.054233025964752615},
      {
      "pid": 4980,
      "name": "bash.exe",
      "cpu_percent": 0,
      "memory_percent": 0.07005800649016602
    },
    {
      "pid": 2360,
      "name": "firefox.exe",
      "cpu_percent": 0,
      "memory_percent": 0.4933882606061641
    },
    {
      "pid": 2408,
      "name": "wsl.exe",
      "cpu_percent": 0,
      "memory_percent": 0.06144806267846693
    }]
    logs_path: str = 'src/tests/log.out'
    def __init__(self) -> None:
        self.ram_total = 17031098368.0
        
    def monitor(self):
        pass


# Launching the real monitor for test involving the real monitor
client  = TestClient(app)
thread = threading.Thread(target=app.state.monitortask.monitor, daemon=True)
thread.start()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_cpu_usage():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [{"id": 0, "usage": "10"}, {"id": 1, "usage": "12"}]
    # restore monitortask for next test
    app.state.monitortask = save_app


def test_get_cpu_core():
    response = client.get("/metrics/v1/cpu/core")
    # we can test types but not values because they will change at each test.
    assert response.status_code == 200
    assert isinstance(response.json()["number"], int)

def test_get_ram():
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/ram/usage")
    assert response.status_code == 200
    assert response.json() == [{"usage":9893027840,"capacity":17031098368,"percent":58.1}]
    app.state.monitortask = save_app


def test_get_disk():
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/disk/info")
    assert response.status_code == 200
    assert response.json() == [{"total_space":474736148480,"used_space":378323877888,"usage_percent":79.7}]
    app.state.monitortask = save_app


def test_get_processes():
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get('/metrics/v1/process/processes')
    assert response.status_code == 200
    assert response.json() == {'processes': [{"id": 4,"name": "System","cpu_percent": 0,"memory_percent": 0.054233025964752615},
    {"id": 4980,"name": "bash.exe","cpu_percent": 0,"memory_percent": 0.07005800649016602},
    {"id": 2360,"name": "firefox.exe","cpu_percent": 0,"memory_percent": 0.4933882606061641},
    {"id": 2408,"name": "wsl.exe","cpu_percent": 0,"memory_percent": 0.06144806267846693}]}
    app.state.monitortask = save_app


def test_get_process_by_pid():
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()
    response = client.get('/metrics/v1/process/process/2408')
    assert response.status_code == 200
    assert response.json() == {
      "id": 2408,
      "name": "wsl.exe",
      "cpu_percent": 0,
      "memory_percent": 0.06144806267846693
    }
    app.state.monitortask = save_app

def test_get_uptime():
    response = client.get("/metrics/v1/uptime/info")
    assert response.status_code == 200
    assert isinstance(response.json()["seconds"],float)

def test_fetch_access_log():
    save_app = app.state.monitortask
    app.state.monitortask = MonitorTaskFake()

    # mocks the logs
    log1 = r'localhost:80 192.168.240.50 - - [11/Dec/2023:20:08:27 +0000] "GET /?author=1 HTTP/1.0" 200 13052 "-" "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/95.0"'
    log2 = r'localhost:80 127.0.0.1 - - [11/Dec/2023:00:05:01 +0000] "GET /wp-cron.php HTTP/1.1" 200 303 "-" "Mozilla/5.0"'
    log3 = r'localhost:80 192.168.240.50 - - [13/Jan/2024:17:22:19 +0000] "GET /?page_id=2 HTTP/1.0" 200 12534 "http://gauvain.telecomste.net/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"'
    # mock the logs file
    path = 'src/tests/log.out'
    with open (path, mode = 'w') as file:
        # write mock logs
        file.write(log1)
        file.write("\n")
        file.write(log2)
        file.write("\n")
        file.write(log3)

    accessLog = {"entries":[
        {
      "host": "localhost",
      "port": "80",
      "ip_address": "192.168.240.50",
      "timestamp": "11/Dec/2023:20:08:27 +0000",
      "request_method": "GET",
      "resource_access": "/?author=1",
      "http_version": "HTTP/1.0",
      "server_response_code": "200",
      "number_of_byte_transferred": "13052",
      "browser": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/95.0"
    },
    {
      "host": "localhost",
      "port": "80",
      "ip_address": "127.0.0.1",
      "timestamp": "11/Dec/2023:00:05:01 +0000",
      "request_method": "GET",
      "resource_access": "/wp-cron.php",
      "http_version": "HTTP/1.1",
      "server_response_code": "200",
      "number_of_byte_transferred": "303",
      "browser": "Mozilla/5.0"
    },
     {
      "host": "localhost",
      "port": "80",
      "ip_address": "192.168.240.50",
      "timestamp": "13/Jan/2024:17:22:19 +0000",
      "request_method": "GET",
      "resource_access": "/?page_id=2",
      "http_version": "HTTP/1.0",
      "server_response_code": "200",
      "number_of_byte_transferred": "12534",
      "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3"
    }]
    }

    response = client.get('/metrics/v1/logs/entries/')

    assert response.status_code == 200
    assert response.json() == accessLog

    # delete log file
    os.remove(path)
    app.state.monitortask = save_app