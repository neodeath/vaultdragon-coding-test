#from some_model import SomemModel
from .vdobject_view_set import VDObjectViewSet
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'object': reverse('object-list', request=request, format=format),	
	})
