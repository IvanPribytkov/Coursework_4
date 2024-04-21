import unittest
from storage import Vacancy, JSONVacancyStorage


class TestJSONVacancyStorage(unittest.TestCase):
    def test_add_vacancy(self):
        storage = JSONVacancyStorage("test_vacancies.json")
        vacancy = Vacancy("Test Title", "https://example.com", "1000-2000 руб.", "Test Description")
        storage.add_vacancy(vacancy)
        self.assertEqual(len(storage.vacancies), 1)
        self.assertEqual(storage.vacancies[0].title, "Test Title")

    def test_delete_vacancy(self):
        storage = JSONVacancyStorage("test_vacancies.json")
        vacancy = Vacancy("Test Title", "https://example.com", "1000-2000 руб.", "Test Description")
        storage.add_vacancy(vacancy)
        storage.delete_vacancy(vacancy)
        self.assertEqual(len(storage.vacancies), 0)

    def test_filter_vacancies(self):
        storage = JSONVacancyStorage("test_vacancies.json")
        vacancy1 = Vacancy("Python Developer", "https://example.com/python", "1000-2000 руб.", "Python experience required")
        vacancy2 = Vacancy("Java Developer", "https://example.com/java", "2000-3000 руб.", "Java experience required")
        storage.add_vacancy(vacancy1)
        storage.add_vacancy(vacancy2)

        filtered_vacancies = storage.filter_vacancies("Python")
        self.assertEqual(len(filtered_vacancies), 1)
        self.assertEqual(filtered_vacancies[0].title, "Python Developer")

        filtered_vacancies = storage.filter_vacancies("Developer")
        self.assertEqual(len(filtered_vacancies), 2)
        self.assertEqual(filtered_vacancies[0].title, "Python Developer")
        self.assertEqual(filtered_vacancies[1].title, "Java Developer")

        filtered_vacancies = storage.filter_vacancies("Java")
        self.assertEqual(len(filtered_vacancies), 1)
        self.assertEqual(filtered_vacancies[0].title, "Java Developer")


if __name__ == "__main__":
    unittest.main()
