import requests
import json
import time


keywords = ["Python", "Django", "FastAPI"]

PER_PAGE = 100


OUTPUT_FILE = "vacancies.json"


def fetch_vacancies(keyword):
    vacancies = []
    page = 0

    while True:
        try:
            url = "https://api.hh.ru/vacancies"
            params = {
                "text": keyword,
                "per_page": PER_PAGE,
                "page": page
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = dict(response.json())

            if not data.get("items"):
                break

            vacancies.extend(data["items"])


            page += 1
            if page >= data.get("pages", 0):
                break
            time.sleep(0.1)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}. Попробуем снова через 5 секунд...")
            time.sleep(5)
            continue
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON, пропускаем страницу")
            page += 1
            continue

    return vacancies

def main():
    all_vacancies = []

    for keyword in keywords:
        print(f"Собираем вакансии по ключевому слову: {keyword}")
        vacancies = fetch_vacancies(keyword)
        all_vacancies.extend(vacancies)
        print(f"Найдено {len(vacancies)} вакансий для '{keyword}'")

    # Сохраняем все вакансии в JSON файл
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_vacancies, f, ensure_ascii=False, indent=4)

    print(f"Всего вакансий сохранено: {len(all_vacancies)}")
    print(f"Файл сохранён: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()



