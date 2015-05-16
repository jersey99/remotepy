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
    def celerify (self,fname, package_name, functions):
        outFname = fname.replace("/code/", "/celerified-code/")
        outfile = open(outFname+'.py','w')
        outfile.write("from celery import Celery\n")
        outfile.write("app = Celery('" + package_name +
                      "', backend='mongodb://localhost/turkeycalltest', broker='mongodb://localhost/turkeycalltest')\n")
        for l in open(fname+'.py','r').readlines():
            ll = l.strip()
            if ll.startswith('def'):
                ll = ll.split(' ')
                print ll[1], fname, functions
                if any(map(lambda x: ll[1] == x or ll[1].startswith(x+'('),functions)):
#                if ll[1] == fname or ll[1].startswith(fname+'('):
                    outfile.write('@app.task\n')
            outfile.write(l)
        outfile.close()
    def createPackage (self, **kwargs):
        if "functions" in kwargs:
            print kwargs["functions"]
            refs = []
            package_name = kwargs['path']
            package_name_file = package_name.split('.py')[0]
            package_name = package_name.split('/')
            package_name = package_name[-1]
            package_name = package_name.split('.py')[0]
            fnames = []
            for f in kwargs["functions"]:
                f.update({'path':kwargs["path"],'package_name':package_name})
                refs.append(self.createFunction(**f))
                fnames.append(f["name"])
            #self.celerify(package_name_file, package_name, fnames)
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
