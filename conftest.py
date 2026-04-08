import allure
import pytest
import requests
from api.user_api import UserAPI
from api.order_api import OrderAPI
from constants import BASE_URL, INGREDIENTS, HTTP_OK
from helpers import generate_user_payload

@pytest.fixture(scope="session")
def api_client():
    with requests.Session() as session:
        yield session

@pytest.fixture
def user_api(api_client):
    return UserAPI(api_client, BASE_URL)

@pytest.fixture
def order_api(api_client):
    return OrderAPI(api_client, BASE_URL)

@pytest.fixture
def ingredient_ids(api_client):
    with allure.step("Получение списка ингредиентов с сервера"):
        resp = api_client.get(f"{BASE_URL}{INGREDIENTS}")
        data = resp.json()
        ids = [ing["_id"] for ing in data.get("data", [])]
    with allure.step(f"Выбраны первые два ингредиента: {ids[:2]}"):
        return ids[:2]

@pytest.fixture
def auth_headers(created_user):
    with allure.step("Формирование заголовка авторизации с токеном"):
        return {"Authorization": created_user["accessToken"]}

@pytest.fixture
def existing_user(user_api):
    payload = generate_user_payload()
    resp = user_api.register(payload)
    assert resp.status_code == HTTP_OK, "Не удалось создать пользователя в фикстуре"
    data = resp.json()
    user_info = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": data.get("accessToken"),
        "refreshToken": data.get("refreshToken")
    }
    yield user_info
    if user_info.get("accessToken"):
        user_api.delete_user(user_info["accessToken"])

@pytest.fixture
def created_user(user_api):
    payload = None
    with allure.step("Генерация данных нового пользователя"):
        payload = generate_user_payload()
        allure.attach(str(payload), "Данные пользователя", allure.attachment_type.JSON)
    with allure.step(f"Регистрация пользователя {payload['email']}"):
        resp = user_api.register(payload)
        data = resp.json()
    user_info = {
        "email": payload["email"],
        "password": payload["password"],
        "name": payload["name"],
        "accessToken": data.get("accessToken"),
        "refreshToken": data.get("refreshToken")
    }
    yield user_info
    with allure.step(f"Удаление пользователя {user_info['email']} после теста"):
        if user_info.get("accessToken"):
            user_api.delete_user(user_info["accessToken"])