# Flask Application

Web applications frequently require processing incoming request data from users. This payload can be in the shape of query strings, form data, and JSON objects. Flask, like any other web framework, allows you to access the request data.

## Installation

To get started with the application you need to complete following steps:

- Install Flask:

```shell
$ pipenv install Flask
```

The pipenv command will create a virtualenv for this project, a Pipfile, install flask, and a Pipfile.lock.

- To activate the project’s virtualenv, run the following command:

```shell
$ pipenv shell
```

- Next, create `.env` file in root directory of the project and add there `SECRET_KEY` and `DB_URI` variables:

```
SECRET_KEY=your-secret-key
DB_URI=your-database-uri
```

- Create tables in your database:

```sql
CREATE TABLE users(
	id INTEGER PRIMARY KEY,
	login VARCHAR,
	username VARCHAR,
	password VARCHAR,
    	token_required VARCHAR
)
```

- Run application:

```shell
$ python3 src/webserver/app.py
```

## Usage

This application have two routes:

- `[@app.route('/login')`
    

- `@app.route('/protected')`
    


## Examples

Here is the example of usage:

```shell
$ curl 'http://localhost:5000/login'

[
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoidXNlciIsImV4cCI6MTYzNTM1ODkxMn0.T1ehzqwaznJ5b35AG1HzU6Eh7lcEX3N1aSTpFHLp2xc"
  }
]
```
