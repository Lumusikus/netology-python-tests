import os
import re
import unittest
from datetime import datetime

import requests

PHONE_REGEX = re.compile(r'^\+?(7|8).?(\d{3}).?-?(\d{3})-?(\d{2})-?(\d{2})\D*(\d*)')


# исправление номера телефона из задания о регулярных выражениях
def parse_phone(phone_raw):
    if phone_match := re.match(PHONE_REGEX, phone_raw):
        phone = f"+7({phone_match.group(2)}){phone_match.group(3)}-{phone_match.group(4)}-{phone_match.group(5)}"
        if len(phone_match.groups()) > 5 and len(phone_match.group(6)) > 0:
            phone += f" доб. {phone_match.group(6)}"
    else:
        phone = phone_raw

    return phone


# итератор из задания про итераторы
def flat_generator(list_of_lists):
    for lst in list_of_lists:
        for item in lst:
            yield item

# декоратор из задания про декораторы
def logger(old_function):
    def new_function(*args, **kwargs):
        with open('main.log', 'a', encoding='utf-8') as log_file:
            now = datetime.now()
            result = old_function(*args, **kwargs)
            log_file.write(f'{now} - Функция {old_function.__name__}; Аргументы: args={args}, kwargs={kwargs}; Результат: {result}\n')
            return result
    return new_function


class TestTasks(unittest.TestCase):

    def setUp(self):
        print('Начинаем тестирование функций из предыдущих заданий')

    def tearDown(self) -> None:
        print('Тестирование функций из предыдущих заданий закончено')

    def test_parse_phone(self):
        simple_phone = '89991112233'
        correct_phone = '+7(999)111-22-33'
        with_additional = '+74956667788,,,33'
        incorrect_phone = '123'

        self.assertEqual(parse_phone(simple_phone), correct_phone)
        self.assertEqual(parse_phone(correct_phone), correct_phone)
        self.assertEqual(parse_phone(with_additional), '+7(495)666-77-88 доб. 33')
        self.assertEqual(parse_phone(incorrect_phone), incorrect_phone)

    def test_iterator(self):

        source_list = [
            [1,2,3],
            [4,5],
            ['Hello'],
        ]

        self.assertListEqual(
            list(flat_generator(source_list)),
            [1, 2, 3, 4, 5, 'Hello'],
        )

    def test_decorator(self):

        @logger
        def sum(a, b=0):
            return a + b

        if os.path.exists('main.log'):
            os.remove('main.log')

        sum(3, b=4.7)
        self.assertTrue(os.path.exists('main.log'))

        with open('main.log', encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        self.assertTrue('sum' in log_file_content)
        self.assertTrue('3' in log_file_content)
        self.assertTrue("{'b': 4.7}" in log_file_content)
        self.assertTrue('7.7' in log_file_content)



class TestYandexDisk(unittest.TestCase):

    def setUp(self):
        print('Начинаем тестирование API Яндекс.Диска')
        # в целях безопасности получаем токен для API из переменной окружения
        self.token = os.environ['YA_DISK_TOKEN']

    def tearDown(self):
        print('Тестирование API Яндекс.Диска завершено')


    def test_yandex_disk(self):

        dir_name = 'super_test_dir'

        # папка не существует на момент начала тестов
        response_check = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={dir_name}',
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        self.assertEqual(response_check.status_code, 404)

        # проверяем создание
        response_create = requests.put(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={dir_name}',
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        self.assertEqual(response_create.status_code, 201)

        # проверяем, что папка создана
        response_check = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={dir_name}',
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        self.assertEqual(response_check.status_code, 200)

        # проверяем удаление
        response_delete = requests.delete(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={dir_name}&permanently=true',
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        self.assertEqual(response_delete.status_code, 204)


if __name__ == '__main__':
    unittest.main()
