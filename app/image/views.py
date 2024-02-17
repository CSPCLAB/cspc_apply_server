from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import ImageSerializer
from swagger_response import *

from drf_yasg.utils import swagger_auto_schema


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# class ImageUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(request_body=ImageSerializer)
#     def post(self, request):
#         if request.user.is_authenticated:
#             image_serializer = ImageSerializer(data=request.data)
#             if image_serializer.is_valid():
#                 image_serializer.save()
#                 return Response(image_serializer.data, status=200)
#             else:
#                 return Response(image_serializer.errors, status=400)
