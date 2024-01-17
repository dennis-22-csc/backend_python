from fastapi import FastAPI
from strawberry.asgi import GraphQL
from query import Query
import strawberry

schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)
app = FastAPI()

app.add_route("/graphql", graphql_app)

