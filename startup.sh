pip install -r requirements/default.txt
python manage.py makemigrations fool
python manage.py migrate --fake-initial fool
python manage.py import_content
python manage.py runserver 8000