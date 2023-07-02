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
        self.filename = f'{keyword.lower()}.json'
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

    def sort_by_salary_from(self):
        """ Функция сортировки вакансий по минимальной зарплате """
        desc = True if input(
            "> - по убыванию\n"
            "< - по возрастанию\n"
            ">>> "
        ) == ">" else False
        vacancies = self.json_read()
        return sorted(vacancies,
                      key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0),
                      reverse=desc)

    def filter_by_salary_from(self):
        """ Функция фильтрации вакансий по минимальной зарплате """
        minimal_salary = int(input(
            "Введите минимальную зарплату\n"
            ">>> "))
        vacancies = self.json_read()
        return sorted(vacancies, key=lambda x: (int(x.salary_from) >= minimal_salary if x.salary_from else 0))


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

    def __lt__(self, other):
        return int(self.salary_from) < int(other)

    def __le__(self, other):
        return int(self.salary_from) <= int(other)

    def __gt__(self, other):
        return int(self.salary_from) > int(other)

    def __ge__(self, other):
        return int(self.salary_from) >= int(other)