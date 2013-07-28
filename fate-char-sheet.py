import os

from flask import Flask, render_template, redirect
from flask.ext.admin import Admin
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from flask.ext.restful import Resource, Api

from models import Character

# Create application
app = Flask(__name__)

# Create secret key so we can use sessions
app.config['SECRET_KEY'] = "dd76525c-f7c6-11e2-8440-5b0a54959281"
app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}

# Create models
connect(
    'fate-char-sheet',
    host=os.environ.get(
        'MONGOLAB_URI',
        'mongodb://localhost/fate-char-sheet'
    )
)
db = MongoEngine()
db.init_app(app)


@app.route('/')
def index():
    return redirect("/admin/")


class CharacterResource(Resource):
    def get(self, name):
        char = Character.objects.get_or_404(name=name).to_mongo()
        del char['_id']
        del char['_cls']
        del char['_types']
        return char

api = Api(app)
api.add_resource(CharacterResource, '/character/<string:name>')


class ReadOnlyView(ModelView):
    # Disable model creation
    name = "ro_view"
    can_edit = False
    can_create = False
    can_delete = False

admin = Admin(app, 'Fate Accelerated')
admin.add_view(
    ModelView(Character, endpoint="edit", name="Edit")
)
admin.add_view(
    ReadOnlyView(Character, endpoint="view", name="View"),
)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
