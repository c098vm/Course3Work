import HHParcing
import SJParcing
import modules


def main():
    keyword = input("Введите ключевое слово для поиска вакансий\n"
                    ">>> ")
    # keyword = "C++"
    print()
    vacancies_json = []

    hh = HHParcing.HeadHunterAPI(keyword)
    sj = SJParcing.SuperJobAPI(keyword)

    for api in [hh, sj]:
        api.get_vacancies()
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
        if command == "0":
            break
        elif command == "1":
            vacancies = jsonfile.json_read()
        elif command == "2":
            vacancies = jsonfile.sort_by_salary_from()
        elif command == "3":
            vacancies = jsonfile.filter_by_salary_from()

        for vacancy in vacancies:
            print(vacancy)

if __name__ == "__main__":
    main()
