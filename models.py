from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class Character(db.Document):
    name = db.StringField(max_length=60)
    description = db.StringField()
    high_concept = db.StringField(max_length=60)
    trouble = db.StringField(max_length=60)
    aspects = db.ListField(db.StringField(max_length=20))
    stunts = db.ListField(db.StringField(max_length=20))
    careful = db.IntField(min_value=0, max_value=3)
    clever = db.IntField(min_value=0, max_value=3)
    flashy = db.IntField(min_value=0, max_value=3)
    forceful = db.IntField(min_value=0, max_value=3)
    quick = db.IntField(min_value=0, max_value=3)
    sneaky = db.IntField(min_value=0, max_value=3)
