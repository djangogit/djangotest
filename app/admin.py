from django.contrib import admin
from models import *
# Register your models here.

class userprofileAdmin(admin.ModelAdmin):
	list_display = ['fullname', 'email', 'phone']
	search_fields = ['fullname', 'email']
admin.site.register(userprofile, userprofileAdmin)


class sitevisitedAdmin(admin.ModelAdmin):
	list_display = ['user', 'sitesentered']
	search_fields = ['sitesentered', 'sitesentered']
admin.site.register(sitevisited, sitevisitedAdmin)
