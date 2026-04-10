import allure
from .base_api import BaseAPI
from constants import REGISTER, LOGIN, USER_DELETE

class UserAPI(BaseAPI):
    def register(self, payload):
        return self.post(REGISTER, json=payload)

    def login(self, email, password):
        return self.post(LOGIN, json={"email": email, "password": password})

    @allure.step("Удаление пользователя по токену")
    def delete_user(self, token):
        headers = {"Authorization": token}
        return self.delete(USER_DELETE, headers=headers)