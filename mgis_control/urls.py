from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin

admin.site.site_header = 'MGIS.Control. Администирование'                  # default: "Django Administration"
admin.site.index_title = 'Управление'                                      # default: "Site administration"
admin.site.site_title = 'Администратор MGIS.Control'                       # default: "Django site admin"


from task_manager import views


schema_view = get_schema_view(
   openapi.Info(
      title="MGIS.Control API",
      default_version='v1.0',
      description="MGIS.Control Server API",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # url(r'^$', login_required(TemplateView.as_view(template_name="index.html")), name='home'),
    url(r'^$', views.mainPage, name='home'),

    path('login/', views.loginPage, name='login'),
    path('login', views.loginPage, name='login'),
    path('create_task_map', views.createTaskMap, name='create_task_map'),
    path('cancel_task', views.cancelTask, name='cancel_task'),
    path('logout', views.logoutPage, name='logout'),

    path('admin/', admin.site.urls),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/', include('api.urls', namespace='api'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

