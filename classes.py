import json
import requests
from abc import ABC, abstractmethod


class API(ABC):

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self, page_count):
        pass


class HeadHunterAPI(API):
    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "MyAppVac/1.01"
    }

    def __init__(self, keyword: str):
        self.params = {
            "per_page": 100,
            "text": keyword,
            "page": None,
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError('Ошибка полученя данных')
        return response.json()["items"]

    def get_vacancies(self, page_count=1):
        self.vacancies = []
        for page in range(page_count):
            page_vacancies = []
            self.params["page"] = page
            print(f'{self.__class__.__name__[0:-3]}: Cтраница {page + 1}. ', end="")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(f'ошибка {error}')
            else:
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий - {len(page_vacancies)}')
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["employer"]["name"],
                "title": vacancy["name"],
                "url": vacancy["alternate_url"],
                "api": "HeadHunter",
            }
            salary = vacancy["salary"]
            if salary:
                formatted_vacancy["salary_from"] = salary["from"]
                formatted_vacancy["salary_to"] = salary["to"]
                formatted_vacancy["currency"] = salary["currency"]
            else:
                formatted_vacancy["salary_from"] = None
                formatted_vacancy["salary_to"] = None
                formatted_vacancy["currency"] = None
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class SuperJobAPI(API):
    url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": "v3.r.137610095.0dd7bc0929015ddd664d11aa1d40630d05c34006.2aceecd4cdef315cbfe73b148fc53c9cf1dc0147"
    }

    def __init__(self, keyword: str):
        self.params = {
            "count": 100,
            "keyword": keyword,
            "page": None,
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError('Ошибка полученя данных')
        return response.json()["objects"]

    def get_vacancies(self, page_count=1):
        self.vacancies = []
        for page in range(page_count):
            page_vacancies = []
            self.params["page"] = page
            print(f'{self.__class__.__name__[0:-3]}: Страница {page + 1}. ', end="")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(f'ошибка {error}')
            else:
                self.vacancies.extend(page_vacancies)
                print(f'Загружено вакансий - {len(page_vacancies)}')
            if len(page_vacancies) == 0:
                break

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy[
                    "payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"]
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies


class ParsingError(Exception):
    pass


class JsonFile:
    def __init__(self, keyword, vacancies_json):
        self.keyword = keyword
        self.filename = f'{keyword.lower()}.json'
        self.json_write(vacancies_json)

    def json_write(self, vacancies_json):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4)

    def json_read(self):
        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]

    def sort_by_salary_from(self):
        desc = True if input(
            "> - по убыванию\n"
            "< - по возрастанию\n"
            ">>> "
        ) == ">" else False
        vacancies = self.json_read()
        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from else 0, x.salary_to if x.salary_to else 0), reverse=desc)

    def filter_by_salary_from(self):
        filtered_vacancies = []
        minimal_salary = int(input(
            "Введите минимальную зарплату\n"
            ">>> "))
        vacancies = self.json_read()
        return sorted(vacancies, key=lambda x: (x.salary_from if x.salary_from and int(x.salary_from) >= minimal_salary else 0))
        # for vacancy in vacancies:
        #     if vacancy.salary_from:
        #         if int(vacancy.salary_from) >= minimal_salary:
        #             filtered_vacancies.extend(vacancy)


class Vacancy:
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
