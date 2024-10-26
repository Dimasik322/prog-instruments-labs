import re
import json
import hashlib
import logging
from typing import List
import csv

logging.basicConfig(level=logging.INFO)

FILE_PATH = "lab_3\\13.csv"
RESULT_PATH = "lab_3\\result.json"
PATTERN = { }

"""
В этом модуле обитают функции, необходимые для автоматизированной проверки результатов ваших трудов.
"""

def calculate_checksum(row_numbers: List[int]) -> str:
    """
    Вычисляет md5 хеш от списка целочисленных значений.

    ВНИМАНИЕ, ВАЖНО! Чтобы сумма получилась корректной, считать, что первая строка с данными csv-файла имеет номер 0
    Другими словами: В исходном csv 1я строка - заголовки столбцов, 2я и остальные - данные.
    Соответственно, считаем что у 2 строки файла номер 0, у 3й - номер 1 и так далее.

    Надеюсь, я расписал это максимально подробно.
    Хотя что-то мне подсказывает, что обязательно найдется человек, у которого с этим возникнут проблемы.
    Которому я отвечу, что все написано в докстринге ¯\_(ツ)_/¯

    :param row_numbers: список целочисленных номеров строк csv-файла, на которых были найдены ошибки валидации
    :return: md5 хеш для проверки через github action
    """
    row_numbers.sort()
    return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()


def serialize_result(variant: int, checksum: str) -> None:
    """
    Метод для сериализации результатов лабораторной пишите сами.
    Вам нужно заполнить данными - номером варианта и контрольной суммой - файл, лежащий в папке с лабораторной.
    Файл называется, очевидно, result.json.

    ВНИМАНИЕ, ВАЖНО! На json натравлен github action, который проверяет корректность выполнения лабораторной.
    Так что не перемещайте, не переименовывайте и не изменяйте его структуру, если планируете успешно сдать лабу.

    :param variant: номер вашего варианта
    :param checksum: контрольная сумма, вычисленная через calculate_checksum()
    """
    try:
        with open(RESULT_PATH, 'w', encoding='utf-8') as file:
            result = {
                "variant" : variant,
                "checksum" : checksum
            }
            file.write(json.dumps(result))
    except Exception as exc:
        logging.error(f"Serializing of result error: {exc}\n")


def read_csv(file_path: str) -> List:
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        head = next(reader)
        rows = [row for row in reader]
        print(rows[4])
    


if __name__ == "__main__":
    read_csv(FILE_PATH)
