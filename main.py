from api import HeadHunterAPI, VacancyAPI
from storage import JSONVacancyStorage, VacancyStorage
from models import Vacancy

def user_interaction(api: VacancyAPI, storage: VacancyStorage) -> None:
    search_query = input("Введите поисковый запрос: ")
    vacancies = api.get_vacancies(search_query)
    if vacancies:
        vacancies_list = [Vacancy(vacancy["name"], vacancy["url"], vacancy.get("salary", "Зарплата не указана"),
                                  vacancy.get("description", "")) for vacancy in vacancies]
        for vacancy in vacancies_list:
            storage.add_vacancy(vacancy)

        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ")
        filtered_vacancies = storage.filter_vacancies(filter_words)

        sorted_vacancies = sorted(filtered_vacancies, key=lambda x: int(x.salary.split("-")[0].replace(" ", "")),
                                  reverse=True)[:top_n]
        if sorted_vacancies:
            print("Топ вакансий:")
            for vacancy in sorted_vacancies:
                print(f"{vacancy.title}: {vacancy.salary}")
        else:
            print("Не найдено вакансий по заданным критериям")
    else:
        print("Не удалось получить вакансии с сервера")


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    json_storage = JSONVacancyStorage("vacancies.json")
    user_interaction(hh_api, json_storage)
