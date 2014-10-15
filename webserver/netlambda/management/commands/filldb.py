from django.core.management.base import BaseCommand, CommandError
from netlambda.models import Function
from os import listdir
import json

class Command(BaseCommand):
    help = 'Fill functions into DB'
    def createFunction (self, **kwargs):
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
