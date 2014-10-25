from django.conf.urls import patterns, include, url
from netlambda.resources import FunctionResource, TaskResource, PackageResource
from netlambda.views import functionView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
function_resource = FunctionResource()
package_resource = PackageResource()
task_resource = TaskResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webserver.views.home', name='home'),
    url(r'^function/', include(function_resource.urls)),
    url(r'^package/', include(package_resource.urls)),
    # url(r'^webserver/', include('webserver.foo.urls')),
    url(r'^task/', include(task_resource.urls)),
    url(r'^(?P<function_name>\s+)$', functionView),
    url(r'^$', functionView)

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
