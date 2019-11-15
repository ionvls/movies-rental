# Movies Rental API

A simple api where a user can browse movies, register and rent them.

## Running the app

Preferably, first create a virtualenv and activate it, perhaps with the following command:

```
virtualenv -p python3 venv
source venv/bin/activate
```

You can use makefile to set everything up by running:
```
make clean
make install
```
Or manually by:

running

```
pip install -r requirements.txt
```

to get the dependencies.

Create the databases *requires to configure the `.env` file

```
create_db movies_rental_api
create_db movies_rental_api_test
```


Next, seed the database with some test data

```
python manage.py seed_db
```

Type "Y" to accept the message (which is just there to prevent you accidentally deleting things -- it's just a local SQLite database)

Finally run the app with

```
python run.py
```

Navigate to the posted URL in your terminal to be greeted with Swagger, where you can test out the API.

## Running tests

To run the test suite, simply run from the root directory like so

```
pytest
```
or by 
```
python manage.py test
```

