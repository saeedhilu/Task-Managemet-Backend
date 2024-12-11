
echo "Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

echo "Running app1 management commands"
python manage.py runserver 0.0.0.0:8000

exec "$@"