from rest_framework import serializers
from captcha.models import  Captcha
from .models import CustomUser
from django.contrib.auth import authenticate
from user.tasks import  send_verification_code


class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    captcha_id = serializers.CharField(required=True)
    user_input = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile', 'email', 'password', 're_password', 'captcha_id', 'user_input','role']

    def validate(self, data):
        captcha_id = data.get('captcha_id')
        user_input = data.get('user_input')
        try:
            captcha = Captcha.objects.get(captcha_id=captcha_id)
        except Captcha.DoesNotExist:
            raise serializers.ValidationError("Invalid CAPTCHA ID")
        if captcha.text != user_input:
            raise serializers.ValidationError("Incorrect CAPTCHA input")
        return data
    def create(self, validated_data):
        validated_data.pop('re_password')
        validated_data.pop('captcha_id')
        validated_data.pop('user_input')
        user = CustomUser.objects.create_user(**validated_data, is_active=False, role='user')
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    captcha_id = serializers.CharField(required=True)
    user_input = serializers.CharField(required=True)
    remember_me = serializers.BooleanField(default=False)
    show_password = serializers.BooleanField(default=False)

    def validate(self, data):
        #captcha
        captcha_id = data.get('captcha_id')
        user_input = data.get('user_input')
        try:
            captcha = Captcha.objects.get(captcha_id=captcha_id)
        except Captcha.DoesNotExist:
            raise serializers.ValidationError("Invalid CAPTCHA ID")
        if captcha.text != user_input:
         raise serializers.ValidationError("Incorrect CAPTCHA input")
        #user
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials serilizser."})
        if not user.is_active:
            raise serializers.ValidationError({"error": "User account is not active. serilizer"})
        data['user'] = user
        return data



# class RegisterCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ("email",)
#
#     def create(self, validated_data):
#         user = CustomUser.objects.create(email=validated_data["email"])
#         code = send_verification_email.delay(user.email)  # ارسال ایمیل به صورت Async
#         user.verification_code = code  # ذخیره کد در دیتابیس
#         user.save()
#         return user

class Register2Serializer(serializers.ModelSerializer):
    identifier = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("identifier",)

    def create(self, validated_data):
        identifier = validated_data["identifier"]

        # بررسی اینکه آیا identifier یک ایمیل است یا شماره موبایل
        if "@" in identifier:  # اگر ایمیل باشد
            user, created = CustomUser.objects.get_or_create(email=identifier)
            contact_type = 'email'
        else:  # اگر شماره موبایل باشد
            user, created = CustomUser.objects.get_or_create(mobile=identifier)
            contact_type = 'mobile'

        # ارسال کد تأیید با Celery (برای موبایل یا ایمیل)
        send_verification_code.delay({contact_type: identifier})

        return user