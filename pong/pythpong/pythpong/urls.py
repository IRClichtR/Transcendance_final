from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from game.views import GameViewset
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pong/', include('game.urls')),
    path('', include('game.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    #simple jwt inclusion
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/', include('game.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
