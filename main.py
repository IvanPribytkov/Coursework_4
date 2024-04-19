from abc import ABC, abstractmethod
from typing import List, Dict
import requests
import json


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Метод для получения вакансий по запросу."""
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_vacancies(self, search_query: str) -> List[Dict]:
        url = f"{self.base_url}/vacancies"
        params = {"text": search_query}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            return []


class Vacancy:
    """Класс для представления вакансии."""

    def __init__(self, title: str, link: str, salary: str, description: str):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления вакансии в хранилище."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для удаления вакансии из хранилища."""
        pass

    @abstractmethod
    def filter_vacancies(self, search_query: str) -> List[Vacancy]:
        """Метод для фильтрации вакансий по ключевому слову."""
        pass


class JSONVacancyStorage(VacancyStorage):
    """Класс для работы с хранилищем вакансий в формате JSON."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.vacancies: List[Vacancy] = []
        self.load_from_json()

    def add_vacancy(self, vacancy: Vacancy) -> None:
        self.vacancies.append(vacancy)
        self._save_to_json()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        if vacancy in self.vacancies:
            self.vacancies.remove(vacancy)
            self._save_to_json()

    def filter_vacancies(self, search_query: str) -> List[Vacancy]:
        filtered_vacancies = []
        for vacancy in self.vacancies:
            if search_query.lower() in vacancy.title.lower() or search_query.lower() in vacancy.description.lower():
                filtered_vacancies.append(vacancy)
        return filtered_vacancies

    def _save_to_json(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump([vars(vacancy) for vacancy in self.vacancies], file, indent=4)

    def load_from_json(self) -> None:
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.vacancies = [Vacancy(**vacancy_data) for vacancy_data in data]
        except FileNotFoundError:
            pass


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
