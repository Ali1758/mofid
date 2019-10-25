from django.contrib import admin
from django.urls import path
from telegram.views import my_view, IndexView

# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', view),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
