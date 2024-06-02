from flask_restx import Namespace, Resource

hello_ns = Namespace("hello", description="Hello related operations")


@hello_ns.route("/")
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello, World!"}
