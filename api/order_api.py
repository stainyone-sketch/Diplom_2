from .base_api import BaseAPI
from constants import ORDERS

class OrderAPI(BaseAPI):
    def create_order(self, ingredients, headers=None, expected_status=200):
        payload = {"ingredients": ingredients}
        return self.post(ORDERS, json=payload, headers=headers, expected_status=expected_status)
    