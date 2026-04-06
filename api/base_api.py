import requests
import allure

class BaseAPI:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    @allure.step("GET {endpoint}")
    def get(self, endpoint, params=None, headers=None, expected_status=None):
        url = f"{self.base_url}{endpoint}"
        response = self.client.get(url, params=params, headers=headers)
        if expected_status is not None:
            assert response.status_code == expected_status, \
                f"Ожидался {expected_status}, получен {response.status_code}"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint, json=None, data=None, headers=None, expected_status=None):
        url = f"{self.base_url}{endpoint}"
        response = self.client.post(url, json=json, data=data, headers=headers)
        if expected_status is not None:
            assert response.status_code == expected_status, \
                f"Ожидался {expected_status}, получен {response.status_code}"
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
        return response
    