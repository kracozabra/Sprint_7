import allure
import requests
import data
from faker import Faker


@allure.step('Генерируем случайные данные для заполнения формы заказа')
def generate_random_order_data():
    fake = Faker(locale="ru_Ru")

    future_date = fake.future_date()
    order_create_data = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": fake.pyint(min_value=1, max_value=224),
        "phone": fake.phone_number(),
        "rentTime": fake.pyint(min_value=1, max_value=7),
        "deliveryDate": f'{future_date.year}-{future_date.month}-{future_date.day}',
        "comment": fake.text(max_nb_chars=80),
        "color": fake.random_choices(elements=("BLACK", "GREY"))
    }
    return order_create_data


@allure.step('Генерируем случайные данные для создания курьера')
def generate_random_courier_data():
    fake = Faker(locale="ru_Ru")

    courier_create_data = {
        "login": fake.user_name(),
        "password": fake.password(length=10),
        "firstName": fake.first_name()
    }
    return courier_create_data


@allure.step('Получаем id курьера')
def get_courier_id_by_login(login, password):
    payload = {
        "login": login,
        "password": password
    }
    response = requests.post(data.LOGIN_COURIER_ENDPOINT, data=payload)
    if response.status_code == 200:
        return response.json()['id']
    else:
        return None


@allure.step('Удаляем курьера')
def delete_courier_by_login(login, password):
    courier_id = get_courier_id_by_login(login, password)
    requests.delete(data.DELETE_COURIER_ENDPOINT + str(courier_id))


@allure.step('Создаем нового курьера и получаем его логин и пароль')
def register_new_courier_and_return_login_password():
    payload = generate_random_courier_data()
    courier_login_data = {}

    response = requests.post(data.CREATE_COURIER_ENDPOINT, data=payload)

    if response.status_code == 201:
        courier_login_data = {
            "login": payload['login'],
            "password": payload['password']
        }
    return courier_login_data
