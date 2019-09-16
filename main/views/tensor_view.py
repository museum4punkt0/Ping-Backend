import base64
import datetime
from rest_framework.decorators import api_view
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from main.models import Users, Museums, ObjectsItem, Settings
from main.utils import label_image
from main.apps import tensors
import logging
import boto3
import uuid
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile



@api_view(['POST'])
def recognize(request):
    user_id = request.GET.get('user_id', None)
    museum_id = request.GET.get('museum_id', None)
    image = request.data.get('image')
    object_id = request.data.get('object_id')

    if not image:
        return JsonResponse({'error': 'Image is required'}, safe=True)

    format = image.name.split('.')[1]

    if not isinstance(image, (InMemoryUploadedFile, TemporaryUploadedFile)) or format not in ('jpg', 'jpeg', 'JPEG'):
        return JsonResponse({'error': 'Image must be jpg format'}, safe=True)

    if user_id:
        try:
            user = Users.objects.get(device_id=user_id)
        except Exception as e:
            logging.error(f'User id {user_id} does not exist {e.args}')
            return JsonResponse({'error': f'User id {user_id} does not exist {e.args}'}, safe=True)
    else:
        logging.error(f'Existing user id must be provided, device id: {user_id}')
        return JsonResponse({'error': 'Existing user id must be provided'}, safe=True)

    if museum_id:
        try:
            museum = Museums.objects.get(sync_id=museum_id)
            museum_loc = museum.localizations.first()
            if museum_loc:
                museum_name = museum_loc.title
            else:
                museum_name = museum_id
        except (Museums.DoesNotExist, ValidationError):
            return JsonResponse({'error': 'Museum not found'}, status=404)
    else:
        logging.error(f'Museum id must be provided')
        return JsonResponse({'error': 'Existing museum id must be provided'},
                            safe=True, status=400)
  
    if tensors:
        museum_tensor = tensors.get(museum.sync_id)
        if museum_tensor:
            model_obj = museum_tensor.get('tensor_flow_model', None)
            label_obj = museum_tensor.get('tensor_flow_lables', None)
        else:
            return JsonResponse({'error': 'Model not found'}, status=404)
    else:
        return JsonResponse({'error': 'Model not found'}, status=404)

    img_bytes = BytesIO(image.read())

    if model_obj and label_obj:
        predict = label_image.recognize(model_obj, img_bytes.read(), label_obj)
    else:
        return JsonResponse({'error': 'No tensor model or labels preloaded for museum'}, safe=True)

    if object_id:

        try:
            obj = ObjectsItem.objects.get(sync_id=object_id)
            obj_name = obj.localizations.first().title or object_id
        except (ObjectsItem.DoesNotExist, ValidationError):
            return JsonResponse({'error': 'Object not found'}, status=404)

        if not uuid.UUID(object_id):
            return JsonResponse({'error': 'object_id must be UUID format'}, status=400)

        response = _match_coincidence(predict, object_id, img_bytes,
                                      museum_name, format, obj_name)
    else:
        response = _search_for_object(predict)

    return response


def _search_for_object(predict):
    first = max(predict, key=predict.get)
    splited = first.split(' ')
    sync_id = '-'.join(splited[-5:])

    return JsonResponse({'sync_id': sync_id, 'prediction': str(predict[first])})


def _match_coincidence(predict, object_id, image, museum, format, obj_name):
    recognition_threshold = Settings.objects.first().recognition_threshold

    for obj, key in predict.items():
        splited = obj.split(' ')
        sync_id = '-'.join(splited[-5:])

        if sync_id == object_id:
            if key > recognition_threshold:

                if key > 70:
                    _upload_image_to_storage(image, museum, format, obj_name)

                return JsonResponse({'sync_id': sync_id, 'prediction': str(key)})
            break

    return JsonResponse({'error': "The object is not identified"}, status=204)


def _upload_image_to_storage(image, museum, format, obj_name):
    client = boto3.client('s3')

    date = datetime.datetime.today().strftime("%m-%Y")
    path = f'ti/{museum}/{obj_name}/{date}/{uuid.uuid4()}.{format}'

    try:
        client.upload_fileobj(image, 'meinobjekt', path)
    except Exception:
        pass
