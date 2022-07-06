![example workflow](https://github.com/AndreyVnk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# API YaMDB

**API YaMDB** - командный проект, поддерживающий обмен данными в формате *JSON*. 

Настроены CI и CD: автоматический запуск тестов (PEP8, Pytest), обновление образов на Docker Hub,автоматический деплой на боевой сервер при пуше в главную ветку main.

Cистема аутентификация реализована через получение JWT-токена. Функционал API предоставляет следующие ресурсы:

- Произведения
- Категории
- Жанры
- Отзывы
- Комментарии


**Технологии:**

* Python 3
* Django Rest Framework
* Simple JWT
* PostgreSQL
* Docker

## Запуск проекта ##
### 1. Склонировать репозиторий
```
git clone https://github.com/AndreyVnk/yamdb_final.git
```
### 2. Создать виртуальное окружение и активировать его
Перейти в папку с проектом _yamdb_final/_ выполнить команды
```
python -m venv venv
source venv/Scripts/activate (для Windows) | source venv/bin/activate (для Linux)
```
### 3. Создать в папке infra/ и заполнить файл _.env_
```
SECRET_KEY=secret_django_key
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=zzzxxxcc # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
### 4. Установить необходимые пакеты
```
pip install -r api_yamdb/requirements.txt
```
### 5. Выполнить миграции
Из папки *yamdb_final/api_yamdb/*, выполнить команду
```
python manage.py migrate
```
### 6. Запустить проект
```
python manage.py runserver
```
Эндпоинты, описанные в документации доступны на корневом адресе проекта: http://127.0.0.1:8000/api/v1/ . Документация к API доступна на http://127.0.0.1:8000/redoc/ .

**Авторы**

AndreyVnk, deorz, idudnikov
