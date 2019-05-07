# Веб-сервис файлообменник

## Задание
На главной странице форма загрузки файлов и поле ввода времени жизни файла. По сабмиту формы файл грузится на сервер. По истечению срока жизни файла он удаляется с сервера, вместо файла пользователь получает страницу 404.

Доп задания:
1. Форма работает через AJAX
2. Сохранение файлов в персистентное хранилище (sql/redis/mongo/etc)
3. Авторизация, можно получить список файлов, созданных авторизованным пользователем
4. Отдельная страница для файла, на котором видно сколько осталось жить этому файлу

## Using
Репозиторий: https://github.com/vodono/filex
Деплой проекта: https://fileex.herokuapp.com/

#### Для запуска проекта локально нужно:
1) создать виртуальное окружение Python и активировать его:
    ```linux
    $ virtualenv venv --python=/usr/local/bin/python3.7
    $ . venv/bin/activate
    ```
1) установить необходимые пакеты:
    ```linux
    $ pip install -r requirements.txt
    ``` 
1) создать базу Postgres в консоли саймой БД:
    ```sql
     # create role filex with createdb createrole login encrypted password 'files';
     # create database files with owner=filex encoding=UTF8;
    ```
1) применить миграции к созданной БД в терминале ОС в папке проекта file_ex:
    ```linux
    $ python src/manage.py upgrade
    ```
1) запустить веб-серверв терминале ОС в папке проекта file_ex:
    ```linux
    $ python src/local_run.py
    ```
1) локальный веб-сайт будет доступен по адресу http://127.0.0.1:5000/

#### Для запуска проекта на сайте heroku.com:
1) создать аккаунт на heroku.com установить консоль:
    ```linux
    $ sudo snap install --classic heroku
    ```
1) создать проект (название может быть не доступно):
    ```linux
    $ heroku apps:create fileex
    ```
1) через команды git сохранить проект на remote (heroku or other, данный проект подключен к своему аккаунту github):
    ```linux
    $ git push heroku master
    ```
1) добавляем postgres:
    ```linux
    $ heroku addons:create heroku-postgresql:hobby-dev --app fileex
    ```
1) применить миграции:
    ```linux
    $ heroku run python src/manage.py db upgrade --app fileex
    ```
1) сайт доступен по адресу: https://fileex.herokuapp.com/
