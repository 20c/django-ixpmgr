vegu's super basic dev instance


1. pip install django<3
2. pip install mysqlclient
3. pip install django_ixpmgr
4. pip install https://gitlab.com/ix-api/ix-api-schema/-/archive/develop/ix-api-schema-develop.zip
5. pip install django-rest-framework
5. edit ixpmgr/settings.py
  1. DATABASES.default: sqlite
  2. DATABSAES.ixpmanager: mysql
  3. DATABASE_ROUTERS: ["django_ixpmgr.routers.Router"]
6. python manage.py migrate --database=default
7. python manage.py runserver
