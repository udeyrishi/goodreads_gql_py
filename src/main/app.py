#!/usr/bin/env python

import asyncio
from graphql.execution.executors.asyncio import AsyncioExecutor
from flask import Flask
from flask_graphql import GraphQLView
import os

API_KEY_ENV_VAR = 'GOODREADS_KEY'

if __name__ == '__main__':
    from schema import schema
    from data import AuthorXMLLoader
else:
    from main.schema import schema
    from main.data import AuthorXMLLoader

def create_app():
    if API_KEY_ENV_VAR not in os.environ:
        raise KeyError(f'`{API_KEY_ENV_VAR}` environment variable was not defined. Please get one from https://www.goodreads.com/api.')
    api_key = os.environ[API_KEY_ENV_VAR]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = Flask(__name__)
    app.add_url_rule(
        '/graphql', 
        view_func=GraphQLView.as_view(
            'graphql', 
            executor=AsyncioExecutor(loop=loop), 
            schema=schema, 
            graphiql=True, 
            get_context=lambda: {'author_loader': AuthorXMLLoader(api_key=api_key, loop=loop)}
        )
    )
    return app

if __name__ == "__main__":
    create_app().run()