# Flask ML boilerplate
A boilerplate project structure for a Flask-based web app interface for running
machine learning models using Celery and RabbitMQ.

## Requirements
- Python 3.6 or newer
- MySQL 8.X
- RabbitMQ
- Redis


## Usage

### Setup
First clone the repository and `cd` into the project root. Create a virtual environment to setup the project.

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

The queuing of machine learning jobs are handled by Celery, using RabbitMQ as the message broker and Redis to store the jobs' results. (Note: the Redis store merely stores the state of the jobs, but the actual ouput of the job should be saved to disk or in a database, with the path to this information stored in Redis). Thus, to use Celery, first install RabbitMQ and Redis.


Configure the `.env` file with the MySQL database URI and ensure the MySQL server is running.
You can now run the database migrations.

```shell
$ flask db init
$ flask db migrate # Generates migration scripts in migrations/
$ flask db upgrade # Performs the database migration
```

### Running server for development
To run the server for development, use the `flask` commands.

```shell
$ source venv/bin/activate
$ flask run
```

To launch the Celery worker:

```shell
$ celery worker -A app.celery --loglevel=info
```



