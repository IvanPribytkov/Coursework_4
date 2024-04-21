from abc import ABC, abstractmethod
from typing import List
import json
from models import Vacancy

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
