from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

    # ✅ Redoc (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

]
