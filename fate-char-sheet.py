import os

from flask import Flask, render_template
from flask.ext import admin
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


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Fate Accelerated')

    # Add views
    admin.add_view(ModelView(Character))

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
