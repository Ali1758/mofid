from django.contrib import admin
from django.urls import path
from mofid.views import index_view
from crawler.views import DownloadView, download_items, full_crawling, custom_crawling
# from django.conf import settings
# from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('login', LoginView.as_view(), name='Login'),
    path('logout', LogoutView.as_view(), name='Logout'),
    path('download/', DownloadView.as_view(), name='download'),
    path('download/<slug:slug>/', download_items.as_view(), name='download_item'),
    path('defaultcrawling/', full_crawling, name='full_crawling'),
    path('customcrawling/', custom_crawling, name='custom_crawling'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)
