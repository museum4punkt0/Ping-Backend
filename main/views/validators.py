import datetime
import uuid

from main.models import ObjectsItem

def validate_common_fields(entity_name, data, o_model, sync_ids, entity_sync_id=None, created_at=None, updated_at=None, ob_sync_id=None):
    errors = []
    if entity_sync_id:
        try:
            uuid_obj = uuid.UUID(entity_sync_id, version=4)
            data['sync_id'] = entity_sync_id
        except:
            errors.append({f'{entity_name}': f'Inappropriate {entity_name} sync id {entity_sync_id} uuid'})
    else:
        errors.append({f'{entity_name}': f'Sync id for {entity_name} is required'})

    if created_at:
        try:
            validtime = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            data['created_at'] = validtime.astimezone()
        except:
            errors.append({f'{entity_name}': f'Inappropriate "created_at" time format value for {entity_name} {entity_sync_id} sync_id'})
    else:
        errors.append({f'{entity_name}': f'Value "created_at" for {entity_name} {entity_sync_id} is required'})

    if updated_at:
        try:
            validtime = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            data['updated_at'] = validtime.astimezone()
        except:
            errors.append({f'{entity_name}': f'Inappropriate "updated_at" time format value for {entity_name} {entity_sync_id} sync_id'})
    else:
        errors.append({f'{entity_name}': f'Value "updated_at" for {entity_name} {entity_sync_id} is required'})

    if ob_sync_id:
        try:
            uuid_obj = uuid.UUID(ob_sync_id, version=4)
        except ValueError:                        
            errors.append({f'{entity_name}': f'Inappropriate "object_sync id": {ob_sync_id} uuid for {entity_name} sync_id'})
    else:
        errors.append({f'{entity_name}': 'Sync id for object is required'})

    objects_item = ObjectsItem.objects.filter(sync_id=uuid_obj).first()
    if objects_item:
        data['objects_item'] = objects_item
    else:
        errors.append({f'{entity_name}': 'Inappropriate or absent objects sync_id'})

    if o_model.objects.filter(sync_id=ob_sync_id):
        errors.append({f'{entity_name}': f'{entity_name} with this sync id {ob_sync_id} already exist'})

    if data['sync_id'] in sync_ids:
        errors.append({f'{entity_name}': f'Sync id {data["sync_id"]} in {entity_name} data sets must be unique'})
    else:
        sync_ids.append(data['sync_id'])

    return errors