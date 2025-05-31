# Configuration

This project was made using python3.13, postgresql@14 and docker. Have does properly setup before doing anything.

In the .env file you will find the basic variables for connection with the porstgresql db, change it accourding to your configuration.

## First initialization

To first run the project run `docker-compose build` and than `docker-compose up`.
With the container running connect to the shell and run `python manage.py migrate` in the /app folder.
Also run `python manage.py createsuperuser` to configure your user.

## Importing the initial data

Still in the container shell you can run `python manage.py csv_traffic_data_importer traffic_speed.csv` to import the initial traffic data.

# Parte 1

You will be able to access the project documentation from http://localhost:8000/swagger/. In here you should be able to test all APIs immplemented.

# Parte 2

To run the test suite just run `python manage.py test` in the container shell.

# Parte 3

First import the new sensor data with `python manage.py csv_sensors_importer`.

To be able to add new sensor readings you will need to add a Bearer Token to the headers. This token can be registered in the Django-Admin page in the AuthToken model.

In the Swagger UI you can add your token to test the request by clicking in the Authorize button in the begging of the page (follow the format indicated in the prompt).