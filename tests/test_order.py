import json
import requests
import helpers
import pytest
import allure
import data


class TestCreateOrder:
    ENDPOINT = f'{data.URL}/api/v1/orders'

    @allure.title('Проверка создания заказа с указаним разных вариантов цвета самоката')
    @pytest.mark.parametrize('color', [[], ['BLACK'], ['GREY'], ['BLACK', 'GREY']])
    def test_create_order_with_different_colors(self, color):
        payload = helpers.generate_random_order_data()
        payload['color'] = color
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 201
        assert response.json()['track'] is not None


class TestGetOrderList:
    ENDPOINT = f'{data.URL}/api/v1/orders'

    @allure.title('Проверка получения списка заказов')
    def test_get_order_list(self):
        response = requests.get(self.ENDPOINT)

        assert response.status_code == 200
        assert response.json()['orders'] != []
