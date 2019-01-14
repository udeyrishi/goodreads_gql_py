#!/usr/bin/env python
# Copyright (c) 2019 Udey Rishi. All rights reserved.

import asyncio
from graphql.execution.executors.asyncio import AsyncioExecutor
from flask import Flask
from flask_graphql import GraphQLView
import logging
import os

API_KEY_ENV_VAR = 'GOODREADS_KEY'

if __name__ == '__main__':
    import argparse
    from goodreads import GoodReadsXMLApi
    from data import data_loaded
    from schema import schema
else:
    from main.data import data_loaded
    from main.goodreads import GoodReadsXMLApi
    from main.schema import schema

def create_app(api_key=None):
    logging.basicConfig(level=logging.DEBUG)

    if api_key == None and API_KEY_ENV_VAR in os.environ:
        logging.getLogger().debug(f'Picked GoodReads API key from environment variable `{API_KEY_ENV_VAR}`.')
        api_key = os.environ[API_KEY_ENV_VAR]

    if api_key == None:
        raise KeyError(f'The GoodReads API key should either be supplied via command line param `-k` or via the environment variable `{API_KEY_ENV_VAR}`. Please get one from https://www.goodreads.com/api.')
    
    api = GoodReadsXMLApi(api_key)

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
            get_context=lambda: {
                'author_loader': data_loaded(fn=api.get_author, loop=loop),
                'book_loader': data_loaded(fn=api.get_book, loop=loop)
            }
        )
    )
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A sample GraphQL API wrapper for the GoodReads REST API.')
    parser.add_argument('-k', '--key', help='The GoodReads API key.')
    args = parser.parse_args()
    create_app(api_key=args.key).run()