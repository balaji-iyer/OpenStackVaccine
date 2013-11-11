from clients.os_client import OS_Client
import os
class TestOSClient:
    def __init__(self):
        self.client = client.Client(os.getenv('OS_USERNAME'),
                                    os.getenv('OS_TENENT_NAME'),
                                    os.getenv('OS_PASSWORD'),
                                    os.getenv('OS_AUTH_URL'))

