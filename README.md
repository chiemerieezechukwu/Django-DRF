# Django-DRF

## Getting started
Clone this repository and add application configurations to a `.env` file in the root of the project. Check `.env.example` file in the root of this project for a complete list of fields to add
### Docker Compose
make sure you're at the root of the project then run
```
$ docker-compose up
```
It will perform database migrations and the api will be served by gunicorn on `http://localhost:8000`
### Populating the database
A python script exists to populate the database automatedly.
Make sure that the application is still running in the docker container then run the command below
```
$ python populate_db.py
```
It will add car entries to the database as well as assign multiple random ratings to each entry

### Running tests inside Docker
With the containers still running, exec into it with the bash command by running
```
$ docker exec -it {APP CONTAINER ID} bash
```
Run the command below to execute all test cases
```
$ python manage.py test
```

The Heroku deployment can be found at - http://django-drf-api.herokuapp.com/