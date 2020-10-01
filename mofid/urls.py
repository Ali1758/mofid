from django.contrib import admin
from django.urls import path
from mofid.views import index_view
from crawler.views import download_view, download_items, backups_view, download_backup
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
    path('repair/<slug:slug>/', repair_items, name='repair_item'),
    path('backups/<slug:slug>/', backups_view, name='backups'),
    path('backups/download/<slug:slug>/', download_backup, name='download_backup'),
]
