from django.http import HttpResponse
from django.template import loader, RequestContext

def functionView(request, function):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context))
def functionView(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(RequestContext(request)))
