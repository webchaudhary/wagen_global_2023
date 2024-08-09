from django.contrib.gis import admin
from .models import Area
from .models import TaskHistory
from .models import MyModelAdmin

# Register your models here.
# admin.site.register(Area, admin.OSMGeoAdmin)
# admin.site.register(TaskHistory, admin.ModelAdmin)
admin.site.register(Area, MyModelAdmin)
admin.site.register(TaskHistory, MyModelAdmin)

