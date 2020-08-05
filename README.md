# person-app
## Installation
Make sure you have python3, pip, and sqlite3. From the home directory of the repo, run

```
$ pip install -r requirements.txt
```
Set up the database using
```
$ flask db init
$ flask db upgrade
```

## Development
```
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

## Adding dependencies
After adding new dependencies via `pip install`, run this command to update the requirements

```
$ pip freeze > requirements.txt
```

Commit the file to source control.

## Testing
To test, run
```
$ python -m unittest tests.test_person
```

## Running database migrations
```
$ flask db migrate -m "<migration_name>"
$ flask db upgrade
```
Commit the migration files to source control.
