from flask_restx import Namespace, Resource
from flask import Flask, jsonify

hello_ns = Namespace("hello", description="Hello related operations")


@hello_ns.route("/")
class HelloWorld(Resource):
    def get(self):
        return jsonify({"message": "Hello, World!"})
