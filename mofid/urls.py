from django.contrib import admin
from django.urls import path
from mofid.views import index_view
from crawler.views import download_view, download_items
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('login', LoginView.as_view(), name='Login'),
    path('logout', LogoutView.as_view(), name='Logout'),
    path('download/', download_view, name='download'),
    path('download/<slug:slug>/', download_items, name='download_item'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
