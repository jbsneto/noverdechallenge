# How to start the project

1. Create virtualenv
> virtualenv noverdechallenge

2. Activate virtualenv
> cd noverdechallenge
> . bin/activate

3. Clone repository
> git clone git@github.com:jbsneto/noverdechallenge.git

4. Enter repository
> cd noverdechallenge

5. Install libs
> pip install -r requirements.txt

6. Run migrate
> python manage.py migrate

7. Run a RabbitMQ server and insert IP
> setting.CELERY_BROKER_URL

8. Run Celery server
> celery -A noverdechallenge worker --loglevel=info

9. Run testing server
> python manage.py runserver

