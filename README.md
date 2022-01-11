# Яндекс.Практикум. Python backend. Дипломный проект

### Описание

Foodgram проект для публикации рецептов. Можно добавлять их в избранное, подписываться на авторов понравившхся рецептов, и загружать список ингредиентов для рецептов добавленных в вашу корзину.
#### Демо (не) запущено по адресу http://51.250.26.225 (Yandex Cloud) (если сильно надо - подниму, покажу)

### Технологии

В проекте применяется 
### Data Base
- **PostgreSQL**
### Frontend
- **React**
### Backend:
- **Django 3.2**
- **DRF**
- **Python 3**
### Deploy
- **Docker**
- **Nginx**
- **Gunicorn**
- **Git**

### <a name="Запуск проекта">Запуск проекта</a>

- Установите Docker и Docker-compose:
```bash
 sudo apt install docker.io
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 sudo chmod +x /usr/local/bin/docker-compose
```
- Скопируйте на сервер файлы Docker-compose.yml и nginx.conf из папки infra-deploy/.
- Деплой и сборка:
```bash
 sudo docker-compose rm -f backend --build
```
- Собрать статику для админ панели:
```bash
  docker-compose exec backend python3 manage.py collectstatic --noinput
```
- Создаем миграции и мигрируем:
```bash
 docker exec -it <CONTAINER ID> bash
 python manage.py makemigrations
 python manage.py migrate --noinput
```

- Создаём суперпользователя в контейнер
```bash
python manage.py createsuperuser
```
- Запустить все контейнеры:
```python
 docker-compose up
```
### Автор
```
 Роман Черкасов - backend
 Ребята из Yandex Practicum - frontend
```

### Описание основных эндпоинтов:
```
POST http://localhost:8000/api/users/ - регистрация
POST http://localhost:8000/api/auth/token/login - создание токена
GET http://localhost:8000/api/users/ - Просмотр информации о пользователях

POST http://localhost:8000/api/users/set_password/ - Изменение пароля
GET http://localhost:8000/api/users/4/subscribe/ - Подписаться на пользователя
DEL http://localhost:8000/api/users/4/subscribe/ - Отписаться от пользователя

POST http://localhost:8000/api/recipes/ - Создать рецепт
GET http://localhost:8000/api/recipes/ - Получить рецепты
GET http://localhost:8000/api/recipes/<id>/ - Получить рецепт по id
DEL http://localhost:8000/api/recipes/<id>/ - Удалить рецепт по id

GET http://localhost:8000/api/recipes/<id>/favorite/ - Добавить рецепт в избранное
DEL http://localhost:8000/api/recipes/<id>/favorite/ - Удалить рецепт из избранного

GET http://localhost:8000/api/users/<id>/subscribe/ - Подписаться на пользователя
DEL http://localhost:8000/api/users/<id>/subscribe/ - Отписаться от пользователя

GET http://localhost:8000/api/ingredients/ - Получить список всех ингредиентов

GET http://localhost:8000/api/tags/ - Получить список всех тегов

GET http://localhost:8000/api/recipes/<id>/shopping_cart/ - Добавить рецепт в корзину
DEL http://localhost:8000/api/recipes/<id>/shopping_cart/ - Удалить рецепт из корзины
```
