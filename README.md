![example workflow](https://github.com/AndreyVnk/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
# API YaMDB

**API YaMDB** - командный проект, поддерживающий обмен данными в формате *JSON*. Развернут в 3х контейнерах (db, web, nginx) c помощью Docker.

Настроены CI и CD: автоматический запуск тестов (PEP8, Pytest), обновление образов на Docker Hub,автоматический деплой на боевой сервер при пуше в ветку master.

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
git clone https://github.com/AndreyVnk/yamdb_final.git && cd yamdb_final/
```
### 2. Добавить Action Secrets
```
DOCKER_USERNAME=<docker login>
DOCKER_PASSWORD=<docker password>
USER=<server_user>
HOST=<server_ip_address>
SSH_KEY=<public_key> # cat ~/.ssh/id_rsa (linux)
TELEGRAM_TO=<chat ID> # для отправки уведомлений в телеграм
TELEGRAM_TOKEN=<bot_token>
SECRET_KEY=secret_django_key
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=zzzxxxcc # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
### 3. Изменить настройки default.conf в папке nginx/
```
server_name <server_ip_address>;
```
### 4. Подготовьте сервер
Установите docker и docker-compose
```
https://docs.docker.com/engine/
```
### 5. Выполнить копирование файлов docker-compose.yaml и nginx/default.conf на сервер
```
scp ./infra/docker-compose.yaml <user>@<ip_address>:/home/<user>/docker-compose.yaml
scp ./infra/nginx/default.conf <user>@<ip_address>:/home/<user>/nginx/default.conf
```
### 6. Выполнить commit и push проекта
```
git add .
git commit -m '*something*'
git push
```
### 7. На сервере выполнить следующие команды
```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py collectstatic --no-input
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py changepassword <username superuser>
```
Эндпоинты, описанные в документации доступны на корневом адресе проекта: http://<server_ip_address>/api/v1/ . Документация к API доступна на http://<server_ip_address>/redoc/ .

**Авторы**

AndreyVnk, deorz, idudnikov
