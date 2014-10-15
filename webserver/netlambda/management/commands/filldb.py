from django.core.management.base import BaseCommand, CommandError
from netlambda.models import Function, Arg
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
        Function(**kwargs).save()
    def handle(self, *args, **options):
        jsonFilesPath = "../function-json/"
        functionFiles = [jsonFilesPath+f for f in listdir(jsonFilesPath) if f.endswith('.json')]
        for jsonFile in functionFiles:
            print jsonFile
            jdata = open(jsonFile)
            functionData = json.load(jdata)
            self.createFunction(**functionData)
            jdata.close()
