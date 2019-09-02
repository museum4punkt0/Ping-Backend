import datetime
from django import template
from main.models import  MusemsTensor, TENSOR_STATUSES

register = template.Library()

@register.simple_tag
def current_status(pk):
    statuses = {'tensor_status': None, 'mobile_tensor_status': None}
    if pk != 'None':
        ms = MusemsTensor.objects.filter(museum=pk)
        if ms:
            statuses['tensor_status'] = getattr(ms[0], 'tensor_status', None)
            statuses['mobile_tensor_status'] = getattr(ms[0], 'mobile_tensor_status', None)
    return statuses