from django.contrib import admin

from . models import CustomUser

admin.site.register(CustomUser)

from . models import PhoneNumber,EmailAddress


admin.site.register(PhoneNumber)
admin.site.register(EmailAddress)
