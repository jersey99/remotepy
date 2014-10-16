from tastypie_mongoengine import resources, fields
#from models import Function, Task, Arg
from netlambda import models

class ArgResource (resources.MongoEngineResource):
    class Meta:
        object_class = models.Arg

class FunctionResource(resources.MongoEngineResource):
    args = fields.EmbeddedListField(of='netlambda.resources.ArgResource', attribute='args', full=True, null=True)
    class Meta:
        object_class = models.Function
        allowed_methods = ('get')
        resource_name = 'func'
        #authorization = authorization.Authorization()

class TaskResource(resources.MongoEngineResource):
    class Meta:
        queryset = models.Task.objects.all()
        allowed_methods = ('get')
        #authorization = authorization.Authorization()
