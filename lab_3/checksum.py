import re
import json
import hashlib
import logging
import csv
from typing import List

logging.basicConfig(level=logging.INFO)

VARIANT = "13"
FILE_PATH = f"lab_3\\{VARIANT}.csv"
RESULT_PATH = "lab_3\\result.json"
PATTERN = {
    "email": r"^\w+(\.\w+)*@\w+(\.\w+)+$",
    "http_status_message": r"^\d{3}(\s\w+)+$",
    "inn": r"^\d{12}$",
    "passport": r"^\d{2}\s\d{2}\s\d{6}$",
    "ip_v4": r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[0-9]?[0-9])$",
    "latitude": r"^[+-]?(90\.0+|[0-8]?[0-9]\.[0-9]+)$",
    "hex_color": r"^#[a-f0-9]{6}$",
    "isbn": r"^(\d{3}-)?\d{1}-\d{5}-\d{3}-\d{1}$",
    "uuid": r"^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$",
    "time": r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d.\d+$"
}

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
    try:
        row_numbers.sort()
        return hashlib.md5(json.dumps(row_numbers).encode('utf-8')).hexdigest()
    except Exception as exc:
        logging.error(f"Checksum calculating error: {exc}\n")


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


def read_csv(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-16') as file:
            reader = csv.reader(file, delimiter=';')
            head = next(reader)
            rows = [row for row in reader]
        return rows
    except Exception as exc:
        logging.error(f"Reading .csv error: {exc}\n")
    

def check_validity(row: list, pattern: dict) -> bool:
    try:
        flag = True
        for pair in list(zip(list(pattern.values()), row)):
            if not bool(re.match(pair[0], pair[1])):
                flag = False
        return flag
    except Exception as exc:
        logging.error(f"Checking row validity error: {exc}\n")    


def get_invalid_indeces(rows: list, pattern: dict) -> list:
    try:
        invalid_rows_indeces = []
        for index in range(len(rows)):
            if not check_validity(rows[index], pattern):
                invalid_rows_indeces.append(index)
        return invalid_rows_indeces
    except Exception as exc:
        logging.error(f"Getting indeces of invalid rows error: {exc}\n")


if __name__ == "__main__":
    rows = read_csv(FILE_PATH)
    invalid_indeces = get_invalid_indeces(rows, PATTERN)
    checksum = calculate_checksum(invalid_indeces)
    serialize_result(VARIANT, checksum)
