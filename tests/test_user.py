import allure
import pytest
from constants import HTTP_OK, HTTP_FORBIDDEN, HTTP_UNAUTHORIZED, ERR_USER_EXISTS, ERR_REQUIRED_FIELDS, ERR_LOGIN_FAILED
from helpers import generate_user_payload

@pytest.mark.user
@allure.epic("Пользователь")
class TestUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_api):
        payload = generate_user_payload()
        resp = user_api.register(payload)
        data = resp.json()
        try:
            assert resp.status_code == HTTP_OK
            assert data["success"] is True
        finally:
            if "accessToken" in data:
                user_api.delete_user(data["accessToken"])

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, user_api, existing_user):
        with allure.step("Попытка повторной регистрации с теми же данными"):
            payload = {"email": existing_user["email"], "password": existing_user["password"], "name": existing_user["name"]}
            resp = user_api.register(payload)
        with allure.step("Проверка ошибки"):
            assert resp.status_code == HTTP_FORBIDDEN
            assert resp.json()["message"] == ERR_USER_EXISTS

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    def test_create_user_missing_field(self, user_api, missing_field):
        payload = generate_user_payload()
        del payload[missing_field]
        with allure.step("Отправка запроса на регистрацию"):
            resp = user_api.register(payload)
        with allure.step("Проверка кода ошибки и сообщения"):
            assert resp.status_code == HTTP_FORBIDDEN
            assert resp.json()["message"] == ERR_REQUIRED_FIELDS

    @allure.title("Логин существующего пользователя")
    def test_login_existing_user(self, user_api, created_user):
        with allure.step(f"Попытка входа с email {created_user['email']}"):
            resp = user_api.login(created_user["email"], created_user["password"])
        with allure.step("Проверка успешного ответа"):
            assert resp.status_code == HTTP_OK
            assert "accessToken" in resp.json()

    @allure.title("Логин с неверным логином")
    def test_login_wrong_email(self, user_api, created_user):
        with allure.step("Попытка входа с неверным email"):
            resp = user_api.login("wrong@example.com", created_user["password"])
        with allure.step("Проверка ошибки авторизации"):
            assert resp.status_code == HTTP_UNAUTHORIZED
            assert resp.json()["message"] == ERR_LOGIN_FAILED

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, user_api, created_user):
        with allure.step("Попытка входа с неверным паролем"):
            resp = user_api.login(created_user["email"], "wrongpass")
        with allure.step("Проверка ошибки авторизации"):
            assert resp.status_code == HTTP_UNAUTHORIZED
            assert resp.json()["message"] == ERR_LOGIN_FAILED