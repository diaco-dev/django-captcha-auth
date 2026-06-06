from django.contrib import admin
from captcha.models import APIKey, Captcha
# Register your models here.
admin.site.register(APIKey)
admin.site.register(Captcha)
