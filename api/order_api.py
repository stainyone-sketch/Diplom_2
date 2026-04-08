from .base_api import BaseAPI
from constants import ORDERS

class OrderAPI(BaseAPI):
    def create_order(self, ingredients, headers=None):
        payload = {"ingredients": ingredients}
        return self.post(ORDERS, json=payload, headers=headers)
    