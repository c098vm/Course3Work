from HHParcer import HHParcer
from SJParcer import SJParcer
from modules import modules
from modules.utils import sort_by_salary_from, filter_by_salary_from


def main():
    vacancies = []
    keyword = input("Введите ключевое слово для поиска вакансий\n"
                    ">>> ")
    print()

    pages_count = int(input('Сколько страниц вакансий загрузить с каждой платформы (не более 10)?\n'
                        '>>> '))
    print()

    if pages_count > 10:
        pages_count = 10

    vacancies_json = []

    hh = HHParcer.HeadHunterAPI(keyword)
    sj = SJParcer.SuperJobAPI(keyword)

    for api in [hh, sj]:
        api.get_vacancies(pages_count)
        vacancies_json.extend(api.get_formatted_vacancies())

    jsonfile = modules.JsonFile(keyword, vacancies_json)

    while True:
        print()
        print("Выберите команду\n"
              "1 - вывести список вакансий\n"
              "2 - отсортировать по минимальной зарплате\n"
              "3 - отфильтровать по минимальной зарплате\n"
              "0 - выход")
        command = input(">>> ")
        print()

        vacancies_data = jsonfile.json_read()

        if command == "0":
            break
        elif command == "1":
            vacancies = vacancies_data
        elif command == "2":
            vacancies = sort_by_salary_from(vacancies_data)
        elif command == "3":
            vacancies = filter_by_salary_from(vacancies_data)

        for vacancy in vacancies:
            print(vacancy)


if __name__ == "__main__":
    main()
