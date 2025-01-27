#  SayalSanjesh

### Project database

* postgresql

# Getting Started

First clone the repository from Github :

    $ git clone https://github.com/mahziarAhmadian/SayalSanjesh.git
    $ cd {{ SayalSanjesh }}

Activate the virtualenv for your project.

Install project dependencies:

    $ pip install -r requirements.txt


Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate


You can now run the development server:

    $ python manage.py runserver