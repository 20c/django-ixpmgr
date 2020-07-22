vegu's super basic dev instance, improved on

```
export IXPMANAGER_DATABASE_PASSWORD=$PASSWORD
export IXPMANAGER_DATABASE_HOST=$HOST
pipenv shell
cd ixpmgr
python manage.py migrate --database=default
python manage.py runserver
```

Enjoy at:

http://localhost:8080/accounts/?format=json
http://localhost:8080/facilities/?format=json
