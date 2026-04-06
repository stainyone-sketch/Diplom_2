import allure
import pytest
from constants import HTTP_OK, HTTP_FORBIDDEN, HTTP_UNAUTHORIZED, ERR_USER_EXISTS, ERR_REQUIRED_FIELDS
from helpers import generate_user_payload

@pytest.mark.user
@allure.epic("Пользователь")
class TestUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_api):
        payload = generate_user_payload()
        with allure.step("Отправить запрос на регистрацию"):
            resp = user_api.register(payload, expected_status=HTTP_OK)
        with allure.step("Проверить успешный ответ"):
            assert resp.status_code == HTTP_OK
            assert resp.json()["success"] is True

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, user_api, unique_user_data):
        with allure.step("Зарегистрировать пользователя первый раз"):
            user_api.register(unique_user_data, expected_status=HTTP_OK)
        with allure.step("Повторно зарегистрировать того же пользователя"):
            resp = user_api.register(unique_user_data, expected_status=HTTP_FORBIDDEN)
        with allure.step("Проверить ошибку"):
            assert resp.status_code == HTTP_FORBIDDEN
            assert resp.json()["message"] == ERR_USER_EXISTS

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    def test_create_user_missing_field(self, user_api, missing_field):
        payload = generate_user_payload()
        del payload[missing_field]
        with allure.step(f"Отправить запрос без поля {missing_field}"):
            resp = user_api.register(payload, expected_status=HTTP_FORBIDDEN)
        with allure.step("Проверить ошибку"):
            assert resp.status_code == HTTP_FORBIDDEN
            assert resp.json()["message"] == ERR_REQUIRED_FIELDS

    @allure.title("Логин существующего пользователя")
    def test_login_existing_user(self, user_api, created_user):
        with allure.step("Отправить запрос на логин"):
            resp = user_api.login(created_user["email"], created_user["password"], expected_status=HTTP_OK)
        with allure.step("Проверить успешный ответ"):
            assert resp.status_code == HTTP_OK
            assert "accessToken" in resp.json()

    @allure.title("Логин с неверным логином")
    def test_login_wrong_email(self, user_api, created_user):
        with allure.step("Отправить запрос с неверным email"):
            resp = user_api.login("wrong@example.com", created_user["password"], expected_status=HTTP_UNAUTHORIZED)
        with allure.step("Проверить ошибку"):
            assert resp.status_code == HTTP_UNAUTHORIZED
            assert resp.json()["message"] == "email or password are incorrect"

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password(self, user_api, created_user):
        with allure.step("Отправить запрос с неверным паролем"):
            resp = user_api.login(created_user["email"], "wrongpass", expected_status=HTTP_UNAUTHORIZED)
        with allure.step("Проверить ошибку"):
            assert resp.status_code == HTTP_UNAUTHORIZED
            assert resp.json()["message"] == "email or password are incorrect"
            