from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.forms import AuthenticationForm, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import MultiPolygon
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django_celery_results.models import TaskResult
import os
import sys
from itertools import chain
from tempfile import NamedTemporaryFile
import json
import fiona
from fiona.crs import from_epsg
from fiona.transform import transform_geom
from .models import Area
from .models import TaskHistory
# from .tasks import simple_test
from .tasks import report_basin

from django.core.exceptions import RequestDataTooBig

# Create your views here.

#add KML support
if not 'KML' in fiona.supported_drivers.keys():
    fiona.drvsupport.supported_drivers['KML'] = 'rw'

def showmap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                #TODO
                print("Error")
            login(request, form.get_user())
        else:
            #TODO
            print("Form not valid")

    return render(request, "index.html", {"loginform": AuthenticationForm})

@login_required
@csrf_exempt
def addFeature(request):
    if request.method == "POST" and request.accepts('text/html'):
        name = request.POST.get('name')
        geomstr = request.POST.get('geom')
        if name and geomstr:
            geom = GEOSGeometry(geomstr)
            if type(geom) == Polygon:
                geom = MultiPolygon([geom])
            if type(geom) == MultiPolygon:
                try:
                    ar = Area(name=name, geom=geom, user=request.user)
                    ar.save()
                    return JsonResponse({"result": "Feature saved",
                                         "featid": ar.id},
                                        status=200)
                except Exception as e:
                    msg = ", ".join(e.messages)
                    return JsonResponse({"result": "Problem saving the feature: {}".format(msg)},
                                                   status=500)
            else:
                return JsonResponse({"result": "The geometry doesn't seem a polygon"},
                                              status=400)
        elif name and not geomstr:
            return JsonResponse({"result": "The geometry was not set"},
                                          status=400)
        else:
            return JsonResponse({"result": "The geometry and the name were not set"},
                                          status=400)
    else:
        return JsonResponse({"result": "Wrong request method"}, status=400)

@login_required
@csrf_exempt
def addLayer(request):
    try: 
        if request.method == "POST" and request.accepts('text/html'):
            namecolumn = request.POST.get('namecol')
            if not namecolumn:
                return JsonResponse({"result": "No name of column to select"},
                                    status=400)
            filestr = request.POST.get('file')
            if not filestr:
                return JsonResponse({"result": "No data to get the features"},
                                    status=400)
            crs4326 = from_epsg(4326)
            errors = []
            nfeats = 0
            with NamedTemporaryFile(delete=False) as tf:
                tf.write(filestr.encode())
            with fiona.open(tf.name) as source:
                if not namecolumn in source.schema['properties'].keys():
                    return JsonResponse({"result": "The column {} does not exists".format(namecolumn)},
                                            status=400)
                if source.schema['geometry'] not in ('Polygon', 'MultiPolygon', 'Multipolygon'):
                        return JsonResponse({"result": "The supported geometry type is Polygon only."
                                        "{} type is not supported".format(source.schema['geometry'])},
                                            status=400)

                for feat in source:
                    nfeats += 1
                    name = feat['properties'][namecolumn]
                    if not name:
                        errors.append("The feature with id {} has no value for "
                                    "attribute column {}".format(feat['id'],
                                                                namecolumn))
                    else:
                        strname = str(name)
                        if strname[0].isdigit():
                            name = settings.NAME_FORMAT.format(user=request.user,
                                                            val=name)
                            
                    if source.crs != crs4326:
                        geom = transform_geom(source.crs, crs4326, feat['geometry'])
                    else:
                        geom = feat['geometry']

                    geom_dict = {
                        "type": geom["type"],
                        "coordinates": geom["coordinates"]
                    }
                
                    geomstr = json.dumps(geom_dict) 

                    # if source.crs != crs4326:
                    #     geomstr = json.dumps(transform_geom(source.crs, crs4326, feat['geometry']))
                    # else:
                    #     geomstr = json.dumps(feat['geometry'])
                    geom = GEOSGeometry(geomstr)
                    if type(geom) == Polygon:
                        geom = MultiPolygon([geom])
                    if type(geom) == MultiPolygon:
                        try:
                            ar = Area(name=name, geom=geom, user=request.user)
                            ar.save()
                        except:
                            errors.append("Problem saving the feature with id {}".format(feat['id']))

                    else:
                        errors.append("The geometry for feature with id {} "
                                    "doesn't seem a polygon".format(feat['id']))
            os.remove(tf.name)
            if len(errors) == 0:
                return JsonResponse({"result": "All features saved correctly"},
                                    status=200)
            elif len(errors) == nfeats:
                return JsonResponse({"result": "All features were not saved",
                                    "errors": errors},
                                    status=400)
            else:
                return JsonResponse({"result": "Some features were not saved",
                                    "errors": errors},
                                    status=400)
        else:
            return JsonResponse({"result": "Wrong request method"}, status=400)
    except RequestDataTooBig:
        # the default max file size limit is 2.5MB in django if want to increase, set DATA_UPLOAD_MAX_MEMORY_SIZE in settings.py
        return JsonResponse({"result": "The file is too large. Please upload a file smaller than 2.5 MB."}, status=400)

@login_required
@csrf_exempt
def getReport(request):
    if request.method == "POST" and request.accepts('text/html'):
        areaid = request.POST.get('id')
        start = request.POST.get('start')
        end = request.POST.get('end')
        precip = request.POST.get('precip')
        et = request.POST.get('et')
        myarea = Area.objects.get(id__exact=areaid)
        current_user = request.user.email
        tsk = report_basin.delay(areaid, start, end, precip, et, current_user)
        tskhist = TaskHistory(user=request.user, area=myarea, task=tsk.id)
        tskhist.save()
        #"job id {}".format(tsk.id)
        return JsonResponse({"result": "Generating Report:"},
                            status=200)
    else:
        return JsonResponse({"result": "Wrong request method"}, status=400)

@login_required
def getAreas(request):
    samples = Area.objects.filter(user__exact=request.user)
    data = serialize('geojsonid', samples, use_natural_primary_keys=True,
                     use_natural_foreign_keys=True)
    return JsonResponse(json.loads(data))

@login_required
def getTasks(request):
    tasks = TaskHistory.objects.filter(user__exact=request.user)
    succededtasks = TaskResult.objects.filter(status="SUCCESS",
                              task_id__in=chain.from_iterable(tasks.values_list('task')))
    data = serialize('jsonid', tasks.filter(task__in=chain.from_iterable(succededtasks.values_list('task_id'))),
                     use_natural_primary_keys=True,
                     use_natural_foreign_keys=True)
    return JsonResponse({"data": json.loads(data)})

@login_required
def deleteTaskHistory(request, idd):
    task = TaskHistory.objects.get(id=idd)
    try:
        task.delete()
        return JsonResponse({"result": "Task id {} deleted".format(idd)},
                            status=200)
    except:
        return JsonResponse({"result": "Error deleting task id {}".format(idd)},
                            status=400)
