from django.db import models
from django.contrib.gis.db import models as gis_models

from users.models import User

NEW_NOT_ASSIGNED = 1
ASSIGNED = 2
COMPLETED = 3
EXPIRED = 4
CANCELED = 5

STATUS_CHOICES = (
    (NEW_NOT_ASSIGNED, 'Новая не назначенная'),
    (ASSIGNED, 'Назначенная'),
    (COMPLETED, 'Выполненная'),
    (EXPIRED, 'Просроченная'),
    (CANCELED, 'Отменённая'),
)


class Task(models.Model):
    """Задание"""
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEW_NOT_ASSIGNED, verbose_name="Статус задания")
    datetime_created = models.DateTimeField(verbose_name="Дата-время создания", auto_now=True)
    datetime_changed = models.DateTimeField(verbose_name="Дата-время изменения", auto_now=True)
    # datetime_deadline = models.DateTimeField(verbose_name="Крайний срок выполнения", auto_now=False, null=True, blank=True)
    datetime_planned = models.DateTimeField(verbose_name="Планируемый срок выполнения", auto_now=False, null=True, blank=True)
    datetime_in = models.DateTimeField(verbose_name="Дата-время прибытия", auto_now=False, null=True, blank=True)
    datetime_out = models.DateTimeField(verbose_name="Дата-время выбытия", auto_now=False, null=True, blank=True)
    # point = gis_models.GeometryField(verbose_name="Точка на карте", null=True, blank=True)
    point = gis_models.PointField(verbose_name="Точка на карте", null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    place_descr = models.TextField("Место задания", null=True, blank=True)
    mission_descr = models.TextField("Цель задания", default=" ", null=True, blank=True)
    note = models.TextField("Комментарий", default=None)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Назначенный исполнитель", related_name='tasks')

    # def get_task_status_label(self):
    #     return TaskStatus(self.type).name.title()

    @property
    def lat(self):
        try: return self.point.y
        except: return None

    lat.fget.short_description = "Широта"

    @property
    def lon(self):
        try: return self.point.x
        except: return None

    lon.fget.short_description = "Долгота"

    class Meta:
        db_table = "tasks"
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Checkpoint(models.Model):
    """Контрольная точка"""
    id = models.AutoField(primary_key=True)
    datetime_created = models.DateTimeField(verbose_name="Дата-время создания",
        auto_now=True)
    point = gis_models.PointField(verbose_name="Точка на карте", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,
        blank=False, verbose_name="Исполнитель", related_name='checkpoint')

    @property
    def username(self):
        user = User.objects.get(login=self.user)
        return user

    @property
    def lat(self):
        try: return self.point.y
        except: return None

    lat.fget.short_description = "Широта"

    @property
    def lon(self):
        try: return self.point.x
        except: return None

    lon.fget.short_description = "Долгота"

    class Meta:
        db_table = "checkpoints"
        verbose_name = "Контрольная точка"
        verbose_name_plural = "Контрольные точки"
