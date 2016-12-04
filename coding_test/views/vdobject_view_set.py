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
		new_log = Log(updated=obj.timestamp, action = action, key = key_value, data = str_data)
		new_log.save();
	def get_response(self, data,timestamp):
		#import pdb;
		#pdb.set_trace();

		return {data['key']:data['value'],'timestamp':str(int(timestamp))}

	def retrieve(self, request, *args, **kwargs):
		
		timestamp = self.request.query_params.get('timestamp', None)
		instance = self.get_object()

		#get from log if the updated time is before the time stamp
		if timestamp is not None:
			try:
				datetime_timestamp = datetime.datetime.fromtimestamp(int(timestamp),tz=pytz.utc)
			except:
				return Response({"detail":"invalid timestamp provided"}, status=status.HTTP_400_BAD_REQUEST)

			
			if datetime_timestamp < instance.timestamp:
				#means need to look at log
				
				log_results = Log.objects.all().filter(updated__lt=datetime_timestamp,key=kwargs['pk']).order_by('-updated')[:1]
				
				if log_results.count() != 1:
					return Response({"detail":"Object not found"}, status=status.HTTP_404_NOT_FOUND)
				instance.value = json.loads(log_results[0].data)["value"]
		serializer = self.get_serializer(instance)
		return Response(serializer.data["value"])

	def create(self, request, *args, **kwargs):
		
		try:
			
			k,v = request.data.popitem()
			
			request_data = {'key':k,'value':v}
			
		except:
			return Response({"detail":"invalid input"}, status=status.HTTP_400_BAD_REQUEST)
		serializer = self.get_serializer(data=request_data)
		try:
			serializer.is_valid(raise_exception=True)
			obj = self.perform_create(serializer)
			#create path
			self.add_log('Create',k)

			ts = datetime.datetime.strptime(serializer.data["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
			headers = self.get_success_headers(serializer.data)

			return Response(self.get_response(serializer.data,ts), status=status.HTTP_201_CREATED, headers=headers)
		except ValidationError as e:
			if 'key' in e.detail and len(e.detail["key"]) == 1 and 'key already exist' in e.detail["key"][0]:			
				obj = VDObject.objects.all().filter(key=k)[0]
				
				#update path
				if obj.value != v:
					obj.value = v
					obj.save()
					
					self.add_log('Update',k)
				
				return Response(self.get_response(obj.__dict__,obj.timestamp.timestamp()))
			else:
				raise e


		

		
