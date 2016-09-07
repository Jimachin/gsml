# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import env, require, run, sudo, cd, prefix
from fabric.contrib.files import exists

__author__ = 'javiermachin'


"""
Fabric configuration file to deploy an web application
"""

def prod():
    """Server remote to production." \

    """
    env.name = 'prod'
    env.user = 'azureuser'
    env.project_name = 'Gosocket_API'
    env.hosts = ['gomachlearning.cloudapp.net']
    env.branch = 'master'
    env.repo = 'https://github.com/Jimachin/gsml.git'
    env.project_root = '/home/ubuntu/src/%(project_name)s/' % env
    env.logs = '/home/ubuntu/logs/%(project_name)s/' % env
    env.venv = '/home/ubuntu/venvs/%(project_name)s/' % env


#--------------------------------------
#commands
#--------------------------------------

def deploy():
    """Deploy application in a virtualenv. Recommended to servers with Django application multiples.

    """
    require('name')
    require('venv')
    download_site()
    setup_pip_requirements()
    apply_local_settings()
    virtualenv_syncdb()
    # virtualenv_initial_data()
    virtualenv_collect_static()
    compile_messages()
    gunicorn_conf()
    supervisor_conf()
    supervisor_restart()
    nginx_conf()
    nginx_restart()


def full_deploy():
    """Deploy the application with all requirements in one environment. Recommened to deploy the first time.

    """
    setup_requirements()
    setup_directories()
    create_virtualenv()
    deploy()


def fast_deploy():
    """Deploy the application quickly in one environment. Don't install dependencies. Don't synchronize the
    models with the database.

    """
    require('name')
    require('venv')
    download_site()
    # virtualenv_initial_data()
    apply_local_settings()
    virtualenv_collect_static()
    compile_messages()
    supervisor_restart()


def compile_messages():
    """Compile the files for language translation.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('python manage.py compilemessages')


def setup_requirements():
    """Setup required packages via OS package manager.

    """
    sudo("apt-get update")
    sudo("apt-get install git -y")
    sudo("apt-get install python-imaging -y")
    sudo("apt-get install libjpeg-dev libjpeg62 zlib1g-dev libffi-dev libfreetype6 libfreetype6-dev python2.7-dev -y")
    sudo("apt-get install python2.7 -y")
    sudo("apt-get install python-setuptools python-pip -y")
    sudo("apt-get install python-virtualenv")
    sudo("apt-get install libmysqlclient-dev mysql-client -y")
    sudo("apt-get install nginx -y")
    sudo("apt-get install supervisor -y")
    sudo("apt-get install sysv-rc-conf -y")
    sudo("apt-get install libevent-dev -y")
    sudo("apt-get install gettext -y")


def git_clone():
    """
    Clone git repo
    """
    run("git clone %(repo)s %(project_root)s" % env)
    with cd(env.project_root):
        run("git checkout %(branch)s" % env)


def git_pull():
    """Pulls the site from the specified repository's branch.

    """
    with cd(env.project_root):
        run("git pull origin %(branch)s" % env)


def download_site():
    """
    Pulls files from repo or clone if required
    Also set permissions for web server access
    """

    if exists("%(project_root)s/.git/" % env):
        git_pull()
    else:
        git_clone()


def setup_directories():
    """Setups the required directories and permissions.

    """
    run("mkdir -p %(project_root)s" % env)
    run("mkdir -p %(venv)s" % env)
    run("mkdir -p %(logs)s" % env)

    sudo("chown -R %(user)s:www-data %(project_root)s" % env)


def create_virtualenv():
    """Create required folders and setups virtual environment, if necessary.

    """
    require("venv")
    if not exists("%(venv)s/bin/python" % env):
        run("virtualenv %(venv)s" % env)


def setup_pip_requirements():
    """Install PIP requirements in virtual environment.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('pip install -r requirements/%(name)s.txt' % env)
    """
    with cd(env.project_root):
        run('pip install -r requirements.pip -E %(venv)s' % env)
    """


def apply_local_settings():
    """Copy custom site settings to site's root.

    """
    with cd(env.project_root):
        run("cp -f conf/%(name)s/local_settings.py local_settings.py" % env)


def virtualenv_syncdb():
    """Syncronize db with Django's models.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run("python manage.py migrate")


def virtualenv_compress():
    """Compress Django's statics files.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('python manage.py compress')


def virtualenv_collect_static():
    """Collect Django's statics files.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('python manage.py collectstatic --noinput')


def gunicorn_conf():
    """Copy gunicorn configuration for this site.

    """
    with cd(env.project_root):
        run("cp -f conf/%(name)s/gunicorn.conf gunicorn.conf" % env)
        run("cp -f conf/%(name)s/gunicorn.sh gunicorn.sh" % env)
        sudo("chmod +x gunicorn.sh")


def nginx_conf():
    """Copy and activate nginx configuration for this site.

    """
    with cd(env.project_root):
        sudo("cp --remove-destination conf/%(name)s/nginx.conf /etc/nginx/sites-available/%(project_name)s.conf" % env)
        if not exists("/etc/nginx/sites-enabled/%(project_name)s.conf" % env):
            sudo("ln -s /etc/nginx/sites-available/%(project_name)s.conf /etc/nginx/sites-enabled/" % env)


def supervisor_conf():
    """
    Copy supervisor configuration for this site
    """
    with cd(env.project_root):
        sudo("cp -f conf/%(name)s/supervisor.conf /etc/supervisor/conf.d/%(project_name)s.conf" % env)
        sudo("chmod 777 /etc/supervisor/conf.d/%(project_name)s.conf" % env)
        run("mkdir -p %(logs)s" % env)
        run("touch %(logs)ssupervisor-out.log" % env)
        run("touch %(logs)ssupervisor-err.log" % env)
        sudo("supervisorctl update" % env)


def supervisor_restart():
    """Copy supervisor configuration for this site.

    """
    sudo("supervisorctl restart %(project_name)s" % env)


def clean():
    """Clear out extraneous files, like pyc/pyo.

    """
    with cd(env.project_root):
        run("""find -type f -name "*.py[co~]" -delete""")


def nginx_restart():
    """Reload nginx configuration.

    """
    sudo("service nginx restart")


def virtualenv_initial_data():
    """Load initial data from initial_data.json.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('python manage.py loaddata initial_data')


def virtualenv_demo_data():
    """Load demo data from demo_data.json.

    """
    with cd(env.project_root):
        with prefix("source %(venv)s/bin/activate" % env):
            run('python manage.py loaddata demo_data')
