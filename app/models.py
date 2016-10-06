from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator

# Create your models here.



class userprofile(models.Model):
	user = models.OneToOneField(User)
	fullname = models.CharField(max_length=100)
	address = models.CharField(max_length=256)
	phone = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')], unique=True)
	email = models.EmailField(unique=True)
	
	class Meta:
		verbose_name_plural = "User Profile"
	
	def __unicode__(self):
		return str(self.user)
	def get_name(self, obj):
        	return obj.author.name
	get_name.admin_order_field  = 'user'
	get_name.short_description = 'User Name'


class sitevisited(models.Model):
	user = models.ForeignKey(userprofile)
	sitesentered = models.CharField(max_length=80)
	words = models.CharField(max_length=100, null=True, blank=True)
	inwords = models.CharField(max_length=100,null=True, blank=True)
	
	def __unicode__(self):
		return self.sitesentered
	
	class Meta:
		verbose_name_plural = "User Visited Sites"


