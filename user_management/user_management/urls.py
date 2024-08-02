from pydoc import visiblename
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from user_management.rest import views
from user_management.rest.views import UpdateUserProfileView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path("", include("pages.urls")),
	path("user/", views.user_data),
	path("user/me", views.me_data),
	path('user/update/', UpdateUserProfileView.as_view(), name='profile-update'),
    path("admin/", admin.site.urls),

] + static(settings.STATIC_URL, 
           document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
