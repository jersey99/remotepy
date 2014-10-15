from mongoengine import *

class Function(Document):
    created_on = DateTimeField()
    path = StringField(required=True)
    name = StringField(required=True)
    args = ListField(StringField())
    defaultArgVals = ListField(DynamicField())
    minRange = ListField(DynamicField())
    maxRange = ListField(DynamicField())
    description = StringField()

class Task(Document):
    created_on = DateTimeField()
    function = ReferenceField(Function, required=True)
    argVals = ListField()
    # completed is a read-only field from Client perspective
    completed = BooleanField(default=False)
    retVal = ListField()
