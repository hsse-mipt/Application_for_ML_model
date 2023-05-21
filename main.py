import os


def run_server(make_migrations, preparse_news):
    if make_migrations:
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
    if preparse_news:
        os.system('python manage.py prepare_news')
    os.system('python manage.py runapscheduler')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    migrations = input('Выполнить миграции? Y/N : ').lower()
    migrations = migrations == 'y'
    preparse = input('Обновить новости? Y/N : ').lower()
    preparse = preparse == 'y'
    run_server(migrations, preparse)
