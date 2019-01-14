## graphql\_goodreads\_py

A simple Python GraphQL playground server that wraps some of the endpoints of the [GoodReads REST API](https://www.goodreads.com/api).

Uses [Flask](http://flask.pocoo.org/) and [Graphene](https://graphene-python.org/). Almost a Python port of the [node version by mpj](https://github.com/mpj/fff-graphql-goodreads).

### Running

```sh
$ pipenv install 
$ pipenv shell
$ export GOODREADS_KEY=<your goodreads api key>
$ export FLASK_APP=src/main/app.py
$ flask run
```

You can then either check out the [GraphiQL](http://localhost:5000/graphql) webpage, or use cURL:

```sh
$ curl -X POST -H "Content-Type: application/json" --data '{"query": "{ author(id:3706) { name } }"}' localhost:5000/graphql
{"data":{"author":{"name":"George Orwell"}}}
```
