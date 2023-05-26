import os


def run_server(cmds):
    for cmd, flag in cmds.items():
        if flag:
            os.system(f'python manage.py {cmd}')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    cmds = {
        'runapscheduler': False,
        'makemigrations': False,
        'migrate': False,
        'prepare_news': False,
        'collectstatic': False,
    }
    for cmd in cmds.keys():
        cmds[cmd] = input(f'Выполнить {cmd}? Y/N : ').lower() == 'y'
    run_server(cmds)
