from django.core.management.base import BaseCommand, CommandError
from netlambda.models import Function, Arg, Package
from os import listdir
import json

class Command(BaseCommand):
    help = 'Fill functions into DB'
    def createFunction (self, **kwargs):
        print kwargs
        if "args" in kwargs:
            print kwargs["args"]
            kwargs["args"] = [Arg(**arg) for arg in kwargs["args"]]
        print kwargs
        f = Function(**kwargs)
        f.save()
        return f
    def createPackage (self, **kwargs):
        if "functions" in kwargs:
            print kwargs["functions"]
            refs = []
            package_name = kwargs['path']
            package_name = package_name.split('/')
            package_name = package_name[-1]
            package_name = package_name.split('.py')[0]
            for f in kwargs["functions"]:
                f.update({'path':kwargs["path"],'package_name':package_name})
                refs.append(self.createFunction(**f))
            p = Package()
            p.name = package_name
            p.path = kwargs["path"]
            p.functions = refs
            p.save()
    def handle(self, *args, **options):
        jsonFilesPath = "../function-json/"
        functionFiles = [jsonFilesPath+f for f in listdir(jsonFilesPath) if f.endswith('.json')]
        for jsonFile in functionFiles:
            print jsonFile
            jdata = open(jsonFile)
            packageData = json.load(jdata)
            self.createPackage(**packageData)
            #self.createFunction(**functionData)
            jdata.close()
