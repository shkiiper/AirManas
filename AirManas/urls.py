from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from general.views import IndexView, HowToUseView, DocumentsView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.decorators import login_required
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    # swagger
    path("server/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "server/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('instructions', HowToUseView.as_view(), name='instructions'),
    path('documents', login_required(DocumentsView.as_view()), name='documents'),

    path('user/', include('users.urls', namespace='users')),
    path('vacation/', include('vacations.urls', namespace='vacation')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
