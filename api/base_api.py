import allure

class BaseAPI:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    @allure.step("GET {endpoint}")
    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = self.client.get(url, params=params, headers=headers)
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint, json=None, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = self.client.post(url, json=json, data=data, headers=headers)
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = self.client.delete(url, headers=headers)
        allure.attach(response.text, name="Response", attachment_type=allure.attachment_type.TEXT)
        return response