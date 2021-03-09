from flask import Flask
from flask import render_template
from flask_restful import Resource, Api, abort

# set up app
from server.controller import controller

app = Flask(__name__)
# wrap app in api
api = Api(app)


class Login(Resource):
    def get(self, username, password):
        try:
            return controller.login(username, password)
        except controller.LoginException as e:
            # tuple (response, status)
            return ('Could not log in user', 401)


api.add_resource(Login, "/login/<string:username>/<string:password>")


if __name__ == '__main__':
    # app.run(debug=True, port=8080, ssl_context='adhoc')  # over https for test
    app.run(debug=True, port=8080)  # over http

