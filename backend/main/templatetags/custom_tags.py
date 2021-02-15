import datetime
from django import template
from main.models import MusemsTensor, TENSOR_STATUSES

register = template.Library()


@register.simple_tag
def current_status(title):
    try:
        title = int(title)
    except:
        pass
    statuses = {"tensor_status": None, "mobile_tensor_status": None}
    if isinstance(title, str):
        ms = MusemsTensor.objects.filter(museum__localizations__title=title)
    elif isinstance(title, int):
        ms = MusemsTensor.objects.filter(museum__pk=title)
    if ms:
        statuses["tensor_status"] = getattr(ms[0], "tensor_status", None)
        statuses["mobile_tensor_status"] = getattr(ms[0], "mobile_tensor_status", None)
    return statuses
