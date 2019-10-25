from django.contrib import admin
from django.urls import path
from telegram.views import my_view, IndexView
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('test/', view),
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='Login'),
    path('logout', LogoutView.as_view(), name='Logout')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
