import requests
from modules.modules import API, ParsingError


class SuperJobAPI(API):
    """ Класс получения данных через API SuperJob """
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
        """ Метод запроса json-данных через API """
        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError('Ошибка полученя данных')
        return response.json()["objects"]

    def get_vacancies(self, page_count=1):
        """ Метод сохранения вакансий в список"""
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
        """ Метод приводит ключи словарей с вакансиями к единому виду """
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
