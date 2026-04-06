import pytest
import requests
from api.user_api import UserAPI
from api.order_api import OrderAPI
from constants import BASE_URL, INGREDIENTS
from helpers import generate_user_payload

@pytest.fixture
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
def unique_user_data():
    return generate_user_payload()

@pytest.fixture
def created_user(user_api, unique_user_data):
    resp = user_api.register(unique_user_data)
    if resp.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя: {resp.text}")
    data = resp.json()
    yield {
        "email": unique_user_data["email"],
        "password": unique_user_data["password"],
        "name": unique_user_data["name"],
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"]
    }

@pytest.fixture
def auth_headers(created_user):
    return {"Authorization": created_user["accessToken"]}

@pytest.fixture
def ingredient_ids(api_client):
    resp = api_client.get(f"{BASE_URL}{INGREDIENTS}")
    assert resp.status_code == 200
    data = resp.json()
    ids = [ing["_id"] for ing in data.get("data", [])]
    return ids[:2]