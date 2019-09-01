# Flask ML boilerplate
A boilerplate project structure for a Flask-based web app interface for running
machine learning models using Celery and RabbitMQ.

## Requirements
- Python 3.6 or newer
- MySQL 8.X


## Usage

### Setup
First clone the repository and `cd` into the project root. Create a virtual environment to setup the project.

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=run.py
```

Configure the `.env` file with the database URI and ensure the MySQL server is running.

```shell
$ flask db init
$ flask db migrate # Generates migration scripts in migrations/
$ flask db upgrade # Performs the database migration
```

### Running server for development
To run the server for development, use the `flask` commands.

```shell
$ flask run
```



