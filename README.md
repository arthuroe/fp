[![Build Status](https://travis-ci.org/arthuroe/fp.svg?branch=develop)](https://travis-ci.org/arthuroe/fp)

### Fantasy Rugby

This application enables users to create fantasy rugby teams and leagues. Users are therefore able to compete amongst themselves and earn points depending on how players selected perform during the games.

#### Development setup

- Clone this repo and navigate into the project's directory

  - `$ git clone https://github.com/arthuroe/fp && cd fp`

- Create a python3 virtual environment for the project and activate it.

  - To install the virtual environment wrapper `mkvirtualenv` you can follow [this](https://jamie.curle.io/installing-pip-virtualenv-and-virtualenvwrapper-on-os-x).
  - `$ mkvirtualenv --py=python3 fp`

- Setup postgresql database

  - `$ create a database`
  - `$ create user`

- Run Migrations for the database

  - `$ python manage.py db init`
  - `$ python manage.py db migrate`
  - `$ python manage.py db upgrade`

- Install the project's requirements

  - `$ pip install requiremenst.txt`

- Copy `.env.sample` into `.env` in the fp which is the base folder of the project. You should adjust it according to your own local settings.

- Export the environment variables in the .env

  - `$ export $(cat .env)`

- Run tests on the code in the project folder with

  - `$ pytest`

- Run the application
  - `$ python run.py`
