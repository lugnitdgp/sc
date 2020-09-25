# Screencast

![Python Versions](https://img.shields.io/pypi/pyversions/django.svg?style=flat) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Kaustuv942/sc)
![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg) ![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)


A quiz app ready for production.

## Build Setup

```bash
#creating virtual env
mkdir project
cd project
virtualenv venv
source venv/bin/activate

#clone the directory
git clone https://github.com/Kaustuv942/sc.git

#change directory
cd sc

#Install dependencies
pip install -r requirements.txt
```
#### Initialize postgres

[Click here for more detail ](https://stackoverflow.com/questions/1471571/how-to-configure-postgresql-for-the-first-time)
```bash
#Make migrations
python manage.py makemigrations
python manage.py migrate

#Run server
python manage.py runserver
```
