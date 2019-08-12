from django.apps import AppConfig
from django.dispatch import receiver
from django.db.backends.signals import connection_created
from mein_objekt.settings import WSGI

class MainConfig(AppConfig):
    name = 'main'

tensors = {}

@receiver(connection_created)
def my_receiver(connection, **kwargs):
    if WSGI:
        from main.models import Museums
        museums = Museums.objects.all()
        try:
            for museum in museums:
                tensor = museum.museumtensor.first()
                if tensor:
                    model = getattr(tensor, 'tensor_flow_model', None)
                    labels = getattr(tensor, 'tensor_flow_lables', None)
                    tensors[museum.sync_id] = {'tensor_flow_model': model.file.read(),
                            'tensor_flow_lables': labels.file.read()}
        except:
            pass
    connection_created.disconnect(my_receiver)

