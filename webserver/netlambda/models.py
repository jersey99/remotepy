from mongoengine import *
#from celerify import Celerify

class Arg(EmbeddedDocument):
    name = StringField(required=True)
    default = DynamicField()
    min = DynamicField()
    max = DynamicField()
    type = StringField(required=True)
    meta_type = StringField()
    desc_list = ListField(StringField(required=True))

class Function(Document):
    created_on = DateTimeField()
    path = StringField(required=True)
    name = StringField(required=True)
    args = ListField(EmbeddedDocumentField(Arg))
    description = StringField()
    package_name = StringField()

class Package(Document):
    name = StringField(required=True)
    path = StringField(required=True)
    functions = ListField(ReferenceField(Function, required=True))

class Task(Document):
    created_on = DateTimeField()
    function = ReferenceField(Function, required=True)
    name = StringField()
    celery_uuid = StringField()
    argNames = ListField(StringField())
    argVals = ListField(DynamicField())
    # completed is a read-only field from Client perspective
    completed = BooleanField(default=False)
    retVal = ListField()
