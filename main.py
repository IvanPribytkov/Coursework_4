from api import HeadHunterAPI
from storage import JSONVacancyStorage
from interaction import user_interaction

if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    json_storage = JSONVacancyStorage("vacancies.json")
    user_interaction(hh_api, json_storage)
