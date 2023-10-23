# Учебный проект Продуктовый помощник - Foodgram

## Cайт доступен по ссылке:
- URL: https://yandex52.ddns.net
- ip: 158.160.15.191

## Администратор (логин, пароль)
- root@gmail.com
- root


## О проекте
### На этом сайте пользователи, зарегистрировавшись, могут:
- публиковать рецепты,
- добавлять чужие рецепты в избранное
- подписываться на публикации других авторов.
- «cписок покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. Есть возможность выгрузить файл (.txt) с перечнем и количеством необходимых ингредиентов для рецептов.

## Стек технологий
- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- gunicorn
- Docker
- Docker Hub
- GitHub

## Используемые библиотеки

- Django==3.2
- django-filter==23.2  
- djangorestframework==3.12.4
- djoser==2.2.0
- gunicorn==20.1.0
- Pillow==9.5.0
- psycopg2-binary==2.9.6


### Использование Continuous Integration и Continuous Deployment (CI/CD).
При выполнении Push в ветку master репозитория GitHub выполнятся сценарии:
1. Автоматически запускаются тесты на GitHub
2. При успешном прохождении тестов, обновляются образы на Docker Hub
3. Автоматическая загрука образов с Docker Hub на продакш сервер
4. Автоматическое разворачивание и запуск серверов в контенерах на продакшн сервере
5. В случае успеха отправка сообщения об этом в телеграмм-бот
После выполнения все пунктов сайт становится доступным в сети интернет.

# Как работать с репозиторием Foodgram
1. Клонировать репозиторий и перейти в папку в командной строке

```
git clone https://github.com/vitaliksherbakov/foodgram-project-react
```

2. Запустить сервер в контейнерах
Для первого запуска, находясь в папке проекта, выполнить команду:

```
docker compose up --build
```

В скрипте (по ключу --build) автоматически соберуться контейнеры, выполнится запуск серверов в них. Последующие запуски сервера не требуют ключа --build

```
3. Заполнить базу начальными данными.
```
docker exec foodgram_backend python manage.py import_data
```
База данных заполнится: таблица ингредиентов(название, ед.измерения), таблица первоначальных тэгов (завтрак, обед, ужин). В админ зоне возможно добавление и редактирование данных этих таблиц.

4. Запустить в контенере Bash и Создать суперпользователя
```
docker exec -it foodgram_backend bash
python manage.py createsuperuser
```
5. Выйдите из контейнера
```
exit
```

### Запустить в браузере

```
http://localhost:9000
```


# Примеры запросов API
## Рецепты
- Список рецептов:
Страница доступна всем пользователям. Доступна фильтрация по избранному, автору, списку покупок и тегам.
> Запрос GET 
http://localhost/api/recipes/

QUERY PARAMETERS
page	(integer) Номер страницы.

limit	(integer) Количество объектов на странице.

is_favorited	(integer) Показывать только рецепты, находящиеся в списке избранного.

is_in_shopping_cart	(integer) Показывать только рецепты, находящиеся в списке покупок.

author	(integer) Показывать рецепты только автора с указанным id.

tags	(Array of strings) Example: tags=lunch&tags=breakfast Показывать рецепты только с указанными тегами (по slug)

> Ответ
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}

- Создание рецепта (Доступно только авторизованному пользователю)
> Запрос POST
http://localhost/api/recipes/

ingredients (required) (Array of objects) Список ингредиентов

    Array: 
        id (required)   (integer) Уникальный id

        amount (required)   (integer) Количество в рецепте

tags (required) (Array of integers) Список id тегов

image (required)    (string <binary>) Картинка, закодированная в Base64

name (required) (string <= 200 characters) Название

text (required) (string) Описание

cooking_time (required) (integer >= 1) Время приготовления (в минутах)

> Ответ
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}

> Получение рецепта GET
http://localhost/api/recipes/{id}/

id (required) (string) Уникальный идентификатор этого рецепта

> Ответ
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}




## Автор
Vitalik Sherbakov
