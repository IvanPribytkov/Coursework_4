import requests
from typing import List, Dict
from abc import ABC, abstractmethod

class VacancyAPI(ABC):
    """Класс для работы с API hh.ru."""

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Метод для получения вакансий с сайта hh.ru."""
        pass

class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru"

    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Метод для получения вакансий с сайта hh.ru."""
        url = f"{self.base_url}/vacancies"
        params = {"text": search_query}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            return []
