from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from milestone1.enrollment_aadhaar.services.encryption_service import encrypt_data
from milestone1.enrollment_aadhaar.serializers.encrypt_serializer import EncryptSerializer
from milestone1.enrollment_aadhaar.services.encryption_service import decrypt_data

class EncodeDataView(APIView):

    def post(self, request):
        serializer = EncryptSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data["data"]

        encoded = encrypt_data(data)

        return Response({
            "encodedData": encoded
        }, status=status.HTTP_200_OK)
