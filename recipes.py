from flask import request
from flask_restx import Namespace, Resource, fields
from models import Recipe
from flask_jwt_extended import jwt_required

recipe_ns = Namespace("recipe", description="Recipe related operations")


recipe_model = recipe_ns.model(
    "Recipe",
    {
        "id": fields.Integer(readonly=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
    },
)


@recipe_ns.route("/")
class RecipesResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    @jwt_required()
    def post(self):
        """Create a new recipe"""
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get("title"), description=data.get("description")
        )
        new_recipe.save()
        return new_recipe, 201


@recipe_ns.route("/<int:recipe_id>")
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    def get(self, recipe_id):
        """Get a recipe by ID"""
        recipe = Recipe.query.get_or_404(recipe_id)
        return recipe

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def put(self, recipe_id):
        """Update a recipe by ID"""
        recipe_to_update = Recipe.query.get_or_404(recipe_id)
        data = request.get_json()
        recipe_to_update.update(data.get("title"), data.get("description"))
        return recipe_to_update, 200

    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, recipe_id):
        """Delete a recipe by ID"""
        recipe_to_delete = Recipe.query.get_or_404(recipe_id)
        recipe_to_delete.delete()
        return recipe_to_delete, 200
