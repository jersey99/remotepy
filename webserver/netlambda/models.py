from mongoengine import *

class Arg(EmbeddedDocument):
    name = StringField(required=True)
    default = DynamicField()
    min = DynamicField()
    max = DynamicField()
    type = StringField(required=True)

class Function(Document):
    created_on = DateTimeField()
    path = StringField(required=True)
    name = StringField(required=True)
    args = ListField(EmbeddedDocumentField(Arg))
    description = StringField()

class Task(Document):
    created_on = DateTimeField()
    function = ReferenceField(Function, required=True)
    argVals = ListField()
    # completed is a read-only field from Client perspective
    completed = BooleanField(default=False)
    retVal = ListField()
