import json
from abc import ABC, abstractmethod


class API(ABC):
    """Абстрактный класс"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self, page_count):
        pass


class ParsingError(Exception):
    """ Класс возбуждающий пользовательскую ошибку """
    pass


class JsonFile:
    """ Класс работает с json-файлом"""

    def __init__(self, keyword, vacancies_json):
        self.keyword = keyword
        self.filename = f'jsondata/{keyword.lower()}.json'
        self.json_write(vacancies_json)

    def json_write(self, vacancies_json):
        """ Метод записи вакансий в файл """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4)

    def json_read(self):
        """ Метод чтения вакансий из файла """
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]


class Vacancy:
    """ Класс вакансии"""

    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.url = vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = "RUR" if vacancy["currency"] == "rub" else vacancy["currency"]

    def __str__(self):
        salary = ""
        if self.salary_from == None and self.salary_to == None:
            salary = "Не указана"
        else:
            if self.salary_from != None:
                salary += f"от {self.salary_from} {self.currency} "
            if self.salary_to != None:
                salary += f"до {self.salary_to} {self.currency}"
        return f"""Работодатель: {self.employer}
Вакансия: {self.title}
Зарплата: {salary}
Ссылка: {self.url}
"""

    @staticmethod
    def to_int(value):
        try:
            return int(value)
        except TypeError:
            return 0

    def __lt__(self, other):
        return self.to_int(self.salary_from) < self.to_int(other.salary_from)

    def __le__(self, other):
        return self.to_int(self.salary_from) <= self.to_int(other.salary_from)

    def __gt__(self, other):
        return self.to_int(self.salary_from) > self.to_int(other.salary_from)

    def __ge__(self, other):
        return self.to_int(self.salary_from) >= self.to_int(other.salary_from)

