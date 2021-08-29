
import math
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from users.models import User
from .models import Task, ASSIGNED, COMPLETED


def getUserIdByName(username):
    user = User.objects.filter(login=username).first()
    try:
        return user.id
    except AttributeError as e:
        return None


def getPointByCoords(lat, lon):
    try:
        point = Point(float(lon), float(lat))
    except ValueError as e:
        return None
    else:
        return point


def checkTasks2Execute(user_id, ch_point):
    buffer_width = settings.MAX_DISTANCE_METERS / 40000000. * 360. / math.cos(ch_point.y / 360. * math.pi)
    buffered_point = ch_point.buffer(buffer_width)

    tasks = Task.objects.filter(
        point__distance_lte=(ch_point, D(m=settings.MAX_DISTANCE_METERS)),
        point__intersects=buffered_point,
        status=ASSIGNED,
        assigned_user_id=user_id
    ).all()

    #tasks = Task.objects.filter(
    #    point__distance_lte=(ch_point, D(m=settings.MAX_DISTANCE_METERS))
    #).all()

    # from django.db import connection
    # print(connection.queries)

    # tasks = Task.objects.filter(point__dwithin=(ch_point, degrees)).all()
    # tasks = Task.objects.all()

    for task in tasks:
        task.status = COMPLETED
        task.datetime_in = datetime.now()
        task.save()
