# Помогает корректно выводить символы кириллицы в консоли PyCharm
def pytest_make_parametrize_id(config, val):
    return repr(val)
