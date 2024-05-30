from flask import Flask, request
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app, db)

api = Api(app, doc="/docs")


@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        return {"message": "Hello World"}


recipe_model = api.model(
    "Recipe",
    {
        "id": fields.Integer(readonly=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
    },
)


@api.route("/recipes")
class RecipesResource(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
    def post(self):
        """Create a new recipe"""
        data = request.get_json()
        new_recipe = Recipe(
            title=data.get("title"), description=data.get("description")
        )
        new_recipe.save()
        return new_recipe, 201


@api.route("/recipe/<int:recipe_id>")
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    def get(self, recipe_id):
        """Get a recipe by ID"""
        recipe = Recipe.query.get_or_404(recipe_id)
        return recipe

    @api.marshal_with(recipe_model)
    def put(self, recipe_id):
        """Update a recipe by ID"""
        recipe_to_update = Recipe.query.get_or_404(recipe_id)
        data = request.get_json()
        recipe_to_update.update(data.get("title"), data.get("description"))
        return recipe_to_update, 200

    @api.marshal_with(recipe_model)
    def delete(self, recipe_id):
        """Delete a recipe by ID"""
        recipe_to_delete = Recipe.query.get_or_404(recipe_id)
        recipe_to_delete.delete()
        return recipe_to_delete, 200


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Recipe": Recipe}


if __name__ == "__main__":
    app.run()
