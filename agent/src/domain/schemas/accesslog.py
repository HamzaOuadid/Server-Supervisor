from pydantic import BaseModel
from typing import List


class AccessLogEntryResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing an entry in an access log.

    Attributes:
        timestamp (str): The timestamp of the log entry.
        client_ip (str): The IP address of the client making the request.
        request_method (str): The HTTP request method (e.g., GET, POST).
        request_url (str): The requested URL.
        status_code (int): The HTTP status code of the response.
        user_agent (str): The user agent string of the client.
    """
    host : str
    port : str
    ip_address : str
    timestamp: str
    request_method: str
    resource_access : str
    http_version : str
    server_response_code : str
    number_of_byte_transferred : str
    browser : str


class GetAccessLogResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing access log information.

    Attributes:
        entries (List[AccessLogEntryResponseSchema]): List of access log entries.
    """
    entries: List[AccessLogEntryResponseSchema]
