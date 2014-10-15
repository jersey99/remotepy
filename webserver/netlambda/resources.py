from tastypie_mongoengine import resources
from models import Function, Task

class FunctionResource(resources.MongoEngineResource):
    class Meta:
        queryset = Function.objects.all()
        allowed_methods = ('get')
        resource_name = 'func'
        #authorization = authorization.Authorization()

class TaskResource(resources.MongoEngineResource):
    class Meta:
        queryset = Task.objects.all()
        allowed_methods = ('create', 'post', 'get')
        #authorization = authorization.Authorization()
