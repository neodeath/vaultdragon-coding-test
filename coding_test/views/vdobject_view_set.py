from coding_test.models.vdobject import VDObject
from coding_test.serializer import VDObjectSerializer

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import ValidationError

from coding_test.models.log import Log

import json
import datetime
import pytz

class VDObjectViewSet(viewsets.ModelViewSet):

	queryset = VDObject.objects.all()
	serializer_class = VDObjectSerializer

	def add_log(self,action, key_value):
		#rather then setting the time here, we get from DB for added data integrity
		obj = VDObject.objects.all().filter(key=key_value)[0]
		#what happen if no changed?
		data = {"value":obj.value}
		str_data = json.dumps(data)
		new_log = Log(updated=obj.updated, action = action, key = key_value, data = str_data)
		new_log.save();
	def get_response(self, data):
		return {data['key']:data['value']}

	def retrieve(self, request, *args, **kwargs):
		
		timestamp = self.request.query_params.get('timestamp', None)
		instance = self.get_object()

		#get from log if the updated time is before the time stamp
		if timestamp is not None:
			try:
				datetime_timestamp = datetime.datetime.fromtimestamp(int(timestamp),tz=pytz.utc)
			except:
				return Response({"detail":"invalid timestamp provided"}, status=status.HTTP_400_BAD_REQUEST)

			
			if datetime_timestamp < instance.updated:
				#means need to look at log
				
				log_results = Log.objects.all().filter(updated__lt=datetime_timestamp,key=kwargs['pk']).order_by('-updated')[:1]
				
				if log_results.count() != 1:
					return Response({"detail":"Object not found"}, status=status.HTTP_404_NOT_FOUND)
				instance.value = json.loads(log_results[0].data)["value"]
		serializer = self.get_serializer(instance)
		return Response(serializer.data["value"])

	def create(self, request, *args, **kwargs):
		
		serializer = self.get_serializer(data=request.data)
		try:
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			#create path
			self.add_log('Create',request.data['key'])

			headers = self.get_success_headers(serializer.data)

			return Response(self.get_response(serializer.data), status=status.HTTP_201_CREATED, headers=headers)
		except ValidationError as e:
			if 'key' in e.detail and len(e.detail["key"]) == 1 and 'key already exist' in e.detail["key"][0]:			
				obj = VDObject.objects.all().filter(key=request.data['key'])[0]
				
				#update path
				if obj.value != request.data['value']:
					obj.value = request.data['value']
					obj.save()
					
					self.add_log('Update',request.data['key'])
				
				return Response(self.get_response(serializer.data))
			else:
				raise e


		

		
