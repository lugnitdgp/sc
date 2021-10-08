<p align="center">
  <a href="https://screencast.anweshadan.vercel.app/">
    <img alt="logo" src="screencastlogo.png" width="150" />
  </a>
</p>
<h1 align="center">
  SCREENCAST Backend
</h1>


[![Build Status](https://travis-ci.com/Kaustuv942/sc.svg?branch=withoutdockerdeploy)](https://travis-ci.com/Kaustuv942/sc) ![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Kaustuv942/sc) ![Website](https://img.shields.io/website?url=https%3A%2F%2Fscapi.trennds.com%2Fapi%2F) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Build Setup

```bash

#clone the directory
git clone https://github.com/Kaustuv942/sc.git

```
#### Initialize postgres

[Click here for more detail ](https://stackoverflow.com/questions/1471571/how-to-configure-postgresql-for-the-first-time)
```bash
#Run script
cd scripts && chmod +x build.sh &&  ./build.sh 
```
## Docker Build

```bash 
sudo docker-compose up -d --build
sudo docker exec -it [web_container_name] python manage.py createsuperuser
```
#### Stopping the container

``` bash
sudo docker-compose stop
```

#### removing the volumes and the container

```bash
sudo docker-compose down -v
```

