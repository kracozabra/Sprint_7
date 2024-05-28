import json
import requests
import helpers
import pytest
import allure
import data


class TestCreateCourier:
    ENDPOINT = f'{data.URL}/api/v1/courier'

    @allure.title('Проверка создания курьера с корректными данными')
    def test_create_courier_with_correct_data(self):
        payload = helpers.generate_random_courier_data()
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 201
        assert response.text == '{"ok":true}'

        helpers.delete_courier_by_login(payload['login'], payload['password'])

    @allure.title('Проверка создания курьера с данными, которые уже есть у другого курьера')
    def test_create_courier_with_existing_data(self):
        payload = helpers.generate_random_courier_data()
        payload_json = json.dumps(payload)

        requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)
        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 409
        assert response.json()['message'] == "Этот логин уже используется. Попробуйте другой."

        helpers.delete_courier_by_login(payload['login'], payload['password'])

    @allure.title('Проверка создания курьера без указания обязательного поля в запросе')
    @pytest.mark.parametrize('field', ['login', 'password', 'firstName'])
    def test_create_courier_without_required_field(self, field):
        payload = helpers.generate_random_courier_data()
        del payload[field]
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи"

    @allure.title('Проверка создания курьера с пустым обязательным полем')
    @pytest.mark.parametrize('field', ['login', 'password', 'firstName'])
    def test_create_courier_with_empty_required_field(self, field):
        payload = helpers.generate_random_courier_data()
        payload[field] = ''
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для создания учетной записи"


class TestLoginCourier:
    ENDPOINT = f'{data.URL}/api/v1/courier/login'

    @allure.title('Проверка авториации курьера с корректными данными')
    def test_login_courier_with_correct_data(self):
        payload = helpers.register_new_courier_and_return_login_password()
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 200
        assert response.json()['id'] is not None

        helpers.delete_courier_by_login(payload['login'], payload['password'])

    @allure.title('Проверка авторизации курьера без указания обязательного поля в запросе')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_courier_without_required_field(self, field):
        payload = helpers.register_new_courier_and_return_login_password()
        backup_payload = payload.copy()
        del payload[field]
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для входа"

        helpers.delete_courier_by_login(backup_payload['login'], backup_payload['password'])

    @allure.title('Проверка авторизации курьера с пустым обязательным полем')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_login_courier_with_empty_required_field(self, field):
        payload = helpers.register_new_courier_and_return_login_password()
        backup_payload = payload.copy()
        payload[field] = ''
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)

        assert response.status_code == 400
        assert response.json()['message'] == "Недостаточно данных для входа"

        helpers.delete_courier_by_login(backup_payload['login'], backup_payload['password'])

    @allure.title('Проверка авторизации курьера с несуществующим логином')
    def test_login_courier_with_not_existing_login(self):
        payload = helpers.generate_random_courier_data()
        backup_payload = payload.copy()
        payload['login'] += '_not_exist'
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)
        assert response.status_code == 404
        assert response.json()['message'] == "Учетная запись не найдена"

        helpers.delete_courier_by_login(backup_payload['login'], backup_payload['password'])

    @allure.title('Проверка авторизации курьера с неверным паролем')
    def test_login_courier_with_not_correct_password(self):
        payload = helpers.generate_random_courier_data()
        backup_payload = payload.copy()
        payload['password'] += '_not_correct'
        payload_json = json.dumps(payload)

        response = requests.post(self.ENDPOINT, data=payload_json, headers=data.headers_json)
        assert response.status_code == 404
        assert response.json()['message'] == "Учетная запись не найдена"

        helpers.delete_courier_by_login(backup_payload['login'], backup_payload['password'])
