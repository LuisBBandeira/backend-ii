from flask import Flask
from flask_graphql import GraphQLView
import graphene


user_data = {"name": "Default Name"}


class User(graphene.ObjectType):
    name = graphene.String()

class Query(graphene.ObjectType):
    user_name = graphene.Field(User)

    def resolve_user_name(self, info):
        return User(name=user_data["name"])

class UpdateUserName(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    user_name = graphene.Field(User)

    def mutate(self, info, name):
        user_data["name"] = name
        return UpdateUserName(user_name=User(name=name))

class Mutation(graphene.ObjectType):
    update_user_name = UpdateUserName.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)
