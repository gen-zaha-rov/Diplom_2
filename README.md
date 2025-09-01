# Diplom_2

В данном проекте выполнены автоматизированные тесты для проверки API для Stellar Burgers с использованием pytest и генерации отчётов Allure.

## Как запустить тесты

1. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустить тесты с генерацией Allure-отчёта:
   ```bash
    pytest --alluredir=allure-results
   ```
3. Просмотреть отчёт:
   ```bash
    allure serve allure-results 
   ```  
   
## Дополнительная информация

* Python 3.9.5

* Тестовый стенд: https://stellarburgers.nomoreparties.site/

* Документация API: https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/api-documentation.pdf?etag=3403196b527ca03259bfd0cb41163a89  