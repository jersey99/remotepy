from tastypie_mongoengine import resources, fields
#from models import Function, Task, Arg
from netlambda import models
from tastypie.validation import Validation

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

#class TaskValidation(Validation):

class TaskResource(resources.MongoEngineResource):
#    function = fields.ReferenceField(to="netlambda.resources.FunctionResource", attribute="function", full=True)
    class Meta:
        object_class = models.Task
        resource_name = 't'
        allowed_methods = ('get', 'post')
#        validation = TaskValidation()
        #authorization = authorization.Authorization()
    def is_valid(self, bundle, request=None):
        print "hiya"
        if not bundle.data:
            return {'__all__': 'Not quite what I had in mind.'}
        errors = {}
        if 'function' in bundle.data and 'id' in bundle.data['function']:
            func_key = bundle.data['function']['id']
            F = models.Function.objects(id=func_key).first()
            if not F: return errors.update({"function": "Doesn't exist"})
            if ((not 'argNames' in bundle.data) or (not 'argVals' in bundle.data) or 
                (len(bundle.data['argNames']) != len(bundle.data['argVals']))):
                return errors.update({"function": "Number of argument Names and Values provided don't match"})
            argVals = bundle.data['argVals']
            argNames = bundle.data['argNames']
            for arg in F.args:
                if arg.name in argNames:
                    i = argNames.index(arg.name)
                    if arg.type == 'int':
                        argVals[i] = int(argVals[i])
                    elif arg.type == 'float':
                        argVals[i] = float(argVals[i])
                    if argVals[i] > arg.max or argVals[i] < arg.min:
                        return errors.update({arg.name:"Out of Bounds"})
            print "Model Validated!"
        print errors
        return errors
    def obj_create(self, bundle, **kwargs):
        errors = self.is_valid(bundle)
        if errors:
            from tastypie.exceptions import ImmediateHttpResponse
            raise ImmediateHttpResponse(response=self.error_response(bundle.request, errors))
        func_key = bundle.data['function']['id']
        F = models.Function.objects(id=func_key).first()
        argVals = bundle.data['argVals']
        argNames = bundle.data['argNames']
        valid_names = []
        valid_values = []
        for arg in F.args:
            valid_names.append(arg.name)
            if arg.name in argNames:
                i = argNames.index(arg.name)
                if arg.type == 'int':
                    valid_values.append(int(argVals[i]))
                elif arg.type == 'float':
                    valid_values.append(float(argVals[i]))
            else:
                valid_values.append(arg.default)
        bundle.data['argNames'] = valid_names
        bundle.data['argVals'] = valid_values
        bundle.data['function'] = F
        print "bundle.data", bundle.data
        # TODO: If task was already run, retrieve the result of the task instead
        from webserver.settings import celery_conn
        if F.path:
            fname = F.path.split('/')
            fname = fname[-1]
            fname = fname.split('.py')[0]
            result = celery_conn.send_task(fname+'.'+F.name, valid_values)
            bundle.data['celery_uuid'] = result.id
            bundle.obj = models.Task(**bundle.data)
            bundle.obj.save()
            return bundle
