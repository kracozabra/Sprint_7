#URL-ы и ENDPOINT-ы
URL = 'https://qa-scooter.praktikum-services.ru'
CREATE_COURIER_ENDPOINT = URL + '/api/v1/courier'
LOGIN_COURIER_ENDPOINT = URL + '/api/v1/courier/login'
DELETE_COURIER_ENDPOINT = URL + '/api/v1/courier/'
CREATE_ORDER_ENDPOINT = URL + '/api/v1/orders'
GET_ORDER_LIST_ENDPOINT = URL + '/api/v1/orders'

#Дополнитлельная информация для запросов
headers_json = {"Content-type": "application/json"}

#Тексты ответов API
response_create_courier_success = '{"ok":true}'
response_create_courier_used_login = "Этот логин уже используется. Попробуйте другой."
response_create_courier_not_enough_data = "Недостаточно данных для создания учетной записи"
response_login_courier_not_enough_data = "Недостаточно данных для входа"
response_login_courier_record_not_found = "Учетная запись не найдена"
