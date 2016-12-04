from django.db import models
from rest_framework.exceptions import APIException,ParseError,NotFound

class VDObject(models.Model):
	timestamp = models.DateTimeField(auto_now=True)
	key = models.TextField(primary_key=True,blank=False) #need to make unqiue
	value = models.TextField(blank=True)
	class Meta:
		pass
	

