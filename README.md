<p>
  <a herf="http://www.djangoproject.com/" target="_blank" alt="Django Official Website">
    <img src="https://static.djangoproject.com/img/logo-django.42234b631760.svg" style="width: 320; background: #0C4B33" />
  </a>
</p>

# `Guide`

Initial Project
---
> ### 1. Install Virtual Environment
> Install venv under root directory.
> ```sh
> python -m venv venv
> ```
> ### 2. Activate Virtual Environment
> Open CLI and execute
> ```sh
> venv\Scripts\activate
> ```
> ### 3. Install packages
> The packages should be installed
> - django
> - djangorestframework
> - mysqlclient
> - python-decouple
> ```sh
> pip install <package_1> <package_2> ...
> ```
> ### 4. Create Environment File
> Create .env file under ./djangoApiDemo
> Add the following parameters in .env file and give each value
> - SECRET_KEY
> - DEBUG
> - DB_HOST
> - DB_PORT
> - DB_NAME
> - MySQL_USER
> - MySQL_PASSWORD
> For example:
> ```sh
> SECRET_KEY = secret_key
> DEBUG = True
> 
> DB_HOST = localhost
> DB_PORT = 3306
> DB_NAME = demodb
> MySQL_USER = user
> MySQL_PASSWORD = password
> ```
> ### 5. Run Site
> #### `Notice that`
> - Be sure that the terminal's current directory is \Django\djangoApiDemo.
> - Be sure you have been install MySQL server and the corresponding MySQL schema has been created.
> ```sh
> python manage.py runserver
> ```
