{% if False %}

# django-project-template

django-project-template is a Django 1.6+ project template, giving you a skeleton web application with some useful, but general, features. 

## Features

+ Separate dev, stag, and prod environments.
    + development, staging, and production settings
    + development and production (incl. staging) requirements
    + switch environments easily based on APP_ENV env var.
+ [django-storages](http://django-storages.readthedocs.org/en/latest/) static asset storage backend integration with S3.
+ Environment variable based database configuration
    + [dj-database-url](https://github.com/kennethreitz/dj-database-url) configures the database from the DATABASE_URL env var.
    + database passwords kept in environment variables and out of source.
    + integrates with Amazon RDS, Heroku DBs, and others easily.
+ Simple deployment to Heroku
    + HTTP redirection to HTTPS (except in development)
    + uses Heroku's free piggyback wildcard SSL.
+ Helps you construct organized web applications that follow the [12factor](http://12factor.net/) methodology.
+ Default project 404 and 500 error pages.

## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 2.7
+ Git >= 1.7
+ Virtualenv >= 1.9
+ Database (either one):
    + MySQL >= 5.6 ([guide]())
    + Postgres >= 9.2 ([guide]())
+ (recommended) Virtualenvwrapper >= 4.0

## Usage

Create a virtual environment in which to install Django and other pip packages. See [virtualenv](https://pypi.python.org/pypi/virtualenv) or [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/))

    workon djproj            # activate a Python virtual environment
    pip install django

If you have cloned [django-project-template](https://github.com/dghubble/django-project-template) with

    git clone https://github.com/dghubble/django-project-template

you can generate a new project with,

    django-admin.py startproject djproj [dest] \
    --template /path/to/django-project-template \
    -e py,rst,md,html \
    -n Procfile

Otherwise,

    django-admin.py startproject djproj [dest] \
    --template https://github.com/dghubble/django-project-template/archive/master.zip \
    -e py,rst,md,html \
    -n Procfile

A *djproj* **project directory** containing a README.md, a manage.py script, and a *djproj* Python **package directory** was created. Rename the outer (project) directory to anything you wish, but don't modify the inner (package) directory, its the package name for you Django application.

    mv djproj newname        # optionally rename project directory

If you specified a destination path after *djproj* in the startproject command, the project directory *contents* will be generated at that path location, not within a generated project directory.

Navigate into the project directory. You can run the commands in the rest of the instructions from there.

### Database Type

`django-project-template` encourages you to use MySQL or PostgreSQL in development, to match whichever database you plan to use in your staging and production environments. Depending on which database you've chosen, comment or delete the following items inside your generated Django application, depending on which databases you're not using:

+ README database `Prerequisites`
+ database specific requirements in requirements/development.txt, requirements/production.txt
+ *djproj*/settings/common.py DATABASES setting

In particular, ensure that the settings/common.py DATABASES default database url string has the correct scheme, username, password, port, and database name for your local database. It is generally ok to store local database authentication credentials in source, since your local database account is likely a throw-away account. However, if this is a concern, remove the 'default' keyword argument to `dj_database_url.config` entirely so the database used by the Django project is configured by the DATABASE_URL environment variable alone.

## Start Developing

You have successfully generated a Django application based on the `django-project-template`. You can now commit and distribute the initial version to other developers on your team if you wish. The README generated inside the application has been customized for your project. It documents local setup, workflows, and deployments.

## Contributing

Want a particular feature? Discovered a bug or problem? Open an [Issue](https://github.com/dghubble/django-project-template/issues) or send a [Pull Request](https://github.com/dghubble/django-project-template/pulls) and I'll get back to you.

{% endif %}
# {{project_name|title}} Project

## Overview

{{project_name}}, a Django web application ...

... initially generated with the [dghubble/django-project-template](https://github.com/dghubble/django-project-template).

## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 2.7
+ Git >= 1.7
+ Virtualenv >= 1.9
+ Database (either one):
    + MySQL >= 5.6 ([guide]())
    + Postgres >= 9.2 ([guide]())
+ (recommended) Virtualenvwrapper >= 4.0

Create a database user and a database {{project_name}}_dev to use for development. Ensure that the `default` DATABASES url string in {{project_name}}/settings/common.py corresponds to your database.

## Quickstart

Create a virtual environment in which to install Python pip packages. With [virtualenv](https://pypi.python.org/pypi/virtualenv),

    virtualenv venv            # create a virtualenv
    source venv/bin/activate   # activate the Python virtualenv 

or with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/),

    mkvirtualenv {{project_name}}   # create and activate environment
    workon {{project_name}}   # reactivate existing environment

Install development dependencies,

    pip install -r requirements/development.txt

Setup database tables,

    python manage.py syncdb   # create neccessary tables

Run the web application locally,

    python manage.py runserver # 127.0.0.1:8000

The standard Django DEBUG mode congrats page should be visible.


## Workflow


### Environments

Switch environments by changing the value of the APP_ENV environment variable.

The `development` or `dev` environment runs the Django application with DEBUG set to true on a small development server which auto-reloads changed files. Django trackbacks are shown instead of error pages. Django itself serves the static assets located inside your project and apps. The database you have created on your local machine is used

The `staging` or `stag` environment can be run both locally or deployed because it includes both in ALLOWED_HOSTS. If deployed, the staging deployment should be separate from the production deployment (e.g. different Heroku application). The staging environment uses production type deployed static assets and databases though the actual hosted assets use a different S3 bucket from production and the staging database should be separate from the production database. Authentication keys or credentials are kept in environment variables, not in source. The staging environment uses the production requirements 'requirements/production.txt' for enforced parity.

Typically, when moving from `development` to `staging`, first switch to the staging environment locally and run the project with manage.py's runserver to test whether interactions with production type static assets and databases works without issue (install production.txt requirements first!). Staging deployments should use production type webservers so that `staging` is identical to `production` except for the names of buckets, dbs, etc.

The `production` or `prod` environment is the environment in which your application should run in the real world. All authentication keys or credentials are kept in environment variables, not in source. The project should be served by a production quality webserver such as [gunicorn](http://gunicorn.org/). Static assets should be served from a a globally available file store (S3) or CDN. Production databases should be backed up and fortified. Production static asset stores and databases should be touched with extreme caution.


### Static Resources

In development, static assets are hosted at '<base_url>/static/' + namespacing appname + path to the asset within the 'myapp/static/myapp' directory. In your templates, include {% templatetag openblock %} load staticfiles {% templatetag closeblock %} at the top of the template and reference static assets like,

    <img src="{% templatetag openblock %} static 'appname/img/myimage.png' {% templatetag closeblock %}" alt="myimage">

This project uses the standard `django.contrib.staticfiles` app so in development, when the DEBUG setting is true, static assets are served automatically with runserver. 


### Deploying Static Resources

In staging and production environments, using a web process to serve static assets is not appropriate. Instead, `django-storages` adapters are used to upload collected static assets to Amazon S3 and to replace static template tags correctly.

First, create [S3 buckets](https://console.aws.amazon.com/s3) {{project_name}}-static-stag and {{project_name}}-static (set in {{project_name}}/settings/staging.py and {{project_name}}/settings/production.py) for static assets. Then create two [IAM](https://console.aws.amazon.com/iam/home) users {{project_name}}_stag and {{project_name}} with the Full S3 Access permission policy.

Be sure the APP_ENV, SECRET_KEY, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY environment variables are set in your environment.

Upload static files,

    python manage.py collectstatic  # when APP_ENV is staging or production

Then, in staging and production, the static assets uploaded to the staging and production buckets, respectively, will be referenced in your templates.

*Note: If a STATIC_ROOT directory was created in your project directory, your APP_ENV is set to development. Delete the STATIC_ROOT directory.*

### Adding Apps

Projects templated from django-project-template are designed so that reusable apps you include source code for can be placed adjacent to the project's package directory {{project_name}}. Add the (unprefixed) app names to {{project_name}}/settings.py INSTALLED_APPS. The `static` and `templates` directories of your included apps should use inner directories that match the name of the app for namespacing.

Start creating included source reusable Django apps with

    python manage.py startapp appname



## Deployment

Before you deploy, customize the ALLOWED_HOSTS in {{project_name}}/settings/staging.py and {{project_name}}/settings/production.py to match only your deployment domain.


### Heroku

Create Heroku app repo and add Git `staging` remote,

    heroku login             # if you haven't already
    heroku create --remote staging  # within project dir
    heroku create --remote production
    git remote -v            # expect: origin, staging, production

By default, Heroku would create a remote named 'heroku', but here the project becomes associated with two Heroku apps, one for `staging` and another for `production`. When git pushing, specify the correct remote and when using heroku commands use the `--remote remote-name` or `-r remote-name` options to specify the application to which deployments should go.

To tell the `heroku` command to default to `staging` for this project,

    git config heroku.remote staging

although you may prefer to require it be specified explicitly.

Continuing, the deployment instructions show a deployment to staging, but the production deployment procedure is analogous (add `-r production` after `heroku` commands)

Now rename your project on Heroku,

    heroku apps:rename {{project_name}}-stag -r staging
    heroku apps:rename {{project_name}} -r production
    # we prefer dashed names over underscores

Define the following environment variables for the Heroku application:

+ APP_ENV
+ SECRET_KEY
+ AWS_ACCESS_KEY_ID
+ AWS_SECRET_ACCESS_KEY

as follows,

    heroku config:set APP_ENV=staging -r staging
    heroku config:set SECRET_KEY='...' -r staging
    ...
    # check env vars are correct
    heroku config -r staging
    heroku config -r production

Turn on Heroku's `user-env-compile` feature so `django-storages` can read environment variables to determine how to collect and upload static assets.

    heroku labs:enable user-env-compile -r staging


#### Database Connection

##### MySQL

For MySQL, [setup]() your [Amazon RDS](https://console.aws.amazon.com/rds/home) instance. Create a user {{project_name}}_stag and database {{project_name}}_stag for staging. Also create user {{project_name}} and database {{project_name}} for production. Be sure to require [SSL encrypted](http://aws.amazon.com/rds/faqs/#54) connections. Alternately, use another [supported](https://addons.heroku.com/?q=mysql) MySQL provider.

    heroku addons:add amazon_rds --url=mysql2://user:pass@rdshost:3306/dbname -r staging
    # check DATABASE_URL is correct
    heroku config -r staging 
    # remove Postgresql addon which Heroku may add automatically
    heroku addons:remove heroku-postgresql:dev          

For conventience, add you MYSQL_HOST to an environment variable so you can connect to your database directly if needed.

    export MYSQL_HOST=dbidentifier.ch34mweifni.region-rds.amazonaws.com
    mysql -h $MYSQL_HOST -u master_user -p

##### PostgreSQL

For PostgreSQL, ...


#### Pushing

Push your application to Heroku,

    git push staging master:master 

One-off commands allow setting up database tables and uploading static assets as you would do locally. Heroku's `user-env-compile` lab should allow `django-storages` to automatically collect and upload static assets so the first command may not be needed.

    heroku run python manage.py collectstatic -r staging
    heroku run python manage.py syncdb -r staging

Check up on your Heroku application,

    heroku open              # open application in browser
    heroku ps                # see web/worker counts and stats

#### Troubleshooting

    heroku ps
    heroku logs              # check Heroku logs
    heroku config            # check your Heroku env vars
    heroku restart           # restart dynos


### EC2













