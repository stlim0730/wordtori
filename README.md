# Word2RI

## Instructions for Developers

### 1. Install all the prerequisites below
  - [Virtual Box](https://www.virtualbox.org/): tested on 2.2.4
  - [Vagrant](https://www.vagrantup.com/): tested on 6.0
  - [Git](https://git-scm.com/downloads): tested on 2.20.1

### 2. Clone the repository

```
git clone https://github.com/stlim0730/wordtori.git
```

This command creates a new directory `wordtori`. In case you want multiple instances of the local repository on the same machine (e.g., running two different instances of the app on a production server), you may specify the path.

```
mkdir meaningofhome
git clone https://github.com/stlim0730/wordtori.git meaningofhome
```

This command doesn't create a new directory.

### 3. Configure local settings

For security reasons, The app doesn't store credentials in this project repository. Instead, you should create `wordtori/local_settings.py` (same path as `settings.py`) containing a few environmental variables for development environment (likewise, you may safely manage settings for production environment separately). The format is as follows. You may add other settings variables here for the local settings.

```
# wordtori/local_settings.py

# Generate a Django secret key and paste it here: https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

DEBUG = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'wordtori',
    'USER': 'ubuntu',
    'PASSWORD': '', # Leave it empty
    'PORT': '5432'
  }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wordtori.noreply'
EMAIL_HOST_PASSWORD = '<password>'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# GitHub credentials below are required for automatic backup for model data.
# The default value is None. If you leave the credentials None,
# the app works normally, but the data is not automatically backed up in the remote repo.
# GITHUB_ACCOUNT = '' # e.g., 'tap2k'
# GITHUB_PASSWORD = '' # e.g., 'mypassword'
# EMAIL_ADDRESS = '' # e.g., 'tsp53@cornell.edu'
```

### 4. Choose an app instance

Word2RI manages multiple instances of the app using Git branches, where each app instance has its own variations of contents and configurations. One branch may represent an instance of the app (Note that there can be normal feature branches for development purpose, which isn't a representative branch for an app instance). You can lookup what branches are available in the remote repository (GitHub) using the following command.

```
git fetch --all
```

`git fetch` command collects all the updates from remote, but doesn't `merge` any of them into the current working tree in the local repository.

```
git branch
git branch --remote
git branch --all
```

`git branch` shows you the local branches available. You may use option `--remote` (or `-r`) to lookup branches in the remote repository; it's useful because the branches representing app instances would have been already built and available in the remote repository. You may switch to one of app instances by checking out a branch.

```
git checkout meaning-of-home
```

### 5. Create (turn on) a virtual machine

Word2RI runs on Ubuntu 16.04 (code name: ubuntu/xenial64). Provisional commands and configurations for virtual machine are in `deployment/provision_vagrant.sh`. `Vagrantfile` specifies the provision script to run when a virtual machine is created. Create a virtual machine with the following command in the repository root (where you cloned it) directory.

```
vagrant up
```

Now, your local instance of the app is running at [http://localhost:8888](http://localhost:8888), where the port number is specified in `Vagrantfile`. You may use the shell of the virtual machine by ssh command.

```
vagrant ssh
```

The first thing you may want to do is make admin account for Django. For security reasons, Django doesn't allow you to do this in scripted way, but in interactive way. Run the following command in the repository root.

```
cd /wordtori #(or /meaningofhome)
python3 manage.py createsuperuser
```

You now can use Django admin tool at [http://localhost:8888/admin](http://localhost:8888/admin).

If you want to add non-superuser staff account (e.g., teacher and student accounts used for meaningofhome), use the same command on the production server and configure the account on admin UI. Note that they are superusers without any limitations by default, so you should configure the permission on admin UI.

### 6. Making changes in the code
_IN PROGRESS_

Once you made changes, there are a few commands to run to apply the changes before you run the updated version of the app. In case you modified things related to database, models (schema), you need to migrate database to a new version.

```
python3 manage.py makemigrations
```

`makemigrations` command of Django generates migration files to use. After running this, you can apply the migration changes as follows. Note that `makemigrations` has to precede `migrate`.

```
python3 manage.py migrate
```

When you made changes in static assets (HTML, css, JavaScript, images, etc.), You should let Django collect it in a dedicated path using `collectstatic` commannd.

```
python3 manage.py collectstatic
```

If you want to reload the server to apply changes in Django code, run the shorcut below.

```
touch reload.ini
```

`uwsgi` module running on Nginx listens to the "touch" on `reload.ini` to reload the app.

### 7. Deploy the updates

If you're deploying master branch, first merge the feature branches you completed into master branch on GitHub. If not, merge is not necessary.

Once the branch you want to deploy is ready, ssh into the production server with root account. Ask the repository owner on the credentials.

```
ssh root@wordtori.com
```

And then, move to the local repository. Note that the server is currently running two instances of the app.

```
cd /wordtori
# or
cd /meaningofhome
```

Make sure you're on the right branch to update and pull the branch.

```
git branch --all
git checkout master
# or
git checkout meaning-of-home
git pull
```

To apply the changes, follow the section 6.

### 8. Teardown (turn off) the virtual machine

When you finished working on the virtual machine, you may turn it off. There are three types of teardown process: destroy, halt, and suspend (This document only explains destroy and suspend). Destroy removes all traces of the virtual machine from your system and free all the resources used. When you `vagrant up` later, it goes through all the provision process, which takes time. It's useful when you want to reset the virtual machine or reinstall prerequisite packages by going through the provisional steps. Run the command below _after you exited the virtual machine's shell_ (vagrant is installed on your system, not the virtual machine).

```
vagrant destroy
```

The second type of teardown process is suspend. It's similar to _sleep_ that preserves the current state of the virtual machine so that you can pick up where you left off. `vagrant up` will quickly restore the state of the virtual machine.

```
vagrant suspend
```

### 9. Create a new instance on a production server

Deploying a new instance of the app on an actual server is almost same as creating an instance on the virtual machine using Vagrant (Just make sure the server is running the same version of the OS as the box Vagrant is running). Follow the list below to create a new instance on a production server.

- `ssh` into the host. You'll need the *root* privilege.
- Create a directory under the root directory (/).
- Clone the repository with the new directory specified (see the section 2).
- Configure local settings for this instance on the server (see the section 3). The essential settings include:
  - Create `local_settings.py` with Django `SECRET_KEY` and `DATABASES`
  - Author content data to prepopulate. `api/management/commands` has `prepopulate.py` that reads `json` and `html` files and create Django objects in the database. This data will be used when the provision script runs `python3 manage.py prepopulate` below.
- Customize the code (including the model schema, view, and templates) if you need.
- Install dependencies following the provision script.
  - `deployment/provision_vagrant.sh` has a long shell script that you ran to spin up the virtual machine.
  - Create a copy of the file and modify `PROJECT_NAME` variable to point the right path of the local repository.
- Run the shell commands under *root* privilege.
  - This step will migrate the Django database and prepopulate the content using the dataset you authored above.
