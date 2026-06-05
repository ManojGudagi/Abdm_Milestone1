from django.urls import path
from django.views.generic import TemplateView # <-- ADD THIS IMPORT

# Adjust this import path depending on where you saved your biometric_views.py file!
from milestone1.enrollment_biometric.views.biometric_views import (
    FaceAuthInitView,
    FaceAuthStatusView,
    BiometricEnrolView
)

urlpatterns = [
    # --- ADD THIS BASE ROUTE TO SERVE THE HTML ---
    path('', TemplateView.as_view(template_name='biometric_enroll.html'), name='biometric-enroll-ui'),

    # ==========================================
    # 📸 FACE AUTH FLOW (3 Steps)
    # ==========================================
    path('biometric/face/init/', FaceAuthInitView.as_view(), name='face-auth-init'),
    path('biometric/face/status/', FaceAuthStatusView.as_view(), name='face-auth-status'),

    # ==========================================
    # 👆 👁️ 📸 UNIFIED VERIFICATION
    # ==========================================
    path('biometric/verify/', BiometricEnrolView.as_view(), name='biometric-verify'),
]