from mongodbforms import DocumentForm
from models import Task, Function


class TaskForm(DocumentForm):
    class Meta:
        model = Task
        fields = ['argVals']
