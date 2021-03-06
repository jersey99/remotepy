import json
from tastypie_mongoengine import resources, fields
from netlambda import models
from tastypie.validation import Validation


class ArgResource (resources.MongoEngineResource):
    class Meta:
        object_class = models.Arg


class FunctionResource(resources.MongoEngineResource):
    args = fields.EmbeddedListField(of='netlambda.resources.ArgResource',
                                    attribute='args', full=True, null=True)

    class Meta:
        object_class = models.Function
        allowed_methods = ('get')
        resource_name = 'func'
        #authorization = authorization.Authorization()


class PackageResource (resources.MongoEngineResource):
    functions = fields.ReferencedListField(of='netlambda.resources.FunctionResource',
                                           attribute='functions',
                                           full=True, null=True)

    class Meta:
        object_class = models.Package
        allowed_methods = ('get')
        resource_name = 'pack'


class TaskResource(resources.MongoEngineResource):
    function = fields.ReferenceField(to="netlambda.resources.FunctionResource",
                                     attribute="function", full=True)

    class Meta:
        object_class = models.Task
        resource_name = 't'
        allowed_methods = ('get', 'post')
        always_return_data = True
        #authorization = authorization.Authorization()

    def obj_get(self, bundle, **kwargs):
        t = models.Task.objects(id=kwargs['pk']).first()
        print("t", t, kwargs['pk'], t.argVals, t.completed)
        if t.completed: return t
        from celery.result import AsyncResult
        res = AsyncResult(t.celery_uuid)
        if res.ready():
            t.completed = True
            t.retVal = [res.get()]
            t.save()
        return t

    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Not quite what I had in mind.'}
        errors = {}
        if 'function' in bundle.data and 'id' in bundle.data['function']:
            func_key = bundle.data['function']['id']
            F = models.Function.objects(id=func_key).first()
            if not F: return errors.update({"function": "Doesn't exist"})
            if ('argNames' not in bundle.data or
                'argVals' not in bundle.data or
                (len(bundle.data['argNames']) != len(bundle.data['argVals']))):
                return errors.update({"function": "Number of argument Names"
                                      "and Values provided don't match"})
            argVals = map(lambda x: json.loads(x), bundle.data['argVals'])
            argNames = bundle.data['argNames']
            for arg in F.args:
                print("Ahem", arg.name, argNames, arg.name in argNames)
                if arg.name in argNames:
                    i = argNames.index(arg.name)
                    if arg.type == 'int':
                        argVals[i] = int(argVals[i])
                    elif arg.type == 'float':
                        argVals[i] = float(argVals[i])
                    elif arg.type == 'list-int':
                        argVals[i] = map(int, list(argVals[i]))
                    elif arg.type == 'list-float':
                        argVals[i] = map(float, list(argVals[i]))
                    if ((type(argVals[i]) == list and
                         any(map(lambda x: (x > arg.max) or (x < arg.min),
                                 argVals[i]))) or
                        (type(argVals[i]) != list and
                         (argVals[i] > arg.max or argVals[i] < arg.min))):
                        errors.update({arg.name: "Out of Bounds"})
                        return errors
            print("Model Validated!")
        print(errors)
        return errors

    def obj_create(self, bundle, **kwargs):
        errors = self.is_valid(bundle)
        if errors:
            from tastypie.exceptions import ImmediateHttpResponse
            r = self.error_response(bundle.request, errors)
            raise ImmediateHttpResponse(response=r)
        func_key = bundle.data['function']['id']
        F = models.Function.objects(id=func_key).first()
        argVals = map(lambda x: json.loads(x), bundle.data['argVals'])
        #argVals = json.loads(bundle.data['argVals'])
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
                elif arg.type == 'list-int':
                    valid_values.append(map(int, list(argVals[i])))
                elif arg.type == 'list-float':
                    valid_values.append(map(float, list(argVals[i])))
            else: valid_values.append(arg.default)
        bundle.data['argNames'] = valid_names
        bundle.data['argVals'] = valid_values
        bundle.data['function'] = F
        bundle.data['name'] = F.name
        bundle.data['completed'] = False
        print("bundle.data", bundle.data)
        # TODO: If task was already run, retrieve result of the task instead
        from webserver.settings import celery_conn
        if F.path:
            fname = F.path.split('/')
            fname = fname[-1]
            fname = fname.split('.py')[0]
            print("R.Key ", fname+'.'+F.name)
            result = celery_conn.send_task(fname+'.'+F.name,
                                           valid_values, queue=fname)
            bundle.data['celery_uuid'] = result.id
            bundle.obj = models.Task(**bundle.data)
            bundle.obj.save()
            print("returning bundle")
            return bundle
