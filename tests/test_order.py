import allure
import pytest
from constants import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INTERNAL_ERROR, HTTP_UNAUTHORIZED, ERR_NO_INGREDIENTS

@pytest.mark.order
@allure.epic("Заказы")
class TestOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_auth(self, order_api, auth_headers, ingredient_ids):
        with allure.step("Отправить запрос на создание заказа с авторизацией"):
            resp = order_api.create_order(ingredient_ids, headers=auth_headers, expected_status=HTTP_OK)
        with allure.step("Проверить успешный ответ"):
            assert resp.json()["success"] is True
            assert "order" in resp.json()

    @allure.title("Создание заказа без авторизации (документация ожидает 401)")
    def test_create_order_no_auth(self, order_api, ingredient_ids):
        with allure.step("Отправить запрос без токена"):
            resp = order_api.create_order(ingredient_ids, expected_status=HTTP_UNAUTHORIZED)
        with allure.step("Проверить, что API вернул 401 (баг: возвращает 200)"):
            assert resp.status_code == HTTP_UNAUTHORIZED

    @pytest.mark.parametrize("ingredients, expected_status, expected_message", [
        ([], HTTP_BAD_REQUEST, ERR_NO_INGREDIENTS),
        ("valid", HTTP_OK, None),
        (["invalid_hash_123"], HTTP_INTERNAL_ERROR, None)
    ])
    def test_create_order_various_ingredients(self, order_api, auth_headers, ingredient_ids, ingredients, expected_status, expected_message):
        if ingredients == "valid":
            ingredients = ingredient_ids[:1]
        with allure.step(f"Отправить запрос с ингредиентами {ingredients}"):
            resp = order_api.create_order(ingredients, headers=auth_headers, expected_status=expected_status)
        if expected_status == HTTP_INTERNAL_ERROR:
            with allure.step("Проверить, что сервер вернул 500 и HTML-страницу с ошибкой"):
                assert "Internal Server Error" in resp.text
        elif expected_message:
            with allure.step("Проверить сообщение об ошибке"):
                assert resp.json()["message"] == expected_message
        else:
            with allure.step("Проверить успешное создание"):
                assert resp.json()["success"] is True
