import json
import datetime
from rest_framework.renderers import JSONRenderer



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y,%m,%d')
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        else:
            return super(DateTimeEncoder, self).default(obj)


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}

        #determine the resource name for this request - default to objects if not defined
        resource = getattr(renderer_context.get('view').get_serializer().Meta, 'resource_name', 'objects')

        #check if the results have been paginated
        if data.get('paginated_results'):
            #add the resource key and copy the results
            response_data['meta'] = data.get('meta')
            response_data[resource] = data.get('paginated_results')
        else:
            response_data[resource] = data

        #call super to render the response
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

        return response