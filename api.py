from abc import ABC, abstractmethod
from typing import List, Dict
import requests

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
