from fabricant import *

#env.project = 'cony.svetlyak.ru'

def dev():
    env.hosts = ['localhost']
    env.environment = 'development'
    env.project_dir = '/vagrant/cony'


def production():
    env.hosts = ['people']
    env.environment = 'production'
    env.project_dir = '/home/art/projects/cony'
    env.repository = 'git@github.com:svetlyak40wt/cony.git'
    use_ssh_config(env)


def _pull_sources():
    if env.environment == 'production':

        base_dir, relative_project_dir = os.path.split(env.project_dir)
        with cd(base_dir):
            if dir_exists(relative_project_dir):
                with cd(relative_project_dir):
                    run('git pull', forward_agent=True)
            else:
                run('git clone %s %s' % (env.repository, relative_project_dir))


def _create_env():
    with cd(env.project_dir):
        if not dir_exists('env'):
            run('virtualenv env')
        run('env/bin/pip install -r requirements/%s.txt' % env.environment)


def deploy():
    package_ensure([
        'nginx',
    ])
    dir_ensure([
        '/home/art/log/backend',
        '/home/art/log/supervisord',
        '/home/art/projects',
    ])

    _pull_sources()
    _create_env()
    make_symlinks()

    upstart_ensure('nginx')


def runserver():
    local('./cony-server')

