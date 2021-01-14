from flask import Flask
from flask_restful import Resource, Api, abort

# set up app
app = Flask(__name__)
# wrap app in api
api = Api(app)

person_info = {
    "simon": {"age": 28, "location": "Swe"},
    "allan": {"age": 2, "location": "desert"}
}


# create new resource
class HelloWorld(Resource):
    def get(self, name):
        try:
            return person_info[name]
        except KeyError:
            abort(404)

            # return {"name": name,
            #         "age": age}
            # return {"data": "hello world"}


# add resource to api, and determine the route to resource ("/helloworld")
# api.add_resource(HelloWorld, "/helloworld")

# add resource with parameters
api.add_resource(HelloWorld, "/personinfo/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)

