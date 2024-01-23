## Post Test Python Framework (Flask & FastAPI) - To Do :
1. Create Notes Migration :white_check_mark:
2. Create Model & CRUD Endpoint For Notes :white_check_mark:
3. [API Documentation](https://github.com/u1-btj/btj-academy-python-flask-yuma?tab=readme-ov-file#api-documentation) :white_check_mark:

# Flask + SQLAlchemy + Alembic Boilerplate

This is a sample project of Async Web API with Flask + SQLAlchemy 2.0 + Alembic.
It includes asynchronous DB access using asyncpg and test code.

See [reference](https://github.com/rhoboro/async-fastapi-sqlalchemy/tree/main).

Other References
- [Flask Docs](https://flask.palletsprojects.com/en/3.0.x/)
- [Gunicorn](https://gunicorn.org/)
- [SQL Alchemy](https://docs.sqlalchemy.org/en/20/orm/index.html)
- [SQL Alchemy - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# Setup

## Install

```shell
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

## Setup a database and create tables

```shell
(venv) $ docker run -d --name db \
  -e POSTGRES_PASSWORD=root \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgdata:/var/lib/postgresql/data/pgdata \
  -p 5432:5432 \
  postgres:15.2-alpine

# Cleanup database
# $ docker stop db
# $ docker rm db
# $ docker volume rm pgdata

(venv) $ APP_CONFIG_FILE=local python3 app/main.py migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> a8483365f505, initial_empty
INFO  [alembic.runtime.migration] Running upgrade a8483365f505 -> 24104b6e1e0c, add_tables
```

# Run

```shell
(venv) $ APP_CONFIG_FILE=local python3 app/main.py api
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000 (92311)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 92315
```

# Test

```shell
(venv) $ python3 -m pytest
```

# Create Migration

```shell
(venv) $ cd app/migrations
(venv) alembic revision -m "<name_of_migration_file>"
```

# API Documentation
For full and detailed API Documentation, check on this [Postman Documentation](https://documenter.getpostman.com/view/31773270/2s9YymJ5Lo)  

List of Endpoint for Notes `/api/v1/notes` :
- POST `/api/v1/notes` -> Create new note, contain title and content on request body. Value for created_by will be set into user_id from JWT Token
- PUT `/api/v1/notes/[id]` -> Update note based on note id, contain title and content on request body. Only user who created the note can update it.
- DELETE `/api/v1/notes/[id]` -> Delete note based on note id. Only user who created the note can delete it.
- GET `/api/v1/notes/[id]` -> Get specific note id. Only user who created the note can retrieved it.
- GET `/api/v1/notes` -> Get all notes with pagination, contain params : item_per_page, page, filter_by_user_id, included_deleted_note. If filter_by_user_id = True, it will only get all notes from specific user based on user_id from JWT Token, otherwise it will get all notes from all user (Default Value = True). If included_deleted_note = True, responses will also contain deleted note, otherwise deleted note will be excluded (Default Value = False).
