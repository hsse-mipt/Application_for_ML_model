import os


def run_server(cmds: dict):
    for cmd, flag in cmds.items():
        if flag:
            os.system(f'python manage.py {cmd}')
    os.system('python manage.py runserver')


def activate_cmds():
    cmds = {
        'runapscheduler': False,
        'makemigrations': False,
        'migrate': False,
        'prepare_news': False,
        'collectstatic': False,
    }

    for cmd in cmds.keys():
        cmds[cmd] = input(f'Execute manage.py {cmd}? Y/N : ').lower() == 'y'

    return cmds


if __name__ == '__main__':
    run_server(activate_cmds())
