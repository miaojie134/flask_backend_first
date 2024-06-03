from flask_restx import Resource, fields, Namespace
from models import User
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

auth_ns = Namespace("auth", description="Authentication related operations")


signup_model = auth_ns.model(
    "SignUp",
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

login_model = auth_ns.model(
    "Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

refresh_model = auth_ns.model(
    "Refresh",
    {
        "refresh_token": fields.String(required=True),
    },
)


@auth_ns.route("/signup")
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        """Sign up a new user"""
        data = request.get_json()
        username = data.get("username")
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return make_response(jsonify({"message": "User already exists."}), 400)
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password")),
        )
        new_user.save()
        return make_response(jsonify({"message": "User created successfully."}), 201)


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Log in an existing user"""
        username = request.get_json().get("username")
        password = request.get_json().get("password")

        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return make_response(
                jsonify({"access_token": access_token, "refresh_token": refresh_token}),
                200,
            )

        return make_response(jsonify({"message": "Invalid credentials"}), 401)


@auth_ns.route("/refresh")
class Refresh(Resource):
    # @auth_ns.expect(refresh_model)
    @jwt_required(refresh=True)
    def post(self):
        """Refresh access token"""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return make_response(
            jsonify({"access_token": access_token}),
            200,
        )
