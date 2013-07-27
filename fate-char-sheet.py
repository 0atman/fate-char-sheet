import os

from flask import Flask, render_template
from flask.ext.admin import Admin, AdminIndexView, expose
from flask.ext.admin.contrib.mongoengine import ModelView
from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from flask.ext.restful import Resource, Api

from models import Character

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}

# Create models
connect(
    'flask-basic',
    host=os.environ.get(
        'MONGOLAB_URI',
        'mongodb://localhost/flask-basic'
    )
)
db = MongoEngine()
db.init_app(app)


# Flask views
@app.route('/')
def index():
    return render_template('index.html', character="test")


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


class FateIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return 1


if __name__ == '__main__':
    # Create admin
    admin = Admin(
        app,
        'Fate Accelerated',
        index_view=AdminIndexView()
    )
    # Add views
    admin.add_view(ModelView(Character))
    admin.add_view(
        ReadOnlyView(Character, endpoint="view", name="View"),
    )

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
