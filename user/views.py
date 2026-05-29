from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, Register2Serializer
#from rest_framework.permissions import IsAuthenticated
#from .permissions import IsSuperUser, IsReadOnlyUser
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful. Please wait for admin approval."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            # "user": {
            #     "id": user.id,
            #     "email": user.email,
            #     "role": user.role,
            # }
        }, status=status.HTTP_200_OK)

# class CustomLoginView(APIView):
#     def post(self, request):
#
#
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(email=email, password=password)
#         if not user:
#             return Response({"error": "Invalid credentials view"}, status=status.HTTP_401_UNAUTHORIZED)
#
#         if not user.is_active:
#             return Response({"error": "User account is not active view."}, status=status.HTTP_403_FORBIDDEN)
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "email": user.email,
#                 "role": user.role,
#             }
#         }, status=status.HTTP_200_OK)

   # serializer = LoginSerializer(data=request.data)
   #      if serializer.is_valid():
   #          return Response({"success": True})
   #      else:
   #          return Response(serializer.errors, status=400)
# class SomeProtectedView(APIView):
#     permission_classes = [IsAuthenticated, IsSuperUser]
#
#     def get(self, request):
#         return Response({"message": "Welcome, Super User!"})
#
# class ReadOnlyView(APIView):
#     permission_classes = [IsAuthenticated, IsReadOnlyUser]
#
#     def get(self, request):
#         return Response({"message": "Welcome, Read-Only User!"})

class RegisterCodeView(APIView):
    def post(self, request):
        serializer = Register2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کد تأیید به ایمیل شما ارسال شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                user.save()
                return Response({"message": "حساب کاربری تأیید شد."}, status=status.HTTP_200_OK)
            return Response({"error": "کد وارد شده صحیح نیست."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "کاربری با این ایمیل یافت نشد."}, status=status.HTTP_404_NOT_FOUND)


class VerifyCode2View(APIView):
    def post(self, request):
        identifier = request.data.get("identifier")
        code = request.data.get("code")

        try:
            if "@" in identifier:
                user = CustomUser.objects.get(email=identifier)
            else:
                user = CustomUser.objects.get(mobile=identifier)

            if user.verification_code == code:
                user.is_verified = True
                user.verification_code = None  # حذف کد پس از تأیید
                user.save()
                return Response({"message": "حساب کاربری تأیید شد."}, status=status.HTTP_200_OK)

            return Response({"error": "کد وارد شده صحیح نیست."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "کاربری با این اطلاعات یافت نشد."}, status=status.HTTP_404_NOT_FOUND)