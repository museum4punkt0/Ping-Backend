import base64
from rest_framework.decorators import api_view
from io import BytesIO
from PIL import Image
from django.http import JsonResponse
from main.models import Users, Museums
from main.utils import label_image
from main.apps import tensors
import logging

@api_view(['POST'])
def recognize(request):
    user_id = request.GET.get('user_id', None)
    museum_id = request.GET.get('museum_id', None)

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
        museum = Museums.objects.get(sync_id=museum_id)
    else:
        logging.error(f'Museum id must be provided')
        return JsonResponse({'error': 'Existing museum id must be provided'},
                            safe=True, status=400)

    if tensors:
        museum_tensor = tensors[museum.name]
        model_obj = museum_tensor.get('tensor_flow_model', None)
        label_obj = museum_tensor.get('tensor_flow_lables', None)

    post_data = request.data
    if post_data:
        image = post_data.get('image')
    else:
        return JsonResponse({'error': 'json data with schema {"image": "<base64 image encoded>" must be transfered}'}, safe=True)

    if image:
        try:
            img_data = base64.b64decode(image)
        except:
            return JsonResponse({'error': 'Inappropriate "image" encoding'}, safe=True)

    if model_obj and label_obj:
        predict = label_image.recognize(model_obj, img_data, label_obj)
        first = max(predict, key=predict.get)
        splited = first.split(' ')
        sync_id = '-'.join(splited[-5:])
    else:
        return JsonResponse({'error': 'No tensor model or labels preloaded for museum'}, safe=True)

    return JsonResponse({'sync_id': sync_id, 'prediction': str(predict[first])})