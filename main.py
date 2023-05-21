import os


def run_server(make_migrations):
    if make_migrations:
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    migrations = input('Выполнить миграции? Y/N : ').lower()
    migrations = 1 if migrations == 'y' else 0
    run_server(migrations)
