from typing import List
from api import VacancyAPI
from storage import Vacancy, VacancyStorage

def user_interaction(api: VacancyAPI, storage: VacancyStorage) -> None:
    """Функция для взаимодействия с пользователем."""
    search_query = input("Введите ваш поисковый запрос: ")
    vacancies = api.get_vacancies(search_query)
    if vacancies:
        vacancies_list = [Vacancy(vacancy["name"], vacancy.get("url", ""), vacancy.get("salary", "Зарплата не указана"), vacancy.get("description", "")) for vacancy in vacancies]
        for vacancy in vacancies_list:
            storage.add_vacancy(vacancy)

        top_n = int(input("Введите количество вакансий для отображения в топе: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ")
        filtered_vacancies = storage.filter_vacancies(filter_words)

        sorted_vacancies = sorted(filtered_vacancies, key=lambda x: int(x.salary.split("-")[0].replace(" ", "")), reverse=True)[:top_n]
        if sorted_vacancies:
            print("Топ вакансий:")
            for vacancy in sorted_vacancies:
                print(f"{vacancy.title}: {vacancy.salary}")
        else:
            print("По заданным критериям вакансии не найдены")
    else:
        print("Не удалось получить вакансии с сервера")
