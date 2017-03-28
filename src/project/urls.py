from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from services.views import index, publish
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/media/favicon.ico', permanent=True)

urlpatterns = [
	url(r'^favicon\.ico$', favicon_view),
	url(r'^$', index, name='index'),
 	url(r'^services/', include('services.urls')),
 	url(r'^admin/publish/(?P<dest>\w{0,4})/$', publish, name='publish'),
 	url(r'^admin/', admin.site.urls),
 	url(r'^redactor/', include('redactor.urls')),
 	url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
