from mongoengine import *
#from celerify import Celerify

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

#    @classmethod
#    def post_save(cls, sender, document, **kwargs):
#        Celerify(document.path, document.name, document.id)

class Task(Document):
    created_on = DateTimeField()
    function = ReferenceField(Function, required=True)
    argNames = ListField(StringField())
    argVals = ListField(DynamicField())
    # completed is a read-only field from Client perspective
    completed = BooleanField(default=False)
    retVal = ListField()
