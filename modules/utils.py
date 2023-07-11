def sort_by_salary_from(vacancies):
    """ Функция сортировки вакансий по минимальной зарплате """
    desc = True if input(
        "> - по убыванию\n"
        "< - по возрастанию\n"
        ">>> "
    ) == ">" else False
    return sorted(vacancies, reverse=desc)


def filter_by_salary_from(vacancies):
    """ Функция фильтрации вакансий по минимальной зарплате """
    minimal_salary = int(input(
        "Введите минимальную зарплату\n"
        ">>> "))
    return sorted(vacancies, key=lambda x: (int(x.salary_from) >= minimal_salary if x.salary_from else 0))

