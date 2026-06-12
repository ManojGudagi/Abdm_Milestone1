from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import TemplateView

schema_view = get_schema_view(
    openapi.Info(
        title="Abdm_Integration Aadhaar API",
        default_version='v1',
        description="ABHA Enrollment APIs (OTP + Session + Enrol)",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    path('portal/milestone1/', TemplateView.as_view(template_name='milestone1.html'), name='m1-portal'),

    path('portal/milestone2/', TemplateView.as_view(template_name='milestone2.html'), name='m2-portal'),
    
    path('portal/milestone3/', TemplateView.as_view(template_name='milestone3.html'), name='m3-portal'),

    path('portal/delete/', TemplateView.as_view(template_name='delete.html'), name='delete-portal'),

    path('portal/deactivate/', TemplateView.as_view(template_name='deactivate.html'), name='deactivate-portal'),

    path('admin/', admin.site.urls),

    path('aadhaar/', include('milestone1.enrollment_aadhaar.urls')),

    path("api2/v1/",include("milestone1.abha_profile.urls")),

    path("api/v1/",include("milestone1.enrollment_mobile.urls")),

    path("api3/v1/",include("milestone1.enrollment_dl.urls")),
    
    path("api4/v1/",include("milestone1.enrollment_biometric.urls")),

    path("api5/v1/",include("milestone1.abha_login.urls")),

    path("api6/v1/",include("milestone1.mobile_login.urls")),

    path("api7/v1/",include("milestone1.abha_search.urls")),
    
    path("api8/v1/",include("milestone1.profile_update.urls")),

    path("api9/v1/",include("milestone1.abhanumber_recover.urls")),

    path("api10/v1/",include("milestone1.abha_delete.urls")),

    path("api11/v1/",include("milestone1.abha_deactivate.urls")),




    path('api_m2/v2/gateway/', include('milestone2.gateway_auth.urls')),

    path('api_m2/v2/bridge/', include('milestone2.bridge_update.urls')),

    path('api_m2/v2/facility/', include('milestone2.facility_linkage.urls')),

    path('api_m2/v2/search/', include('milestone2.bridge_search.urls')),

    path('api_m2/v2/config/', include('milestone2.gateway_config.urls')),

    path('api_m2/v2/token/', include('milestone2.link_token.urls')),

    path('api_m2/v2/care-context/', include('milestone2.care_context.urls')),

    path('api_m2/v2/update/', include('milestone2.notify_update.urls')),

    path('api_m2/v2/sms/', include('milestone2.sms_notify.urls')),

    path('api_m2/v2/hiu/', include('milestone2.hiu_discover.urls')),

    path('api_m2/v3/user-initiated-linking/link/care-context/', include('milestone2.hiu_on_init.urls')),
    path('api_m2/v3/user-initiated-linking/link/care-context/', include('milestone2.hiu_on_confirm.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # ✅ Redoc (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

]


