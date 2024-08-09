import os
import shutil
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_text
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.dispatch.dispatcher import receiver
from django.contrib.gis import admin

def _delete(path):
    try:
        shutil.rmtree(path)
    except:
        print("Problem removing output task results directory,\n{pa}".format(pa=path))

# Create your models here.
class Area(models.Model):
    """Class for country object, data are imported automatically with
       general.mapping
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name=_("Area name"))
    user = models.ForeignKey(User, verbose_name=("User uploaded the area"),
                             on_delete=models.CASCADE)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        db_table = u"area"
        ordering = ["name"]
        verbose_name = _("area")
        verbose_name_plural = _("areas")
        unique_together = ['name', 'user']

    def __unicode__(self):
        return smart_text(self.name)

    def __str__(self):
        return self.__unicode__()

    def natural_key(self):
        return self.__unicode__()

    def clean(self):
        data = Area.objects.filter(user__exact=self.user).filter(name__iexact=self.name)
        if len(data) > 0:
            from django.core.exceptions import ValidationError
            raise ValidationError("The name is already existing")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Area, self).save(*args, **kwargs)

class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class TaskHistory(models.Model):
    """Class to maintain an history of the tasks"""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name=("User running the task"),
                             on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=("Area where task run"),
                             on_delete=models.CASCADE)
    task = models.CharField(max_length=150, verbose_name=_("Task id"))
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u"taskhistory"
        ordering = ["-data"]
        verbose_name = _("Task history")
        verbose_name_plural = _("Tasks history")

    def __unicode__(self):
        return smart_text("{us} - {ar}, {da}".format(us=self.user,
                                                     ar=self.area,
                                                     da=self.data))

    def __str__(self):
        return self.__unicode__()

    def natural_key(self):
        return self.__unicode__()

@receiver(models.signals.post_delete, sender=TaskHistory)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    task_outdir = os.path.join(settings.MEDIA_ROOT, instance.task)
    if os.path.exists(task_outdir):
        _delete(task_outdir)