from rest_framework import serializers
from coding_test.models import VDObject

class VDObjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = VDObject
		fields = ('key','value','timestamp')


