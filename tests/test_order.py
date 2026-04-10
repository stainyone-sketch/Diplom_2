import allure
import pytest
from constants import HTTP_OK, HTTP_BAD_REQUEST, HTTP_INTERNAL_ERROR, HTTP_UNAUTHORIZED, ERR_NO_INGREDIENTS

@pytest.mark.order
@allure.epic("Заказы")
class TestOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_auth(self, order_api, auth_headers, ingredient_ids):
        with allure.step(f"Отправка запроса на создание заказа с ингредиентами {ingredient_ids}"):
            resp = order_api.create_order(ingredient_ids, headers=auth_headers)
        with allure.step("Проверка успешного ответа"):
            assert resp.status_code == HTTP_OK
            assert resp.json()["success"] is True
            assert "order" in resp.json()

    @allure.title("Создание заказа без авторизации (документация ожидает 401)")
    @pytest.mark.xfail(reason="Баг API: создание заказа без авторизации возвращает 200 вместо 401")
    def test_create_order_no_auth(self, order_api, ingredient_ids):
        with allure.step("Отправка запроса на создание заказа без токена авторизации"):
            resp = order_api.create_order(ingredient_ids)
        with allure.step("Проверка, что API вернул 401 (фактически баг, вернётся 200)"):
            assert resp.status_code == HTTP_UNAUTHORIZED

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, order_api, auth_headers):
        with allure.step("Отправка запроса с пустым списком ингредиентов"):
            resp = order_api.create_order([], headers=auth_headers)
        with allure.step("Проверка ошибки 400 и сообщения"):
            assert resp.status_code == HTTP_BAD_REQUEST
            assert resp.json()["message"] == ERR_NO_INGREDIENTS

    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient_hash(self, order_api, auth_headers):
        with allure.step("Отправка запроса с несуществующим хешем ингредиента"):
            resp = order_api.create_order(["invalid_hash_123"], headers=auth_headers)
        with allure.step("Проверка ошибки 500 и наличия страницы ошибки"):
            assert resp.status_code == HTTP_INTERNAL_ERROR
            assert "Internal Server Error" in resp.text