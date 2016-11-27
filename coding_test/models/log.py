from django.db import models
from rest_framework.exceptions import APIException,ParseError,NotFound

class Log(models.Model):
	updated = models.DateTimeField(auto_now=True)
	key = models.TextField(blank=False) #need to make unqiue

	#data is saved as a string of set so that can add more values in future
	data = models.TextField(blank=False,default='{}')
	ACTION_CHOICES = (
		('Create','CREATE'),
		('Update','UPDATE')
	)
	action = models.CharField(max_length=6,choices=ACTION_CHOICES)
	class Meta:
		pass
	

