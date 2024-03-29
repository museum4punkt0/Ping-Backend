import base64
import datetime
import uuid
import logging
import distutils.util
import json
from io import BytesIO
from PIL import Image
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.conf import settings

from main.models import (
    ObjectsItem,
    Chats,
    Votings,
    Collections,
    Categories,
    UsersLanguageStyles,
    UserTour,
    MuseumTour,
    Users,
    LOCALIZATIONS_CHOICES,
    LANGUEAGE_STYLE_CHOICES,
)

POSITION_RANGE = {"x": (0, 500), "y": (0, 999)}


def validate_common_fields(
    entity_name,
    data,
    action,
    sync_ids=None,
    o_model=None,
    entity_sync_id=None,
    created_at=None,
    updated_at=None,
    ob_sync_id=None,
):
    uuid_obj = None
    errors = []
    if entity_sync_id:
        try:
            uuid_obj = uuid.UUID(entity_sync_id, version=4)
            data["sync_id"] = entity_sync_id
        except:
            errors.append(
                {
                    f"{entity_name}": f"Inappropriate {entity_name} sync id {entity_sync_id} uuid"
                }
            )
    else:
        errors.append({f"{entity_name}": f"Sync id for {entity_name} is required"})

    if created_at:
        try:
            validtime = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            data["created_at"] = validtime.astimezone()
        except:
            errors.append(
                {
                    f"{entity_name}": f'Inappropriate "created_at" time format value for {entity_name} {entity_sync_id} sync_id'
                }
            )
    else:
        errors.append(
            {
                f"{entity_name}": f'Value "created_at" for {entity_name} {entity_sync_id} is required'
            }
        )

    if updated_at:
        try:
            validtime = datetime.datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            data["updated_at"] = validtime.astimezone()
        except:
            errors.append(
                {
                    f"{entity_name}": f'Inappropriate "updated_at" time format value for {entity_name} {entity_sync_id} sync_id'
                }
            )
    else:
        errors.append(
            {
                f"{entity_name}": f'Value "updated_at" for {entity_name} {entity_sync_id} is required'
            }
        )

    if action == "add":
        if o_model.objects.filter(sync_id=entity_sync_id):
            if entity_name == "collection":
                user = Users.objects.filter(collections__sync_id=entity_sync_id).first()
                errors.append(
                    {
                        f"{entity_name}": f"{entity_name} with this sync id {entity_sync_id} already exist in account of user: {user.sync_id}"
                    }
                )
            else:
                errors.append(
                    {
                        f"{entity_name}": f"{entity_name} with this sync id {entity_sync_id} already exist"
                    }
                )

        if data["sync_id"] in sync_ids:
            errors.append(
                {
                    f"{entity_name}": f'Sync id {data["sync_id"]} in {entity_name} data sets must be unique'
                }
            )
        else:
            sync_ids.append(data["sync_id"])

    if entity_name in ["user", "tour"]:
        return errors
    else:
        if ob_sync_id:
            try:
                uuid_obj = uuid.UUID(ob_sync_id, version=4)
            except ValueError as e:
                errors.append(
                    {
                        f"{entity_name}": f'Inappropriate "object_sync id": {ob_sync_id} uuid for {entity_name} sync_id, {e.args}'
                    }
                )
                return errors
        else:
            errors.append({f"{entity_name}": "Sync id for object is required"})

        objects_item = ObjectsItem.objects.filter(sync_id=uuid_obj).first()
        if objects_item:
            data["objects_item"] = objects_item
        else:
            errors.append(
                {
                    f"{entity_name}": f"Inappropriate or absent objects sync_id: {uuid_obj}"
                }
            )

    return errors


def validate_chats(
    action,
    data,
    user,
    errors,
    ch_sync_id,
    created_at,
    updated_at,
    ob_sync_id,
    finished,
    planned,
    history,
    last_step,
):

    csync_ids = []
    c_errors = validate_common_fields(
        "chat",
        data,
        action,
        sync_ids=csync_ids,
        o_model=Chats,
        entity_sync_id=ch_sync_id,
        created_at=created_at,
        updated_at=updated_at,
        ob_sync_id=ob_sync_id,
    )

    errors[f"{action}_errors"].extend(c_errors)

    if len(errors[f"{action}_errors"]) > 0:
        return None, errors

    if finished is not None:
        if isinstance(finished, str):
            try:
                bl = bool(distutils.util.strtobool(finished))
                data["finished"] = bl
            except Exception as ex:
                logging.error(
                    f'Inappropriate "finished":{ex} bool value for chat {ch_sync_id} sync_id'
                )
                errors[f"{action}_errors"].append(
                    {
                        "chat": f'Inappropriate "finished" bool value for chat {ch_sync_id} sync_id'
                    }
                )
        elif isinstance(finished, bool):
            data["finished"] = finished
    else:
        errors[f"{action}_errors"].append(
            {"chat": f'Value "finished" for chat {ch_sync_id} is required'}
        )

    if history is not None:
        data["history"] = history
    else:
        errors[f"{action}_errors"].append(
            {"chat": f'Value "history" for chat {ch_sync_id} is required'}
        )

    if planned is not None:
        if isinstance(planned, str):
            try:
                bl = bool(distutils.util.strtobool(planned))
                data["planned"] = bl
            except Exception as ex:
                logging.error(
                    f'Inappropriate "planned":{ex} bool value for chat {ch_sync_id} sync_id'
                )
                errors[f"{action}_errors"].append(
                    {
                        "chat": f'Inappropriate "planned" bool value for chat {ch_sync_id} sync_id'
                    }
                )
        elif isinstance(planned, bool):
            data["planned"] = planned
    else:
        errors[f"{action}_errors"].append(
            {"chat": f'Value "planned" for chat {ch_sync_id} is required'}
        )

    if last_step is not None:
        try:
            ls = int(last_step)
            data["last_step"] = ls
        except:
            errors[f"{action}_errors"].append(
                {
                    "chat": f'Inappropriate "last step" integer value for chat {ch_sync_id} sync_id'
                }
            )
    else:
        errors[f"{action}_errors"].append(
            {"chat": f'Value "last step" for chat {ch_sync_id} is required'}
        )

    data["user"] = user

    return data, errors


def validate_votings(
    action, data, user, errors, vt_sync_id, created_at, updated_at, ob_sync_id, vote
):

    vsync_ids = []
    c_errors = validate_common_fields(
        "vote",
        data,
        action,
        sync_ids=vsync_ids,
        o_model=Votings,
        entity_sync_id=vt_sync_id,
        created_at=created_at,
        updated_at=updated_at,
        ob_sync_id=ob_sync_id,
    )

    errors[f"{action}_errors"].extend(c_errors)

    if len(errors[f"{action}_errors"]) > 0:
        return None, errors

    if vote is not None:
        if isinstance(vote, str):
            try:
                bl = bool(distutils.util.strtobool(vote))
                data["vote"] = bl
            except:
                errors[f"{action}_errors"].append(
                    {
                        "vote": f'Inappropriate "vote" bool value for chat {vt_sync_id} sync_id'
                    }
                )
        elif isinstance(vote, bool):
            data["vote"] = vote
    else:
        errors[f"{action}_errors"].append(
            {"vote": f'Value "vote" for vote {vt_sync_id} is required'}
        )

    data["user"] = user

    return data, errors


def validate_collections(
    action,
    data,
    user,
    errors,
    cl_sync_id,
    created_at,
    updated_at,
    ob_sync_id,
    image,
    ctgrs,
):

    clsync_ids = []
    uuid_obj = None
    c_errors = validate_common_fields(
        "collection",
        data,
        action,
        sync_ids=clsync_ids,
        o_model=Collections,
        entity_sync_id=cl_sync_id,
        created_at=created_at,
        updated_at=updated_at,
        ob_sync_id=ob_sync_id,
    )
    errors[f"{action}_errors"].extend(c_errors)

    if len(errors[f"{action}_errors"]) > 0:
        return None, errors

    if image and image.size > 0:
        image_name = f"collectns_images/{str(cl_sync_id)}/image.jpg"
        data["image"] = (image, image_name)
    else:
        errors[f"{action}_errors"].append(
            {"collection": f"Image is required and must be jpg or png format"}
        )

    if ctgrs:
        if isinstance(ctgrs, list):
            for cat in ctgrs:
                try:
                    uuid_obj = uuid.UUID(cat, version=4)
                except:
                    errors[f"{action}_errors"].append(
                        {
                            "collection": f"Inappropriate collection category sync id {cat}"
                        }
                    )

                category_object = Categories.objects.filter(sync_id=uuid_obj).first()
                if category_object:
                    data["category"].append(category_object)
                else:
                    errors[f"{action}_errors"].append(
                        {"collection": "Inappropriate or absent category sync_id"}
                    )
        elif isinstance(ctgrs, str):
            try:
                uuid_obj = uuid.UUID(ctgrs, version=4)
            except:
                errors[f"{action}_errors"].append(
                    {"collection": f"Inappropriate collection category sync id {ctgrs}"}
                )

            category_object = Categories.objects.filter(sync_id=uuid_obj).first()
            if category_object:
                data["category"].append(category_object)
            else:
                errors[f"{action}_errors"].append(
                    {"collection": "Inappropriate or absent category sync_id"}
                )
    else:
        errors[f"{action}_errors"].append(
            {"collection": "Sync id for collection category is required"}
        )

    data["user"] = user

    return data, errors


def validate_user(
    action,
    data,
    user,
    errors,
    us_sync_id,
    created_at,
    updated_at,
    name,
    avatar,
    category,
    positionx,
    positiony,
    floor,
    language,
    language_style,
    font_size,
    level,
    score,
    device_id,
):
    uuid_obj = None

    c_errors = validate_common_fields(
        "user",
        data,
        action,
        entity_sync_id=us_sync_id,
        created_at=created_at,
        updated_at=updated_at,
    )
    errors[f"{action}_errors"].extend(c_errors)

    if len(errors[f"{action}_errors"]) > 0:
        return None, errors

    if name:
        data["name"] = str(name)

    if avatar:
        if avatar.size > 0:
            avatar_name = f"users_avatars/{str(us_sync_id)}/image.jpg"
            data["avatar"] = (avatar, avatar_name)
        else:
            errors[f"{action}_errors"].append({"user": f"Image must be not null size"})

    if category:
        try:
            uuid_obj = uuid.UUID(category, version=4)
        except:
            errors[f"{action}_errors"].append(
                {"user": f"Inappropriate user sync id {category} "}
            )

        category_object = Categories.objects.filter(sync_id=uuid_obj).first()
        if category_object:
            data["category"] = category_object
        else:
            errors[f"{action}_errors"].append(
                {"user": "Inappropriate category sync_id"}
            )

    if positionx is not None:
        try:
            px = int(positionx)
            data["positionx"] = px
            # TODO improve position validation
            # if not POSITION_RANGE['x'][0] <= px <= POSITION_RANGE['x'][1]:
            #     errors[f'{action}_errors'].append({'user': f'"positionx"  value for user {us_sync_id} sync_id must be in range {POSITION_RANGE["x"]}'})
        except:
            errors[f"{action}_errors"].append(
                {
                    "user": f'Inappropriate "positionx" integer value for user {us_sync_id} sync_id'
                }
            )
    else:
        errors[f"{action}_errors"].append(
            {"user": f'Value "positionx" for user {us_sync_id} is required'}
        )

    if positiony is not None:
        try:
            py = int(positiony)
            data["positiony"] = py
            # TODO improve position validation
            # if not POSITION_RANGE['y'][0] <= py <= POSITION_RANGE['y'][1]:
            #     errors[f'{action}_errors'].append({'user': f'"positiony"  value for user {us_sync_id} sync_id must be in range {POSITION_RANGE["y"]}'})
        except:
            errors[f"{action}_errors"].append(
                {
                    "user": f'Inappropriate "positiony" integer value for user {us_sync_id} sync_id'
                }
            )
    else:
        errors[f"{action}_errors"].append(
            {"user": f'Value "positiony" for user {us_sync_id} is required'}
        )

    if floor is not None:
        try:
            fl = int(floor)
            data["floor"] = fl
        except:
            errors[f"{action}_errors"].append(
                {
                    "user": f'Inappropriate "floor" integer value for user {us_sync_id} sync_id'
                }
            )
    else:
        errors[f"{action}_errors"].append(
            {"user": f'Value "floor" for user {us_sync_id} is required'}
        )

    if language and language.lower() in LOCALIZATIONS_CHOICES:
        data["language"] = language.lower()
    else:
        errors[f"{action}_errors"].append(
            {"user": f'Value "language" for user {us_sync_id} is not available'}
        )

    if level is not None:
        try:
            level = int(level)
            data["user_level"] = level
        except:
            errors[f"{action}_errors"].append(
                {"user": f'Value of "level" for user {us_sync_id} must be integer'}
            )

    if font_size:
        try:
            font_size = str(font_size)
            data["font_size"] = font_size
        except:
            errors[f"{action}_errors"].append(
                {"user": f'Value of "font_size" for user {us_sync_id} must be string'}
            )

    ls = getattr(user, "userslanguagestyles", None)
    if not ls:
        ls = UsersLanguageStyles.objects.create(user=user)
    data["language_style"] = ls

    if isinstance(language_style, list):
        try:
            data["language_style"].language_style = language_style
        except:
            errors[f"{action}_errors"].append(
                {"user": f'Value "language_style" for user {us_sync_id} must be json'}
            )
    else:
        errors[f"{action}_errors"].append(
            {"user": f'Value "language_style" for user {us_sync_id} is required'}
        )

    if device_id:
        if isinstance(device_id, str) and "DELETE" in device_id:
            data["device_id"] = device_id

    return data, errors


def validate_tours(
    action, data, user, errors, tr_sync_id, created_at, updated_at, museumtour_sync_id
):

    trsync_ids = []
    c_errors = validate_common_fields(
        "tour",
        data,
        action,
        o_model=UserTour,
        sync_ids=trsync_ids,
        entity_sync_id=tr_sync_id,
        created_at=created_at,
        updated_at=updated_at,
    )

    errors[f"{action}_errors"].extend(c_errors)

    if len(errors[f"{action}_errors"]) > 0:
        return None, errors

    if museumtour_sync_id:
        try:
            uuid_obj = uuid.UUID(museumtour_sync_id, version=4)
        except ValueError as e:
            errors.append(
                {
                    f"{entity_name}": f'Inappropriate "museum_tour sync id": {museumtour_sync_id} uuid for {entity_name} sync_id, {e.args}'
                }
            )
            return errors
    else:
        errors.append({f"{entity_name}": "Sync id for museum tour is required"})

    museum_tour = MuseumTour.objects.filter(sync_id=uuid_obj).first()
    if museum_tour:
        data["museum_tour"] = museum_tour
    else:
        errors.append(
            {
                f"{entity_name}": f"Inappropriate or absent museum tour sync_id: {uuid_obj}"
            }
        )

    data["user"] = user

    return data, errors
