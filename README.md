# Library Project

![Иллюстрация к проекту](https://github.com/nsat1/sup/blob/main/library.png)

Этот проект представляет собой систему управления библиотекой, позволяющую просматривать, добавлять, изменять и удалять книги, а также отслеживать выдачу книг читателям.

## Требования

- Python 3.8+
- Django 3.2+
- Django REST Framework
- Django Simple History
- Другие зависимости указаны в файле `requirements.txt`

## Установка

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/yourusername/library-project.git
    cd library-project
    ```

2. **Создайте виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Linux/Mac
    venv\Scripts\activate  # Для Windows
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте параметры PostgreSQL:**
5. 
В файле `library_project/settings.py/`
``
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your db name',
        'USER': 'your user name',
        'PASSWORD': 'your password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
``
4. **Примените миграции:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Создайте суперпользователя:**

    ```bash
    python manage.py createsuperuser
    ```

6. **Запустите сервер разработки:**

    ```bash
    python manage.py runserver
    ```

## Основная структура проекта

- `library_app/` - Основное приложение библиотеки.
  - `models.py` - Определение моделей.
  - `views.py` - Определение представлений.
  - `serializers.py` - Сериализаторы для API.
  - `admin.py` - Настройка админ-панели.
- `library_project/` - Основной конфигурационный файл проекта.
  - `settings.py` - Настройки проекта.
  - `urls.py` - Маршруты проекта.
- `templates/` - Шаблоны HTML.

## API

Проект включает API, доступное по следующим эндпоинтам:

- `/api/books/` - Список книг.
- `/api/borrow/<int:book_id>/` - Взять книгу.
- `/api/return/<int:book_id>/` - Вернуть книгу.
- `/api/my_books/` - Список книг на руках у текущего пользователя.
- `/api/docs/` - документация.

## Админ-панель

Админ-панель доступна по адресу `/admin/` и позволяет:

- Просматривать, создавать, изменять и удалять пользователей.
- Просматривать, создавать, изменять и удалять книги.
- Просматривать, создавать, изменять и удалять записи о выдаче книг.
- Фильтровать записи о выдаче книг по тем, кто еще не вернул книгу.
- Просматривать историю изменений в моделях книг.


## Для запуска используйте команду:

```bash
python manage.py runserver
