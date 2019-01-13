#!/usr/bin/env python

from graphql.execution.executors.asyncio import AsyncioExecutor
from flask import Flask
from flask_graphql import GraphQLView
from schema import schema

if __name__ == '__main__':
    app = Flask(__name__)
    app.debug = True
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', executor=AsyncioExecutor(), schema=schema, graphiql=True))
    app.run()