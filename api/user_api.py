from .base_api import BaseAPI
from constants import REGISTER, LOGIN

class UserAPI(BaseAPI):
    def register(self, payload, expected_status=200):
        return self.post(REGISTER, json=payload, expected_status=expected_status)

    def login(self, email, password, expected_status=200):
        return self.post(LOGIN, json={"email": email, "password": password}, expected_status=expected_status)
    