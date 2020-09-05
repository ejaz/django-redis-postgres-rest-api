To install postgresql and to view data:
- brew install postgresql
- brew services start postgresql
- brew cask install pgadmin4

To install Redis Server:
- brew install redis
- brew services start redis

Commands to run before start(python3 manage.py runserver):
- brew install python 3
- pip3 install djangorestframework
- pip3 install django-cors-headers
- pip3 install psycopg2-binary
- pip3 install redis
- python3 manage.py makemigrations
- python3 manage.py migrate

For database edit the settings.py > Database-section
- Add your database settings into it e.g. name, user, password and port
- You need to start redis server as well to store the price and stock while name will be stored in postgresql.

Endpoints:
To save a new product:

- http://localhost:8080/api/product   [POST]:
    {
    "name": "test41",
    "price": 3003,
    "stock": 44
    }

To get all products:
- http://localhost:8080/api/product   [GET]

To get the specific product with ID:
- http://localhost:8080/api/product/4   [GET]