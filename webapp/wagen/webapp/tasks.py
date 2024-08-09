#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 06:44:31 2021

@author: lucadelu
@author: spareeth

"""
import os
import sys
import subprocess
import statistics
import shutil
from django.conf import settings
from celery import shared_task
from .functions import render_prod_html
from .functions import render_pdf_html
# from .functions import render_html
from .functions import render_pdf
from .functions import send_mail_attach
from .models import Area

os.environ.update({'GRASSBIN': settings.GRASS_BIN})
##export LD_LIBRARY_PATH=$(grass78 --config path)/lib
from grass_session import TmpSession
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import display as d
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.gis import *
import grass.script as grass
import grass.script.setup as gsetup

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.colors as colors
from sklearn.linear_model import Ridge
import geopandas as gdf
import pandas as pd
import pymannkendall as mk


# -----------------------------------
# Testing create report function
# -----------------------------------
# @shared_task(bind=True)
# def simple_test(self, area, start, stop, precip, et, current_user):
#     jobid = self.request.id
#     print(jobid)
#     #user1 = User.email
#     print(current_user)
#     #print(user)
#     #create a new directory for each task as set names
#     newdir = os.path.join(settings.MEDIA_ROOT, jobid)
#     LC_ESA = os.path.join(settings.DATA_DIR, 'worldcover_ESA')
#     os.mkdir(newdir)
#     outimg = os.path.join(newdir, "map.png")
#     outhist = os.path.join(newdir, "hist.svg")
#     #GRASS variables
#     os.environ.update(dict(GRASS_COMPRESS_NULLS='1',
#                            GRASS_COMPRESSOR='ZSTD',
#                            GRASS_OVERWRITE='1'))
#     # create a GRASS Session instance with a new location and mapset
#     user = TmpSession()
#     # user.open(gisdb=settings.GRASS_DB, location='job{}'.format(jobid),
#     #               create_opts='EPSG:4326')
#     user.open(gisdb=settings.GRASS_DB, location='wagen',
#         mapset='{}'.format(jobid), create_opts='EPSG:4326')

#     from grass.pygrass.raster import RasterRow
#     from grass.pygrass.gis.region import Region
#     from grass.pygrass.raster import raster2numpy
#     #get the area and create a new GRASS vector for this
#     #from grass.pygrass.vector import VectorTopo
#     #from grass.pygrass.vector import geometry as geo 
#     myarea = Area.objects.get(id=area)
#     #centroid = geo.Point(myarea.geom.centroid.x, myarea.geom.centroid.y)
#     #bound = geo.Line([myarea[0][0]])
#     vectname = "{na}_{job}".format(na=myarea.name.replace(' ', ''),
#                                    job=jobid.replace("-", "_"))
#     #new = VectorTopo(vectname)
#     #new.open('w')
#     #area = geo.Area(boundary=bound, centroid=centroid)
#     #new.write(area)
#     #new.close()
#     v.in_ogr(input="PG:dbname={db} host={add} port={po} user={us} "
#              "password={pwd}".format(db=settings.DATABASES['default']['NAME'],
#                                      add=settings.DATABASES['default']['HOST'],
#                                      po=settings.DATABASES['default']['PORT'],
#                                      us=settings.DATABASES['default']['USER'],
#                                      pwd=settings.DATABASES['default']['PASSWORD']),
#              output=vectname, where="id={}".format(area))
    
#     # execute some command inside PERMANENT
#     #g.mapsets(flags="l")
#     g.region(vector=vectname, res=0.01)
#     r.random_surface(flags="u", output="randomsurface")
#     d.mon(start='cairo', output=outhist)
#     d.histogram(map="randomsurface")
#     d.mon(stop="cairo")
#     r.mapcalc(expression="selected=if(randomsurface>100,randomsurface,null())")
#     d.mon(start="cairo", output=outimg)
#     d.rast(map="selected")
#     d.vect(map=vectname, fill_color="none", color="red", width=1)
#     d.mon(stop="cairo")
#     #deletebelow
#     ### Figure 1 - study area ###
#     g.mapsets(mapset="data_annual,data_monthly,grace", operation="add")
#     g.region(vector=vectname, res=0.005)
#     print("Hallo")
#     bbox = grass.parse_command('g.region', flags='pg')
#     print(bbox)
#     # compute area in ha of the studyarea
#     # Extract the extents
#     #spatial_extent=(28.9134,32.6882,29.9117,31.5939)
#     west = round(float(bbox['w']), 2)
#     east = round(float(bbox['e']), 2)
#     north = round(float(bbox['n']), 2)
#     south = round(float(bbox['s']), 2)
#     spatial_extent=(float(bbox['w']),float(bbox['e']),float(bbox['s']),float(bbox['n']))
#     ## Correcting Region() manually for the raster2numpy to work
#     print("hallo again")
#     #reg = Region().from_vect(vectname)
#     reg = Region()
#     reg.north = float(bbox['n'])
#     reg.south = float(bbox['s'])
#     reg.west = float(bbox['w'])
#     reg.east = float(bbox['e'])
#     reg.nsres = float(bbox['nsres'])
#     reg.ewres = float(bbox['ewres'])
#     reg.rows = int(bbox['rows'])
#     reg.cols = int(bbox['cols'])
#     reg.write()
#     reg.set_raster_region()
#     #g.mapset(mapset='job{}'.format(jobid))
#     #grass.mapcalc('{r} = {a}'.format(r=f'dem_alos1', a=f'dem_alos'))
#     print("hallo again2")
#     #g.mapset mapset=user1
#     #region = Region()
#     #region = reg.from_vect(vectname)
#     dem=raster2numpy("dem_alos", mapset="PERMANENT")
#     dem = np.ma.masked_where(dem == -2147483648, dem)
#     fig1 = os.path.join(newdir, "fig1.png")
#     fig, ax = plt.subplots(figsize = (12,8))
#     plt.imshow(dem, cmap='terrain', vmin=10, vmax=np.nanmax(dem), extent=spatial_extent)
#     scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
#     fig.gca().add_artist(scalebar)
#     df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
#     x, y, arrow_length = 1.1, 0.1, 0.1
#     ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
#             arrowprops=dict(facecolor='black', width=5, headwidth=15),
#             ha='center', va='center', fontsize=18, xycoords=ax.transAxes)
#     #ax.legend(bbox_to_anchor=(0.17,0.2))
#     plt.colorbar(shrink=0.50, label='Elevation[meters]')
#     plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=10)  # add axes label
#     plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=10)
#     plt.title('Study area', fontsize=10)
#     plt.savefig(fig1, bbox_inches='tight',pad_inches = 0, dpi=100)
#     #Delete till here
#     htmlfile = render_html(jobid, myarea)
#     pdffile = render_pdf(htmlfile, jobid)
#     print("dopo report")
#     sub="Your WA generator report"
#     mess="Your WA generator report is ready. You can access the report using this link: http://127.0.0.1:8000/media/{}/index.html".format(jobid)
#     to=current_user
#     attach=pdffile
#     plt.close('all')
#     #user.close()
#     send_mail_attach(sub, mess, to, attach)
#     return htmlfile, pdffile

@shared_task(bind=True)
def report_basin(self, area, start, stop, precip, et, current_user):
    print(start)
    print(stop)
    print(precip)
    print(et)
    print(current_user)
    timerange = range(int(start),int(stop)+1)
    years = list(timerange)
    years_str = [str(s) for s in years]
    jobid = self.request.id
    LC_ESA = os.path.join(settings.DATA_DIR, 'worldcover_ESA')
    #create a new directory for each task as set names
    newdir = os.path.join(settings.MEDIA_ROOT, jobid)
    os.mkdir(newdir)
    #GRASS variables
    os.environ.update(dict(GRASS_COMPRESS_NULLS='1',
                           GRASS_COMPRESSOR='ZSTD',
                           GRASS_OVERWRITE='1'))
    # create a GRASS Session instance with a new location and mapset
    user = TmpSession()
    #user.open(gisdb=settings.GRASS_DB, location='job{}'.format(jobid),
    #               create_opts='EPSG:4326')
    #user.open(gisdb=settings.GRASS_DB, location='wagen',
                   #mapset='job{}'.format(jobid), create_opts='EPSG:4326')
    user.open(gisdb=settings.GRASS_DB, location='wagen',
                   mapset='job{}'.format(jobid), create_opts='')
    #gisdb=settings.GRASS_DB
    #location='wagen'
    #mapset='job{}'.format(jobid)
    #session = gsetup.init(gisdb, location, mapset)

    from grass.pygrass.raster import RasterRow
    from grass.pygrass.gis.region import Region
    from grass.pygrass.raster import raster2numpy

    #get the area and create a new GRASS vector for this
    #from grass.pygrass.vector import VectorTopo
    #from grass.pygrass.vector import geometry as geo 
    myarea = Area.objects.get(id=area)
    #centroid = geo.Point(myarea.geom.centroid.x, myarea.geom.centroid.y)
    #bound = geo.Line([myarea[0][0]])
    #vectname = "{na}_{job}".format(na=myarea.name, job=jobid.replace("-", "_"))
    vectname = "{na}_{job}".format(na=myarea.name.replace(' ', '').replace("-", "_").replace("'", "_").replace("ô", "_").replace("&", "and").replace("(", "_").replace(")", "_"), job=jobid.replace("-", "_"))
    #new = VectorTopo(vectname)
    #new.open('w')
    #area = geo.Area(boundary=bound, centroid=centroid)
    #new.write(area)
    #new.close()
    v.in_ogr(input="PG:dbname={db} host={add} port={po} user={us} password={pwd}".format(db=settings.DATABASES['default']['NAME'], add=settings.DATABASES['default']['HOST'], po=settings.DATABASES['default']['PORT'],  us=settings.DATABASES['default']['USER'], pwd=settings.DATABASES['default']['PASSWORD']), output=vectname, where="id={}".format(area))

    out1 = os.path.join(newdir, "bound.gpkg")
    out2 = os.path.join(newdir, "bound.geojson")
    v.out_ogr(input=vectname, output=out1)
    v.out_ogr(input=vectname, output=out2, format='GeoJSON')
    cent = grass.parse_command('v.out.ascii', input=vectname, type='centroid', format='point', separator='comma')
    centkeys = list(cent.keys())
    centlist = [item for items in centkeys for item in items.split(",")]
    centX = float(centlist[0])
    centY = float(centlist[1])
    # execute some command inside PERMANENT
    # Add the data mapsets in search path
    g.mapsets(mapset="data_annual,data_monthly,data_monthly_ndvi,grace,cmip_ssp245,cmip_ssp585,pcp_era5,pcp_gpm,pcp_gsmap,pcp_persiann", operation="add")
    g.region(vector=vectname, res=0.0025)
    bbox = grass.parse_command('g.region', flags='pg')
    df = gdf.read_file(out1)
    # compute area in ha of the studyarea
    grass.run_command('v.to.db', map=vectname, option='area', type='boundary', units='kilometers', columns='area')
    area_col = grass.parse_command('v.univar', map=vectname, column='area', flags=('g'))
    studyarea = int(float(area_col['min']))
    # Extract the extents
    #spatial_extent=(28.9134,32.6882,29.9117,31.5939)
    west = round(float(bbox['w']), 2)
    east = round(float(bbox['e']), 2)
    north = round(float(bbox['n']), 2)
    south = round(float(bbox['s']), 2)
    spatial_extent=(float(bbox['w']),float(bbox['e']),float(bbox['s']),float(bbox['n']))
    ## Correcting Region() manually for the raster2numpy to work
    print("hallo again")
    #reg = Region().from_vect(vectname)
    reg = Region()
    reg.north = float(bbox['n'])
    reg.south = float(bbox['s'])
    reg.west = float(bbox['w'])
    reg.east = float(bbox['e'])
    reg.nsres = float(bbox['nsres'])
    reg.ewres = float(bbox['ewres'])
    reg.rows = int(bbox['rows'])
    reg.cols = int(bbox['cols'])
    reg.write()
    reg.set_raster_region()
    
    # Adding mask to study area
    # remaining figures/stats only on masked area
    r.mask(vector=vectname)
    # Extract the DEM stats
    grass.mapcalc('{r} = int({a} * 1.0)'.format(r=f'dem_studyarea', a=f'dem_alos'))    
    dem_stats = grass.parse_command('r.univar', map=f'dem_studyarea', flags='eg', percentile='2,98')
    p2 = float(dem_stats['percentile_2'])
    p98 = float(dem_stats['percentile_98'])
    dem_min = int(float(dem_stats['percentile_2']))
    dem_max = int(float(dem_stats['percentile_98']))
    
    ### Figure 1 - study area ###
    demtif = os.path.join(newdir, "DEM.tif")
    r.out_gdal(input='dem_studyarea', output=demtif)
    dem=raster2numpy("dem_studyarea", mapset='job{}'.format(jobid))
    dem = np.ma.masked_where(dem == -2147483648, dem)
    fig1 = os.path.join(newdir, "fig1.png")
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(dem, cmap='terrain', vmin=np.nanmin(dem), vmax=np.nanmax(dem), extent=spatial_extent)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    #df.boundary.plot(ax=ax, facecolor='none', edgecolor='k', label='Boundary');
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=18, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Elevation[meters]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=10)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=10)
    plt.title('Study area', fontsize=10)
    plt.savefig(fig1, bbox_inches='tight',pad_inches = 0, dpi=100)

    ### Prepare Landcover for study area
    ## Using copernicus LC or wapor LC below command
    ## Change as required
    if et == 'wapor2' or et == 'enset':
            patlc = 'LC_wapor_reclass_'
            lcmap = patlc + stop
            grass.mapcalc('{r} = {a}'.format(r=f'LC_studyarea1', a=lcmap))
            print('Using wapor LCC')
    else:
            grass.mapcalc('{r} = {a}'.format(r=f'LC_studyarea1', a=f'LC_copernicus_reclass'))
            print('Using Copernicus LCC')
    ## Using worldcover 10m ESA map
    #inlc = os.path.join(LC_ESA, "worldcover.vrt")
    #outlc = os.path.join(newdir, "LC_bbox.tif")
    #compress = 'COMPRESS=DEFLATE'
    #tiled = 'TILED=YES'
    #config1 = 'GDALWARP_IGNORE_BAD_CUTLINE'
    #config2 = 'YES'
    #srs='EPSG:4326'
    #res1 = 0.0025
    #command = "gdalwarp -cutline %s -crop_to_cutline %s %s -co %s -co %s --config %s %s -te %s %s %s %s -te_srs %s -tr %s %s" % (out2, inlc, outlc, compress, tiled, config1, config2, west, south, east, north, srs, res1, res1)
    #os.system(command)
    #r.in_gdal(input=outlc, output='LC_studyarea')
    #grass.mapcalc('{r} = int({a} * 1)'.format(r=f'LC_studyarea', a=f'LC_bbox'))
    #catfile = os.path.join(LC_ESA, "worldcover_category.csv")
    #colorfile = os.path.join(LC_ESA, "worldcover_colors.txt")
    #r.category(map='LC_studyarea', rules=catfile, separator='comma')
    #r.colors(map='LC_studyarea', rules=colorfile)
    ## Using worldcover 10m ESA map import ENDS here
    ##############################################
    ### Landcover statistics ###
    print('LC details starts here:')
    LCcsv = os.path.join(newdir, "LC.csv")
    LC_stats = grass.parse_command('r.stats',flags='napl',separator='comma',input='LC_studyarea1',output=LCcsv)
    LCdf = pd.read_csv(LCcsv, header=None, sep=',')
    LCdf_filt = LCdf.loc[LCdf[2] > 2500]
    LC_code = LCdf_filt[0].tolist()
    print(LC_code)
    LC_name = LCdf_filt[1].tolist()
    print(LC_name)
    LC_area = LCdf_filt[2].tolist()
    print(LC_area)
    LC_perc_str = LCdf_filt[3].tolist()
    print(LC_perc_str)
    # Update LC_study area removing the land cover types which are less than 10 pixels
    LCdf_filt1 = LCdf.loc[LCdf[2] < 2500]
    LC_code1 = LCdf_filt1[0].tolist()
    LC_code1_str=[str(item) for item in LC_code1]
    LC_code_mask=" ".join(LC_code1_str)
    print(f"LC to be masked are {LC_code_mask}")
    if not LC_code1_str:
            print('No classes to be ignored')
            grass.mapcalc('{r} = {a}'.format(r=f'LC_studyarea', a=f'LC_studyarea1'))
    else:
            r.mask(raster="LC_studyarea1", maskcats=LC_code_mask, flags="i")
            grass.mapcalc('{r} = {a}'.format(r=f'LC_studyarea', a=f'LC_studyarea1'))
    r.mask(vector=vectname)
    #LC_stats_keys = list(LC_stats.keys())
    #x = [item for items in LC_stats_keys for item in items.split(",")]
    #LC_code_str = x[0::4]
    #print(LC_code_str)
    #LC_name = x[1::4]
    #print(LC_name)
    #LC_area_str = x[2::4]
    #print(LC_area_str)
    #LC_perc_str = x[3::4]
    #print(LC_perc_str)
    #LC_code = [int(item) for item in LC_code_str]
    #LC_code_sort = sorted(LC_code)
    #LC_area = [float(item) for item in LC_area_str]
    LC_perc = [item.replace("%", "") for item in LC_perc_str]
    LC_perc_flt = [round(float(item), 1) for item in LC_perc]
    print(LC_perc_flt)
    LC_area_ha = [int(round(x/10000)) for x in LC_area]
    print(LC_area_ha)
    LC_area_sqkm = [int(round(x/100)) for x in LC_area_ha]
    print(LC_area_sqkm)
    ### Extract color codes from Landcover ###
    LC_color = grass.parse_command('r.what.color',input='LC_studyarea',value=LC_code,format='#%02x%02x%02x')
    LC_color_keys = list(LC_color.keys())
    LC_color_comma = [item.replace(": ", ",") for item in LC_color_keys]
    y = [item for items in LC_color_comma for item in items.split(",")]
    LC_color_hex = y[1::2]

    # Extract color codes second time for the pie chart of Landcover
    #LC_color1 = grass.parse_command('r.what.color',input='LC_studyarea',value=LC_code,format='#%02x%02x%02x')
    #LC_color1_keys = list(LC_color1.keys())
    #LC_color1_comma = [item.replace(": ", ",") for item in #LC_color1_keys]
    #y1 = [item for items in LC_color1_comma for item in items.split(",")]
    #LC_color1_hex = y1[1::2]
    
    ### Figure 2 - Landcover ###
    lc = os.path.join(newdir, "lc.png")
    lcpie = os.path.join(newdir, "pie.png")
    leg = os.path.join(newdir, "leg.png")
    lctif = os.path.join(newdir, "LC.tif")
    r.out_gdal(input='LC_studyarea', output=lctif)
    LC=raster2numpy("LC_studyarea", mapset='job{}'.format(jobid))
    LC = np.ma.masked_where(LC == -2147483648, LC)
    fig, ax = plt.subplots(figsize = (12,8))
    cmap = ListedColormap(LC_color_hex)
    print(LC_color_hex)
    print(LC_code)
    LC_code.insert(0, -1)
    LC_code1 = [x+1 for x in LC_code]
    norm = BoundaryNorm(LC_code1, cmap.N)
    plt.imshow(LC, cmap=cmap, extent=spatial_extent, norm=norm, interpolation='nearest', resample=True)
    #plt.imshow(LC, cmap=cmap, extent=spatial_extent, norm=norm)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.01, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Major Land cover types', fontsize=12)
    plt.savefig(lc, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    ### LC Pie Chart ###
    y = np.array(LC_perc_flt)
    x = LC_name
    LC_colors = LC_color_hex
    fig, ax = plt.subplots(figsize = (4,4))
    patches, texts = plt.pie(y, colors=LC_colors, startangle=90, radius=1.2, shadow = True)
    plt.savefig(lcpie, bbox_inches='tight',pad_inches = 0, dpi=100)
    labels = ['{0} - {1:1.1f} %'.format(i,j) for i,j in zip(x, y)]
    sort_legend = True
    if sort_legend:
            patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                            key=lambda x: x[2],
                            reverse=True))
    fig, ax = plt.subplots(figsize = (4,4))
    ax.axis('off')
    #plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.), fontsize=10)
    plt.legend(patches, labels, loc='center', fontsize=10, borderpad=0.2)
    plt.savefig(leg, bbox_inches='tight',pad_inches = 0, dpi=100)    
    ## Remove mask and set region to 500 m and reset mask
    r.mask(flags="r")
    g.region(vector=vectname, res=0.0025)
    r.mask(vector=vectname)

    ## FIGURE 3 - ETA plot ###
    etaplt = os.path.join(newdir, "eta.png")
    maps = [et + "_eta_y" + s for s in years_str]
    #maps=grass.list_grouped(type=['raster'], pattern="ssebop_eta_*")['data_annual']    
    r.series(input=maps, output='ETa_mean', method='average')
    if et == 'wapor2' or et == 'wapor3':
            grass.mapcalc('{r} = {a} * 0.1'.format(r=f'ETa_mean', a=f'ETa_mean'))
    else:
            print('No scaling for ETa required')
    etatif = os.path.join(newdir, "ETa.tif")
    r.out_gdal(input='ETa_mean', output=etatif)
    #print(etmaps)
    ETa=raster2numpy('ETa_mean', mapset='job{}'.format(jobid))
    ETa = np.ma.masked_where(ETa == -2147483648, ETa)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ETa, cmap='jet_r', vmin=10, vmax=np.nanmax(ETa),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='ETa [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual ETa ', fontsize=12)
    plt.savefig(etaplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    eta_basin = grass.parse_command('r.univar', map=f'ETa_mean', flags='g')
    mean_eta_basin = int(round(float(eta_basin['mean'])))

    ## FIGURE xx - ETr plot ###
    etrplt = os.path.join(newdir, "etr.png")
    #ssebop_etpa_y2016
    maps = ["ssebop_etpa_y" + s for s in years_str]
    #maps=grass.list_grouped(type=['raster'], pattern="ssebop_eta_*")['data_annual']    
    r.series(input=maps, output='ETr_mean', method='average')
    etrtif = os.path.join(newdir, "ETr.tif")
    r.out_gdal(input='ETr_mean', output=etrtif)
    #print(etmaps)
    ETr=raster2numpy('ETr_mean', mapset='job{}'.format(jobid))
    ETr = np.ma.masked_where(ETr == -2147483648, ETr)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ETr, cmap='jet_r', vmin=np.nanmin(ETr), vmax=np.nanmax(ETr),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='ETr [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual ETr ', fontsize=12)
    plt.savefig(etrplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    etr_basin = grass.parse_command('r.univar', map=f'ETr_mean', flags='g')
    mean_etr_basin = int(round(float(etr_basin['mean'])))

    ## FIGURE xx - NDVI plot ### - ndvi_annual_2012
    ndvimapplt = os.path.join(newdir, "ndvimap.png")
    maps = ["ndvi_annual_" + s for s in years_str]
    #maps=grass.list_grouped(type=['raster'], pattern="ssebop_eta_*")['data_annual']    
    r.series(input=maps, output='ndvi_mean1', method='average')
    grass.mapcalc('{r} = {a} * 0.0001'.format(r=f'ndvi_mean', a=f'ndvi_mean1'))
    ndvitif = os.path.join(newdir, "ndvi.tif")
    r.out_gdal(input='ndvi_mean', output=ndvitif)
    #print(etmaps)
    ndvimean=raster2numpy('ndvi_mean', mapset='job{}'.format(jobid))
    ndvimean = np.ma.masked_where(ndvimean == -2147483648, ndvimean)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ndvimean, cmap='summer_r', vmin=np.nanmin(ndvimean), vmax=np.nanmax(ndvimean),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='NDVI]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual max NDVI ', fontsize=12)
    plt.savefig(ndvimapplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    ## FIGURE XX - ETA anomaly plot ###
    etanoplt = os.path.join(newdir, "etanomaly.png")
    #maps=grass.list_grouped(type=['raster'], pattern="ssebop_etano_y*")['data_annual']
    #r.series(input=maps, output='ETano_mean', method='average')
    #print(etmaps)
    pat = "ssebop_etano_y"
    etanomap = pat + stop
    etanotif = os.path.join(newdir, "ETano.tif")
    grass.mapcalc('{r} = {a}'.format(r=f'etanomap', a=etanomap))
    r.out_gdal(input='etanomap', output=etanotif)
    ETano=raster2numpy('etanomap', mapset='job{}'.format(jobid))
    #ETano=raster2numpy(etanomap, mapset='data_annual')
    ETano = np.ma.masked_where(ETano == -2147483648, ETano)
    fig, ax = plt.subplots(figsize = (12,8))
    #divnorm=colors.TwoSlopeNorm(vmin=10, vcenter=100 vmax=np.nanmax(ETano))
    #plt.imshow(ETano, cmap='seismic_r', extent=spatial_extent, norm=divnorm, interpolation='none', resample=False)
    plt.imshow(ETano, cmap='YlOrRd', vmin=np.nanmin(ETano), vmax=np.nanmax(ETano),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Anomaly [%]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual ETa anomaly ', fontsize=12)
    plt.savefig(etanoplt, bbox_inches='tight',pad_inches = 0, dpi=100)

    ## FIGURE 4 PCP plot###
    pcpplt = os.path.join(newdir, "pcp.png")
    maps = ["pcpa_" + precip + "_" + s for s in years_str]
    #maps=grass.list_grouped(type=['raster'], pattern="chirps_precip*")['data_annual']
    r.series(input=maps, output='pcp_mean', method='average')
    pcptif = os.path.join(newdir, "PCP.tif")
    r.out_gdal(input='pcp_mean', output=pcptif)
    #print(etmaps)
    PCP=raster2numpy("pcp_mean", mapset='job{}'.format(jobid))
    PCP = np.ma.masked_where(PCP == -2147483648, PCP)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(PCP, cmap='Blues', vmin=np.nanmin(PCP), vmax=np.nanmax(PCP),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Precipitation [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual Precipitation', fontsize=12)
    plt.savefig(pcpplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    pcp_basin = grass.parse_command('r.univar', map=f'pcp_mean', flags='g')
    mean_pcp_basin = "%.0f" % round(float(pcp_basin['mean']), 1)
    
    ## FIGURE 5 PCP-ETa plot ###
    pminet = os.path.join(newdir, "pminuset.png")
    grass.mapcalc('{r} = {a} - {b}'.format(r=f'pminuset', a=f'pcp_mean', b=f'ETa_mean'))
    #print(etmaps)
    pminusettif = os.path.join(newdir, "PminusET.tif")
    r.out_gdal(input='pminuset', output=pminusettif)
    pminuset=raster2numpy("pminuset", mapset='job{}'.format(jobid))
    pminuset = np.ma.masked_where(pminuset == -2147483648, pminuset)
    fig, ax = plt.subplots(figsize = (12,8))
    
    if np.nanmax(pminuset) > 0:
           print('first condition for divnorm')
           divnorm=colors.TwoSlopeNorm(vmin=np.nanmin(pminuset), vcenter=0, vmax=np.nanmax(pminuset))
    else:
           print('second condition for divnorm')
           divnorm=colors.TwoSlopeNorm(vmin=np.nanmin(pminuset), vcenter=np.nanmedian(pminuset), vmax=np.nanmax(pminuset))   
    plt.imshow(pminuset, cmap='RdYlBu', extent=spatial_extent, norm=divnorm, interpolation='none', resample=False)
    #plt.imshow(pminuset, cmap='RdYlBu', vmin=-1000, vmax=np.nanmax(pminuset),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='PCP - ETa [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('PCP - ETa', fontsize=12)
    plt.savefig(pminet, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    r.mask(raster="LC_studyarea", maskcats='40')
    ## Saving table with Bio, ET and WP annual
    if et == 'wapor2' or et == 'enset':
            mapsdmp = [et + "_tbp_" + s for s in years_str]
    else:
            mapsdmp = ["dmp_annual_" + s for s in years_str]
    dmp=[]
    for i in mapsdmp:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']),0)
            dmp.append(mean)
    print(dmp)
    if et == 'wapor2':
            etmaps = ["wapor2_eta_y" + s for s in years_str]
    elif et == 'wapor3':
            etmaps = ["wapor3_eta_y" + s for s in years_str]
    elif et == 'enset':
            etmaps = ["enset_eta_y" + s for s in years_str]
    elif et == 'ensetglobal':
            etmaps = ["ensetglobal_eta_y" + s for s in years_str]
    else:
            etmaps = ["ssebop_eta_y" + s for s in years_str]
    etag=[]
    for i in etmaps:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            #mean = int(round(float(stats['mean'])))
            mean = round(float(stats['mean']),0)
            etag.append(mean)
    print(etag)
    WPbAnnual = [round(float(a / (b * 10)), 2) for a, b in zip(dmp, etag)]
    df_wpb = pd.DataFrame({'TBP(Kg/ha)': dmp, 'ETa(mm/year)': etag, 'WPb(Kg/m3)': WPbAnnual}, index=years)
    df_wpb.loc['Average'] = round(df_wpb.mean(), 1)
    dfwpb = os.path.join(newdir, "wpbtable.csv")
    df_wpb.to_csv(dfwpb, index = True)
    
    ## FIGURE 6 DMP plot ###
    dmpfig = os.path.join(newdir, "dmp.png")
    dmptif = os.path.join(newdir, "DMP.tif")
    #maps=grass.list_grouped(type=['raster'], pattern="dmp_annual*")['data_annual']
    r.series(input=mapsdmp, output='dmp_mean', method='average')
    r.out_gdal(input='dmp_mean', output=dmptif)
    dmp=raster2numpy("dmp_mean", mapset='job{}'.format(jobid))
    dmp = np.ma.masked_where(dmp == -2147483648, dmp)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(dmp, cmap='BrBG', vmin=1000, vmax=np.nanmax(dmp),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='DMP [Kg/ha]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Total Biomass Production (TBP)', fontsize=12)
    plt.savefig(dmpfig, bbox_inches='tight',pad_inches = 0, dpi=100)    
    dmp_basin = grass.parse_command('r.univar', map=f'dmp_mean', flags='g')
    #mean_dmp_basin = round(float(dmp_basin['mean']), 0)    

    #ETdivP_ssebop_2013_idw
    ##Splitting ETa int ETb and ETg using EK method
    maps = ["ETdivP_ssebop_" + s for s in years_str]
    r.series(input=maps, output='ETdivP_mean1', method='average')
    grass.mapcalc('{r} = if({a} > 0.85, 0.85, {a})'.format(r=f'ETdivP_mean', a=f'ETdivP_mean1'))
    grass.mapcalc('{r} = {a} * {b}'.format(r=f'ETg_mean', a=f'ETdivP_mean', b=f'pcp_mean'))
    grass.mapcalc('{r} = {a} - {b}'.format(r=f'ETb_mean', a=f'ETa_mean', b=f'ETg_mean'))

    """
    ### SPLITTING ETa into ETg and ETb starts here.
    ### Create Irrigated and Rainfed maps ###
    #grass.mapcalc('{r} = if({a} == 40 && {b} == 11, 1, null())'.format(r=f'cropland_irrigated', a=f'LC_studyarea', b=f'LC_globcover'))
    grass.mapcalc('{r} = if({a} == 40 && {b} == 14, 1, null())'.format(r=f'cropland_rainfed', a=f'LC_studyarea', b=f'LC_globcover'))
    r.mask(raster="cropland_rainfed")
    eta_rf = grass.parse_command('r.univar', map=f'ETa_mean', flags='g')
    thrf = round(float(eta_rf['mean']), 0)
    print(f"Rainfed threshold is {thrf}")
    r.mask(raster="LC_studyarea", maskcats='40')
    grass.mapcalc('{r} = {a} * 0.8'.format(r=f'pcp_thrf', a=f'pcp_mean'))
    #grass.mapcalc('{r} = {a} - {b}'.format(r=f'ETb_irrig1', a=f'ETa_mean', b=thrf))
    grass.mapcalc('{r} = if({b} < {c}, {a} - {b}, {a} - {c})'.format(r=f'ETb_irrig1', a=f'ETa_mean', b=f'pcp_thrf', c=thrf))
    #grass.mapcalc('{r} = min({a}, {b} * 0.8)'.format(r=f'ETg_mean', a=f'ETg_irrig', b=f'pcp_mean'))
    grass.mapcalc('{r} = if({a} < 0, 0, {a})'.format(r=f'ETb_irrig', a=f'ETb_irrig1'))
    grass.mapcalc('{r} = {b} - {a}'.format(r=f'ETg_mean', a=f'ETb_irrig', b=f'ETa_mean'))
    #grass.mapcalc('{r} = if({a} > {b} * 0.8, {b} * 0.8, {a})'.format(r=f'ETg_mean', a=f'ETg_irrig', b=f'pcp_mean'))
    r.mask(raster="LC_studyarea", maskcats='80')
    grass.mapcalc('{r} = {b} - {a}'.format(r=f'ETb_water', a=f'pcp_mean', b=f'ETa_mean'))
    r.mask(flags="r")
    r.mask(raster="LC_studyarea", maskcats='40')
    r.patch(input=["ETb_irrig", "ETb_water"], output="ETb_mean")
    """
    r.mask(raster="LC_studyarea", maskcats='40')
    ## RWD map ###
    eta_irri = grass.parse_command('r.univar', map=f'ETa_mean', flags='ge', percentile='98')
    thrwd = round(float(eta_irri['percentile_98']), 0)
    grass.mapcalc('{r} = 1 - ({a} / {b})'.format(r=f'rwd1', a=f'ETa_mean', b=thrwd))
    grass.mapcalc('{r} = if({a} < 0, null(), {a})'.format(r=f'rwd', a=f'rwd1'))
    #mean_eta_irri = round(float(eta_irri['mean']), 0)
    ## WPdmp map ##
    grass.mapcalc('{r} = {a} / ({b} * 10)'.format(r=f'WPdmp', b=f'ETa_mean', a='dmp_mean'))
    #pcp_irri = grass.parse_command('r.univar', map=f'pcp_mean', flags='ge')
    #mean_pcp_irri = round(float(pcp_irri['mean']), 0)
    #dmp_irri = grass.parse_command('r.univar', map=f'dmp_mean', flags='ge')
    #mean_dmp_irri = round(float(dmp_irri['mean']), 0)
    #wp_irri = grass.parse_command('r.univar', map=f'WPdmp', flags='ge')
    #mean_wp_irri = round(float(wp_irri['mean']), 0)
    r.mask(flags="r")
    g.region(vector=vectname, res=0.005)
    r.mask(raster="LC_studyarea", maskcats='40')
    grass.mapcalc('{r} = {a}'.format(r=f'bws', a='BlueWS'))
    grass.mapcalc('{r} = {a}'.format(r=f'gws', a='GreenWS'))
    grass.mapcalc('{r} = {a}'.format(r=f'ews', a='EconomicWS'))
    r.mask(flags="r")
    g.region(vector=vectname, res=0.0025)

    ### FIGURE 7  ETblue plot ###
    etbplt = os.path.join(newdir, "etb.png")
    etgplt = os.path.join(newdir, "etg.png")
    ETb=raster2numpy('ETb_mean', mapset='job{}'.format(jobid))
    ETb = np.ma.masked_where(ETb == -2147483648, ETb)
    ETg=raster2numpy('ETg_mean', mapset='job{}'.format(jobid))
    ETg = np.ma.masked_where(ETg == -2147483648, ETg)
    etbtif = os.path.join(newdir, "ETb.tif")
    r.out_gdal(input='ETb_mean', output=etbtif)
    etgtif = os.path.join(newdir, "ETg.tif")
    r.out_gdal(input='ETg_mean', output=etgtif)
    et_max = np.nanpercentile(np.maximum(ETb, ETg), 99)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ETb, cmap='jet_r', vmin=0, vmax=et_max, extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='ETblue [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual ET blue ', fontsize=12)
    plt.savefig(etbplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    etb_basin = grass.parse_command('r.univar', map=f'ETb_mean', flags='g')
    mean_etb_basin = int(round(float(etb_basin['mean'])))
    
    ### FIGURE 8  ETgreen plot ###
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ETg, cmap='jet_r', vmin=0, vmax=et_max, extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='ET green [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual ET green', fontsize=12)
    plt.savefig(etgplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    etg_basin = grass.parse_command('r.univar', map=f'ETg_mean', flags='g')
    mean_etg_basin = int(round(float(etg_basin['mean'])))
    

    # Partitioning E&T - Temporary
    #r.mask(raster="LC_studyarea", maskcats='40')
    #grass.mapcalc('{r} = {a} * 0.4'.format(r=f'E_irrig', a=f'ETa_mean'))
    #grass.mapcalc('{r} = {a} * 0.6'.format(r=f'T_irrig', a=f'ETa_mean'))
    #r.mask(raster="LC_studyarea", maskcats='80')
    #grass.mapcalc('{r} = {a}'.format(r=f'E_water', a=f'ETa_mean'))
    #grass.mapcalc('{r} = 0'.format(r=f'T_water'))
    #r.mask(raster="LC_studyarea", maskcats='80 40', flags="i")
    #grass.mapcalc('{r} = {a} * 0.6'.format(r=f'E_others', a=f'ETa_mean'))
    #grass.mapcalc('{r} = {a} * 0.4'.format(r=f'T_others', a=f'ETa_mean'))
    #r.mask(vector=vectname)
    #r.patch(input=["E_irrig", "E_others", "E_water"], output="E_mean")
    #r.patch(input=["T_irrig", "T_others", "T_water"], output="T_mean")
    eamaps = ["Ea_" + et + "_annual_" + s for s in years_str]
    tamaps = ["Ta_" + et + "_annual_" + s for s in years_str]
    #maps=grass.list_grouped(type=['raster'], pattern="dmp_annual*")['data_annual']
    r.mask(vector=vectname)
    r.series(input=tamaps, output='T_mean_raw', method='average')
    r.series(input=eamaps, output='E_mean_raw', method='average')
    if et == 'wapor2' or et == 'wapor3':
            grass.mapcalc('{r} = {a} * 0.1'.format(r=f'T_mean_raw', a=f'T_mean_raw'))
            grass.mapcalc('{r} = {a} * 0.1'.format(r=f'E_mean_raw', a=f'E_mean_raw'))
    else:
            print('No scaling for Ea and Ta required')

    ## Filter Ea and Ta for negative values and 99 percentile
    grass.mapcalc('{r} = if({a} < 0, 0, {a})'.format(r=f'T_mean_raw1', a=f'T_mean_raw'))
    grass.mapcalc('{r} = if({a} < 0, 0, {a})'.format(r=f'E_mean_raw1', a=f'E_mean_raw'))
    thta1 = grass.parse_command('r.univar', map=f'T_mean_raw1', flags='ge', percentile='99')
    thta = int(round(float(thta1['percentile_99'])))
    grass.mapcalc('{r} = if({a} > {b}, {b}, {a})'.format(r=f'T_mean', a=f'T_mean_raw1', b=thta))
    thea1 = grass.parse_command('r.univar', map=f'E_mean_raw1', flags='ge', percentile='99')
    thea = int(round(float(thea1['percentile_99'])))
    grass.mapcalc('{r} = if({a} > {b}, {b}, {a})'.format(r=f'E_mean', a=f'E_mean_raw1', b=thea))
    eatif = os.path.join(newdir, "Ea.tif")
    r.out_gdal(input='E_mean', output=eatif)
    tatif = os.path.join(newdir, "Ta.tif")
    r.out_gdal(input='T_mean', output=tatif)
    r.mask(raster="LC_studyarea", maskcats='40')
    grass.mapcalc('{r} = {a}'.format(r=f'E_mean_crop', a=f'E_mean'))
    grass.mapcalc('{r} = {a}'.format(r=f'T_mean_crop', a=f'T_mean'))
    Ea=raster2numpy('E_mean_crop', mapset='job{}'.format(jobid))
    Ea = np.ma.masked_where(Ea == -2147483648, Ea)
    Ta=raster2numpy('T_mean_crop', mapset='job{}'.format(jobid))
    Ta = np.ma.masked_where(Ta == -2147483648, Ta)
    e_t_max = np.nanpercentile(np.maximum(Ea, Ta), 99)
    taplt = os.path.join(newdir, "ta.png")
    eaplt = os.path.join(newdir, "ea.png")
    #print(etmaps)

    ## FIGURE XX - Ea plot ###
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(Ea, cmap='jet_r', vmin=0, vmax=e_t_max,extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Ea [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual Ea ', fontsize=12)
    plt.savefig(eaplt, bbox_inches='tight',pad_inches = 0, dpi=100)

    ## FIGURE XX - Ta plot ###
    #print(etmaps)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(Ta, cmap='jet_r', vmin=0, vmax=e_t_max,extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Ta [mm/year]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual Ta ', fontsize=12)
    plt.savefig(taplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    ### FIGURE 9 Wpdmp plot ###
    wpplt = os.path.join(newdir, "wpdmp.png")
    wptif = os.path.join(newdir, "WPDMP.tif")
    r.out_gdal(input='WPdmp', output=wptif)    
    WPdmp=raster2numpy('WPdmp', mapset='job{}'.format(jobid))
    WPdmp = np.ma.masked_where(WPdmp == -2147483648, WPdmp)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(WPdmp, cmap='RdYlGn', vmin=0, vmax=np.nanpercentile(WPdmp, 95),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label=' Water Productivity [Kg/m3]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Annual Water Productivity', fontsize=12)
    plt.savefig(wpplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    ### FIGURE 10 RWD plot ###
    rwdplt = os.path.join(newdir, "rwd.png")
    rwdtif = os.path.join(newdir, "WDI.tif")
    r.out_gdal(input='rwd', output=rwdtif)
    rwd=raster2numpy('rwd', mapset='job{}'.format(jobid))
    rwd = np.ma.masked_where(rwd == -2147483648, rwd)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(rwd, cmap='RdBu_r', vmin=0, vmax=np.nanpercentile(rwd, 99),extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='WDI [%]')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Water Deficit Index', fontsize=12)
    plt.savefig(rwdplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    ### FIGURE 11 BWS plot ###
    bwsplt = os.path.join(newdir, "bws.png")
    bwstif = os.path.join(newdir, "BWS.tif")
    r.out_gdal(input='bws', output=bwstif)
    bws=raster2numpy('bws', mapset='job{}'.format(jobid))
    bws = np.ma.masked_where(bws == -2147483648, bws)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(bws, cmap='YlOrRd', vmin=0, vmax=12,extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Number of months')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Blue Water Scarcity', fontsize=12)
    plt.savefig(bwsplt, bbox_inches='tight',pad_inches = 0, dpi=100)

    ### FIGURE 12 GWS plot ###
    gwsplt = os.path.join(newdir, "gws.png")
    gwstif = os.path.join(newdir, "GWS.tif")
    r.out_gdal(input='gws', output=gwstif)
    gws=raster2numpy('gws', mapset='job{}'.format(jobid))
    gws = np.ma.masked_where(gws == -2147483648, gws)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(gws, cmap='winter', vmin=0, vmax=12,extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Number of months')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Green Water Scarcity', fontsize=12)
    plt.savefig(gwsplt, bbox_inches='tight',pad_inches = 0, dpi=100)

    ### FIGURE 13 EWS plot ###
    ewsplt = os.path.join(newdir, "ews.png")
    ewstif = os.path.join(newdir, "EWS.tif")
    r.out_gdal(input='ews', output=ewstif)
    ews=raster2numpy('ews', mapset='job{}'.format(jobid))
    ews = np.ma.masked_where(ews == -2147483648, ews)
    fig, ax = plt.subplots(figsize = (12,8))
    plt.imshow(ews, cmap='cool', vmin=0, vmax=12,extent=spatial_extent, interpolation='none', resample=False)
    scalebar = ScaleBar(100, 'km', box_color='w', box_alpha=0.7, location='lower left') # 1 pixel = 0.2 meter
    fig.gca().add_artist(scalebar)
    df.boundary.plot(ax=ax, facecolor='none', edgecolor='k');
    x, y, arrow_length = 1.1, 0.1, 0.1
    ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20, xycoords=ax.transAxes)
    #ax.legend(bbox_to_anchor=(0.17,0.2))
    plt.colorbar(shrink=0.50, label='Number of months')
    plt.xlabel('Longitude ($^{\circ}$ East)', fontsize=12)  # add axes label
    plt.ylabel('Latitude ($^{\circ}$ North)', fontsize=12)
    plt.title('Economic Water Scarcity', fontsize=12)
    plt.savefig(ewsplt, bbox_inches='tight',pad_inches = 0, dpi=100)
    
    r.mask(flags="r")
    r.mask(vector=vectname)
    ### Bar plots - land use versus ETa, PCP ###
    
    lc_eta_stats = grass.parse_command('r.univar', map=f'ETa_mean', zones=f'LC_studyarea', flags='gt')
    lc_etr_stats = grass.parse_command('r.univar', map=f'ETr_mean', zones=f'LC_studyarea', flags='gt')
    lc_pcp_stats = grass.parse_command('r.univar', map=f'pcp_mean', zones=f'LC_studyarea', flags='gt')
    lc_ea_stats = grass.parse_command('r.univar', map=f'E_mean', zones=f'LC_studyarea', flags='gt')
    lc_ta_stats = grass.parse_command('r.univar', map=f'T_mean', zones=f'LC_studyarea', flags='gt')
    #lc_etg_stats = grass.parse_command('r.univar', map=f'ETg_mean', zones=f'LC_studyarea', flags='gt')
    #lc_etb_stats = grass.parse_command('r.univar', map=f'ETb_mean', zones=f'LC_studyarea', flags='gt')
    neta = list(lc_eta_stats.keys())
    netr = list(lc_etr_stats.keys())
    npcp = list(lc_pcp_stats.keys())
    nea = list(lc_ea_stats.keys())
    nta = list(lc_ta_stats.keys())
    #netg = list(lc_etg_stats.keys())
    #netb = list(lc_etb_stats.keys())
    #  d=["%.0f" % round(float(item), 0) for item in a]
    yeta = [item for items in neta for item in items.split("|")]
    lc_eta_str = yeta[15::14]
    #lc_eta_mean=["%.0f" % round(float(item), 0) for item in yeta[21::14]]
    lc_eta_mean = [round(float(item),0) for item in yeta[21::14]]
    yetr = [item for items in netr for item in items.split("|")]
    lc_etr_mean = [round(float(item),0) for item in yetr[21::14]]
    ypcp = [item for items in npcp for item in items.split("|")]
    #lc_pcp_mean=["%.0f" % round(float(item), 0) for item in ypcp[21::14]]
    lc_pcp_mean = [round(float(item), 1) for item in ypcp[21::14]]
    lc_pcp_mean_str = ["%.0f" % round(float(item), 1) for item in lc_pcp_mean]
    print(f"PCP mean are {lc_pcp_mean}")
    #yea = [item for items in nea for item in items.split("|")]
    #lc_ea_mean = [int(round(float(item))) for item in yea[21::14]]
    #lc_ea_mean = yea[21::14]
    print(f"LC names are {lc_eta_str}")
    #print(f"Annual Ea LC stats {lc_ea_mean}")
    #yta = [item for items in nta for item in items.split("|")]
    #lc_ta_mean = [int(round(float(item))) for item in yta[21::14]]
    #lc_ta_mean = yta[21::14]
    #print(f"Annual Ea LC stats {lc_ta_mean}")
    #yetg = [item for items in netg for item in items.split("|")]
    #lc_etg_mean = [int(round(float(item))) for item in yetg[21::14]]
    #yetb = [item for items in netb for item in items.split("|")]
    #lc_etb_mean = [int(round(float(item))) for item in yetb[21::14]]

    lcbar = os.path.join(newdir, "lcbar.png")
    #x = np.arange(len(lc_eta_str))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    df1 = pd.DataFrame({'ETa': lc_eta_mean, 'PCP': lc_pcp_mean, 'Area': LC_area_sqkm}, index=lc_eta_str)
    df2 = df1.sort_values(by = ['Area'], ascending=False)
    ax = df2.plot.barh(y = ['ETa', 'PCP'], color=['seagreen', 'dodgerblue'])
    ax.invert_yaxis()
    ax.set_title('Annual ETa/PCP per Landcover')
    ax.set_xlabel('mm/year')
    plt.savefig(lcbar, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    ### Bar plot - multiple years eta stats in one bar graph
    eta_2010 = grass.parse_command('r.univar', map=f'{et}_eta_y2010', zones=f'LC_studyarea', flags='gt')
    eta_2011 = grass.parse_command('r.univar', map=f'{et}_eta_y2011', zones=f'LC_studyarea', flags='gt')
    eta_2012 = grass.parse_command('r.univar', map=f'{et}_eta_y2012', zones=f'LC_studyarea', flags='gt')
    eta_2013 = grass.parse_command('r.univar', map=f'{et}_eta_y2013', zones=f'LC_studyarea', flags='gt')
    eta_2014 = grass.parse_command('r.univar', map=f'{et}_eta_y2014', zones=f'LC_studyarea', flags='gt')
    eta_2015 = grass.parse_command('r.univar', map=f'{et}_eta_y2015', zones=f'LC_studyarea', flags='gt')
    eta_2016 = grass.parse_command('r.univar', map=f'{et}_eta_y2016', zones=f'LC_studyarea', flags='gt')
    eta_2017 = grass.parse_command('r.univar', map=f'{et}_eta_y2017', zones=f'LC_studyarea', flags='gt')
    eta_2018 = grass.parse_command('r.univar', map=f'{et}_eta_y2018', zones=f'LC_studyarea', flags='gt')
    eta_2019 = grass.parse_command('r.univar', map=f'{et}_eta_y2019', zones=f'LC_studyarea', flags='gt')
    eta_2020 = grass.parse_command('r.univar', map=f'{et}_eta_y2020', zones=f'LC_studyarea', flags='gt')
    eta_2021 = grass.parse_command('r.univar', map=f'{et}_eta_y2021', zones=f'LC_studyarea', flags='gt')
    eta_2022 = grass.parse_command('r.univar', map=f'{et}_eta_y2022', zones=f'LC_studyarea', flags='gt')
    eta_2023 = grass.parse_command('r.univar', map=f'{et}_eta_y2023', zones=f'LC_studyarea', flags='gt')
    neta2010 = list(eta_2010.keys())
    neta2011 = list(eta_2011.keys())
    neta2012 = list(eta_2012.keys())
    neta2013 = list(eta_2013.keys())
    neta2014 = list(eta_2014.keys())
    neta2015 = list(eta_2015.keys())
    neta2016 = list(eta_2016.keys())
    neta2017 = list(eta_2017.keys())
    neta2018 = list(eta_2018.keys())
    neta2019 = list(eta_2019.keys())
    neta2020 = list(eta_2020.keys())
    neta2021 = list(eta_2021.keys())
    neta2022 = list(eta_2022.keys())
    neta2023 = list(eta_2023.keys())
    yeta2010 = [item for items in neta2010 for item in items.split("|")]
    yeta2011 = [item for items in neta2011 for item in items.split("|")]
    yeta2012 = [item for items in neta2012 for item in items.split("|")]
    yeta2013 = [item for items in neta2013 for item in items.split("|")]
    yeta2014 = [item for items in neta2014 for item in items.split("|")]
    yeta2015 = [item for items in neta2015 for item in items.split("|")]
    yeta2016 = [item for items in neta2016 for item in items.split("|")]
    yeta2017 = [item for items in neta2017 for item in items.split("|")]
    yeta2018 = [item for items in neta2018 for item in items.split("|")]
    yeta2019 = [item for items in neta2019 for item in items.split("|")]
    yeta2020 = [item for items in neta2020 for item in items.split("|")]
    yeta2021 = [item for items in neta2021 for item in items.split("|")]
    yeta2022 = [item for items in neta2022 for item in items.split("|")]
    yeta2023 = [item for items in neta2023 for item in items.split("|")]
    lc_eta_str = yeta2020[15::14]
    lc_eta_2010 = [round(float(item),0) for item in yeta2010[21::14]]
    lc_eta_2011 = [round(float(item),0) for item in yeta2011[21::14]]
    lc_eta_2012 = [round(float(item),0) for item in yeta2012[21::14]]
    lc_eta_2013 = [round(float(item),0) for item in yeta2013[21::14]]
    lc_eta_2014 = [round(float(item),0) for item in yeta2014[21::14]]
    lc_eta_2015 = [round(float(item),0) for item in yeta2015[21::14]]
    lc_eta_2016 = [round(float(item),0) for item in yeta2016[21::14]]
    lc_eta_2017 = [round(float(item),0) for item in yeta2017[21::14]]
    lc_eta_2018 = [round(float(item),0) for item in yeta2018[21::14]]
    lc_eta_2019 = [round(float(item),0) for item in yeta2019[21::14]]
    lc_eta_2020 = [round(float(item),0) for item in yeta2020[21::14]]
    lc_eta_2021 = [round(float(item),0) for item in yeta2021[21::14]]
    lc_eta_2022 = [round(float(item),0) for item in yeta2022[21::14]]
    lc_eta_2023 = [round(float(item),0) for item in yeta2023[21::14]]
    lcbaret = os.path.join(newdir, "lcbaret.png")
    #x = np.arange(len(lc_eta_str))  # the label locations
    #width = 0.35  # the width of the bars
    fig, ax = plt.subplots(figsize=(40,10))
    df = pd.DataFrame({'2010': lc_eta_2010, '2011': lc_eta_2011, '2012': lc_eta_2012, '2013': lc_eta_2013, '2014': lc_eta_2014, '2015': lc_eta_2015, '2016': lc_eta_2016, '2017': lc_eta_2017, '2018': lc_eta_2018, '2019': lc_eta_2019, '2020': lc_eta_2020}, index=lc_eta_str)
    if et == 'wapor2' or et == 'wapor3':
            for col in df.columns:
                    df[col] = df[col] * 0.1
    else:
            print('No need of scaling')
    ax = df.plot.barh()
    ax.invert_yaxis()
    #ax.set_title('Yearly ETa per Landcover', fontsize=14)
    #ax.set_xlabel('mm/year', fontsize=18)
    plt.title('Yearly ETa per Landcover', fontsize=12)
    plt.xlabel('mm/year', fontsize=12)
    plt.savefig(lcbaret, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    
    ## Table 2 Saving to csv's
    ## below eta and pcp in km3 vol
    # round(float(bbox['w']), 2)
    eta_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_eta_mean, LC_area_sqkm)]
    etr_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_etr_mean, LC_area_sqkm)]
    pcp_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_pcp_mean, LC_area_sqkm)]
    peta = [a - b for a, b in zip(lc_pcp_mean, lc_eta_mean)]
    peta_str = ["%.1f" % round(float(item), 1) for item in peta]
    peta_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(peta, LC_area_sqkm)]
    #peta_perc = [int(round(a / b * 100)) for a, b in zip(peta, lc_pcp_mean)]
    df_bcm1 = pd.DataFrame({'Land cover type': lc_eta_str, 'Area(km\u00b2)': LC_area_sqkm, 'Area(%)': LC_perc_flt, 'P(mm/year)': lc_pcp_mean_str, 'ETa(mm/year)': lc_eta_mean, 'P-ETa(mm/year)': peta_str, 'ETr(mm/year)': lc_etr_mean}, index=lc_eta_str)
    df_bcm2 = df_bcm1.sort_values(by = ['Area(%)'], ascending=False)
    dfbcm2 = os.path.join(newdir, "Table2.csv")
    df_bcm2.to_csv(dfbcm2, index = False)
    print('Saving  Table 2')

    df_bcm3 = pd.DataFrame({'Land cover type': lc_eta_str, 'Area(km\u00b2)': LC_area_sqkm, 'Area(%)': LC_perc_flt, 'P(km\u00b3/year)': pcp_vol, 'ETa(km\u00b3/year)': eta_vol, 'P-ETa(km\u00b3/year)': peta_vol, 'ETr(km\u00b3/year)': etr_vol}, index=lc_eta_str)
    df_bcm4 = df_bcm3.sort_values(by = ['Area(%)'], ascending=False)
    dfbcm4 = os.path.join(newdir, "Table3.csv")
    df_bcm4.to_csv(dfbcm4, index = False)
    print('Saving  Table 3')

    # Table 5 with Ea Ta ETb ETg per LC
    #ea_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_ea_mean, LC_area_sqkm)]
    #ta_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_ta_mean, LC_area_sqkm)]
    #etg_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_etg_mean, LC_area_sqkm)]
    #etb_vol = ["%.2f" % round(float(a / 1000000 * b), 2) for a, b in zip(lc_etb_mean, LC_area_sqkm)]
    #df_bcm5 = pd.DataFrame({'Land cover type': lc_eta_str, 'Area(km\u00b2)': LC_area_sqkm, 'Area(%)': LC_perc_flt, 'Ea(mm/year)': lc_ea_mean, 'Ta(mm/year)': lc_ta_mean}, index=lc_eta_str)
    #df_bcm5['Ea(mm/year)'].astype("Int32")
    #df_bcm5['Ta(mm/year)'].astype("Int32")
    #df_bcm5['Ea(mm/year)'] = np.floor(pd.to_numeric(df_bcm5['Ea(mm/year)'], downcast='float', errors='coerce').astype('Int64'))
    #df_bcm5['Ta(mm/year)'] = np.floor(pd.to_numeric(df_bcm5['Ta(mm/year)'], downcast='float', errors='coerce').astype('Int64'))
    #df_bcm6 = df_bcm5.sort_values(by = ['Area(%)'], ascending=False)
    #dfbcm6 = os.path.join(newdir, "Table5.csv")
    #df_bcm6.to_csv(dfbcm6, index = False)
    #print('Saving  Table 5')
    
    LC0 = df_bcm4.iat[0,0]
    LC1 = df_bcm4.iat[1,0]
    LCA0 = df_bcm4.iat[0,1]
    LCA1 = df_bcm4.iat[1,1]
    ### COMPARISON bar charts ###
    year = list(range(2009,2023))
    
    maps_eta = [et + "_eta_y" + s for s in years_str]
    eta=[]
    for i in maps_eta:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            eta.append(mean)
    print('etamean:')
    print(eta)
    
    # #maps_ssebop=grass.list_grouped(type=['raster'], pattern="ssebop_eta_y*")['data_annual']
    # maps_ssebop = ["ssebop_eta_y" + s for s in years_str]
    # ssebop=[]
    # for i in maps_ssebop:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = int(round(float(stats['mean'])))
            # ssebop.append(mean)
    # print('ssebop:')
    # print(ssebop)

    # maps_ensembleet = ["enset_eta_y" + s for s in years_str]
    # enset=[]
    # for i in maps_ensembleet:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = round(float(stats['mean']), 0)
            # enset.append(mean)
    # print('ensemble:')
    # print(enset)
    
    # maps_ensembleetglobal = ["ensetglobal_eta_y" + s for s in years_str]
    # ensetglobal=[]
    # for i in maps_ensembleetglobal:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = round(float(stats['mean']), 0)
            # ensetglobal.append(mean)
    # print('ensetglobal:')
    # print(ensetglobal)

    # ##ssebop_etpa_y2016
    # maps_ssebopetr = ["ssebop_etpa_y" + s for s in years_str]
    # ssebopetr=[]
    # for i in maps_ssebopetr:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = int(round(float(stats['mean'])))
            # ssebopetr.append(mean)
    # print('ssebopetr:')
    # print(ssebopetr)

    # maps_wapor2 = ["wapor2_eta_y" + s for s in years_str]
    # wap2=[]
    # for i in maps_wapor2:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = round(float(stats['mean']), 0)
            # wap2.append(mean)
    # wapor2 = [x * 0.1 for x in wap2]
    # print('wapor2:')
    # print(wapor2)
    
    # maps_wapor3 = ["wapor3_eta_y" + s for s in years_str]
    # wap3=[]
    # for i in maps_wapor3:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = round(float(stats['mean']), 0)
            # wap3.append(mean)
    # wapor3 = [x * 0.1 for x in wap3]
    # print('wapor3:')
    # print(wapor3)

    # maps_ta = [f'Ta_{et}_annual_' + s for s in years_str]
    # ta1=[]
    # for i in maps_ta:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = int(round(float(stats['mean'])))
            # ta1.append(mean)

    # if et == 'wapor2' or et == 'wapor3':
        # ta = [x * 0.1 for x in ta1]
    # else:
        # ta = ta1
    # print('ta:')
    # print(ta)

    # maps_ea = [f'Ea_{et}_annual_' + s for s in years_str]
    # ea1=[]
    # for i in maps_ea:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = int(round(float(stats['mean'])))
            # ea1.append(mean)

    # if et == 'wapor2' or et == 'wapor3':
        # ea = [x * 0.1 for x in ea1]
    # else:
        # ea = ea1
    # print('ea:')
    # print(ea)
    
    #maps_modis=grass.list_grouped(type=['raster'], pattern="modis_eta_*")['data_annual']
    # maps_modis = ["modiseta_annual_" + s for s in years_str]
    # modis=[]
    # for i in maps_modis:
            # stats = grass.parse_command('r.univar', map=i, flags='g')
            # mean = int(round(float(stats['mean'])))
            # modis.append(mean)
    # print(modis)
    
    #maps_chirps=grass.list_grouped(type=['raster'], pattern="chirps_precip_*")['data_annual']
    maps_chirps = ["pcpa_chirps_" + s for s in years_str]
    chirps=[]
    for i in maps_chirps:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            chirps.append(mean)
    print(chirps)

    maps_ensemblepcp = ["pcpa_ensemble_" + s for s in years_str]
    enspcp=[]
    for i in maps_ensemblepcp:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            enspcp.append(mean)
    print(enspcp)
    
    #maps_gpm=grass.list_grouped(type=['raster'], pattern="gpm_precip_*")['data_annual']
    maps_gpm = ["pcpa_gpm_" + s for s in years_str]
    gpm=[]
    for i in maps_gpm:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            gpm.append(mean)
    print(gpm)
    
    #maps_persiann=grass.list_grouped(type=['raster'], pattern="persiann_precip_*")['data_annual']
    maps_persiann = ["pcpa_persiann_" + s for s in years_str]
    persiann=[]
    for i in maps_persiann:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            persiann.append(mean)
    print(persiann)
    
    maps_gsmap = ["pcpa_gsmap_" + s for s in years_str]
    gsmap=[]
    for i in maps_gsmap:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            gsmap.append(mean)
    print(gsmap)
    
    maps_era5 = ["pcpa_era5_" + s for s in years_str]
    era5=[]
    for i in maps_era5:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            era5.append(mean)
    print(era5)
    
    #df_comparison = pd.DataFrame({'Year': years, 'ssebop': ssebop, 'wapor2': wapor2, 'wapor3': wapor3, 'enset': enset, 'ensetglobal': ensetglobal, 'MODIS': modis, 'chirps': chirps, 'gpm': gpm, 'persiann': persiann, 'gsmap': gsmap, 'era5': era5, 'enspcp': enspcp}, index=years)
    
    df_comparison = pd.DataFrame({'Year': years, 'chirps': chirps, 'gpm': gpm, 'persiann': persiann, 'gsmap': gsmap, 'era5': era5, 'enspcp': enspcp}, index=years)
    
    df_eta = pd.DataFrame({'Year': years, 'eta': eta}, index=years)
    
    # ### Bar chart comparison ETa
    # etabar = os.path.join(newdir, "etabar.png")
    # fig, ax = plt.subplots()
    # if df_comparison['wapor2'].isnull().all() == True or df_comparison['enset'].isnull().all() == True:
        # df_comparison.plot.bar(y = ['ssebop', 'wapor3', 'ensetglobal' ], rot = 40, ax = ax, color=['seagreen', 'limegreen', 'springgreen'])
    # else:
        # df_comparison.plot.bar(y = ['ssebop', 'wapor2', 'wapor3', 'enset', 'ensetglobal'], rot = 40, ax = ax, color=['seagreen', 'limegreen', 'springgreen', 'green', 'lightgreen']) 
    # #ax.invert_yaxis()
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # ax.set_title('Annual ETa')
    # ax.set_ylabel('mm/year')
    # plt.savefig(etabar, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    ### Bar chart annual PCP
    pcpbar1 = os.path.join(newdir, "pcpbar1.png")
    fig, ax = plt.subplots()
    df_comparison.plot.bar(y = precip, rot = 40, ax = ax, color=['dodgerblue'])
    #ax.invert_yaxis()
    ax.set_title('Annual Precipitation')
    ax.set_ylabel('mm/year')
    plt.savefig(pcpbar1, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    
    ### Bar chart annual ETa
    etabar = os.path.join(newdir, "etabar.png")
    fig, ax = plt.subplots()
    df_eta.plot.bar(y = eta, rot = 40, ax = ax, color=['seagreen'])
    #ax.invert_yaxis()
    ax.set_title('Annual EvapoTranspiration')
    ax.set_ylabel('mm/year')
    plt.savefig(etabar, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    
    ### Bar chart comparison PCP
    pcpbar2 = os.path.join(newdir, "pcpbar2.png")
    fig, ax = plt.subplots()
    df_comparison.plot.bar(y = ['chirps', 'gpm', 'gsmap', 'era5', 'persiann', 'enspcp'], rot = 40, ax = ax, color=['dodgerblue', 'dimgrey', 'mediumorchid', 'teal', 'navy', 'azure'])
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #ax.invert_yaxis()
    ax.set_title('Comparison of P products')
    ax.set_ylabel('mm/year')
    plt.savefig(pcpbar2, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    Pcomptable = os.path.join(newdir, "Pcomparison.csv")
    df_comparison.to_csv(Pcomptable, index = True)
    print('Saving  P comparison table')

    # Table 1 - Saving the annual PCP and ETa into table:
    ## below eta and pcp in km3 vol
    # round(float(bbox['w']), 2)
    # monthly_ndvi_scaled = [float(x/10000) for x in monthly_ndvi]
    #anneta_vol = ["%.2f" % round(float(x / 1000000 * studyarea), 2) for x in ssebop]
    anneta_vol = [round(float(x / 1000000 * studyarea), 2) for x in eval(et)]
    annpcp_vol = [round(float(x / 1000000 * studyarea), 2) for x in eval(precip)]
    annpeta = [a - b for a, b in zip(eval(precip), eval(et))]
    annpeta_vol = [round(float(x / 1000000 * studyarea), 2) for x in annpeta]
    annetr_vol = [round(float(x / 1000000 * studyarea), 2) for x in ssebopetr]
    #annpeta_perc = [int(round(a / b * 100)) for a, b in zip(annpeta, eval(precip))]
    df_yearly = pd.DataFrame({'P(mm/year)': eval(precip), 'ETa(mm/year)': eval(et), 'P-ETa(mm/year)': annpeta, 'ETr(mm/year)': ssebopetr, 'P(km\u00b3/year)': annpcp_vol,  'ETa(km\u00b3/year)': anneta_vol, 'P-ETa(km\u00b3/year)': annpeta_vol, 'ETr(km\u00b3/year)': annetr_vol}, index=years)
    df_yearly.loc['Average'] = round(df_yearly.mean(), 1)
    df_yearly['P(mm/year)'] = df_yearly['P(mm/year)'].apply(np.int64)
    df_yearly['ETa(mm/year)'] = df_yearly['ETa(mm/year)'].apply(np.int64)
    df_yearly['P-ETa(mm/year)'] = df_yearly['P-ETa(mm/year)'].apply(np.int64)
    df_yearly['ETr(mm/year)'] = df_yearly['ETr(mm/year)'].apply(np.int64)
    dfyearly = os.path.join(newdir, "Table1.csv")
    df_yearly.to_csv(dfyearly, index = True)

    # Table 4 for Ea and Ta
    annea_vol = [round(float(x / 1000000 * studyarea), 2) for x in ea]
    annta_vol = [round(float(x / 1000000 * studyarea), 2) for x in ta]
    df_yearly1 = pd.DataFrame({'Ea(mm/year)': ea, 'Ta(mm/year)': ta, 'Ea(km\u00b3/year)': annea_vol,  'Ta(km\u00b3/year)': annta_vol}, index=years)
    df_yearly1.loc['Average'] = round(df_yearly1.mean(), 1)
    df_yearly1['Ea(mm/year)'] = df_yearly1['Ea(mm/year)'].apply(np.int64)
    df_yearly1['Ta(mm/year)'] = df_yearly1['Ta(mm/year)'].apply(np.int64)
    dfyearly1 = os.path.join(newdir, "Table4.csv")
    df_yearly1.to_csv(dfyearly1, index = True)

    # PKA trend plots:
    anneta_vol1 = [round(float(x / 1000000 * studyarea), 4) for x in eval(et)]
    print(anneta_vol1)
    annpcp_vol1 = [round(float(x / 1000000 * studyarea), 4) for x in eval(precip)]
    print(annpcp_vol1)
    etavol_avg = statistics.mean(anneta_vol1)
    print(etavol_avg)
    pcpvol_avg = statistics.mean(annpcp_vol1)
    print(pcpvol_avg)
    eta_anomaly = [int(((x / etavol_avg) - 1) * 100) for x in anneta_vol1]
    pcp_anomaly = [int(((x / pcpvol_avg) - 1) * 100) for x in annpcp_vol1]
    df_anomaly = pd.DataFrame({'Year': years, 'ETa_anomaly': eta_anomaly, 'PCP_anomaly': pcp_anomaly}, index=years)
    panoplot = os.path.join(newdir, "panoplot.png")
    etanoplot = os.path.join(newdir, "etanoplot.png")
    fig, ax = plt.subplots()
    x = df_anomaly['Year']
    y = df_anomaly['ETa_anomaly']
    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    ax.set_ylabel('Delta ET')
    ax.set_xlabel('Year')
    plt.savefig(etanoplot, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    fig, ax = plt.subplots()
    y = df_anomaly['PCP_anomaly']
    plt.scatter(x, y)
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    ax.set_ylabel('Delta P')
    ax.set_xlabel('Year')
    plt.savefig(panoplot, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    ### Bar chart annual PCP-ET
    pminetbar = os.path.join(newdir, "pminetbar.png")
    fig, ax = plt.subplots()
    df_yearly['positive'] = df_yearly['P-ETa(mm/year)'] > 0
    df_yearly['P-ETa(mm/year)'].plot(kind='bar', rot = 40, ax = ax, color=df_yearly.positive.map({True: 'deepskyblue', False: 'darkred'}))
    #ax.invert_yaxis()
    ax.set_title('Annual P-ETa')
    ax.set_ylabel('mm/year')
    plt.savefig(pminetbar, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    # PCP long term trend
    #matplotlib.rcParams.update({'font.size': 26})
    longyears = list(range(1981,2021))
    longyears_str = [str(s) for s in longyears]
    ts_chirps = ["pcpa_chirps_" + s for s in longyears_str]
    chirpsts=[]
    for i in ts_chirps:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            #mean = float(stats['mean'])
            chirpsts.append(mean)
    print(chirpsts)
    df_pcpts = pd.DataFrame({'Year': longyears, 'PCP': chirpsts}, index=longyears)
    pcptstable = os.path.join(newdir, "pcpts.csv")
    df_pcpts.to_csv(pcptstable, index = False)
    print('Saving  long term precip table')
    pcptsbar = os.path.join(newdir, "pcpbarts.png")
    fig, ax = plt.subplots(figsize=(30,10))
    ax.tick_params(axis='both', labelsize=14)
    #ax.invert_yaxis()
    ax.set_title('Annual Precipitation from 1981 to 2020', fontsize=20)
    ax.set_xlabel('mm/year', fontsize=16)
    x = df_pcpts['Year']
    y = df_pcpts['PCP']
    plt.bar(x, y, color=['dodgerblue'])
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
    plt.savefig(pcptsbar, bbox_inches='tight', pad_inches = 0.1, dpi=100)

    ## Bar chart monthly ETa/PCP & NDVI
    maps_monthly_eta=grass.list_grouped(type=['raster'], pattern=f'{et}_eta_2020*')['data_monthly']
    monthly_eta1=[]
    for i in maps_monthly_eta:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            monthly_eta1.append(mean)

    if et == 'wapor':
        monthly_eta = [x * 0.1 for x in monthly_eta1]
    else:
        monthly_eta = monthly_eta1
    print('monthly_eta:')
    print(monthly_eta)

    
    maps_monthly_pcp=grass.list_grouped(type=['raster'], pattern=f'{precip}_monthly_2020*')['data_monthly']
    monthly_pcp=[]
    for i in maps_monthly_pcp:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            monthly_pcp.append(mean)
    print(monthly_pcp)
    
    maps_monthly_ndvi=grass.list_grouped(type=['raster'], pattern="ndvi_monthly_2020*")['data_monthly']
    monthly_ndvi=[]
    for i in maps_monthly_ndvi:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            monthly_ndvi.append(mean)
    print(monthly_ndvi)
    monthly_ndvi_scaled = [float(x/10000) for x in monthly_ndvi]
    
    r.mask(raster="LC_studyarea", maskcats='40')
    monthly_ndvi_crop=[]
    for i in maps_monthly_ndvi:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 0)
            monthly_ndvi_crop.append(mean)
    print(monthly_ndvi_crop)
    monthly_ndvi_crop_scaled = [float(x/10000) for x in monthly_ndvi_crop]

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_monthly = pd.DataFrame({'ETa': monthly_eta, 'PCP': monthly_pcp, 'NDVI': monthly_ndvi_scaled, 'NDVI_crop': monthly_ndvi_crop_scaled}, index=months)
    
    monthlyetabar = os.path.join(newdir, "monthlyetabar.png")
    fig, ax = plt.subplots()
    df_monthly.plot.bar(y = ['ETa', 'PCP'], rot = 40, ax = ax, color=['seagreen', 'dodgerblue'])
    #ax.invert_yaxis()
    ax.set_title('Monthly variation of ETa and P')
    ax.set_ylabel('mm/month')
    plt.savefig(monthlyetabar, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    
    monthlyndvi = os.path.join(newdir, "monthlyndvi.png")
    fig, ax = plt.subplots()
    df_monthly.plot.line(y = 'NDVI', rot = 40, ax = ax, color=['mediumseagreen'])
    #ax.invert_yaxis()
    ax.set_title('Monthly variation of NDVI')
    ax.set_ylabel('NDVI')
    plt.savefig(monthlyndvi, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    monthlyndvi_crop = os.path.join(newdir, "monthlyndvi_crop.png")
    fig, ax = plt.subplots()
    df_monthly.plot.line(y = 'NDVI_crop', rot = 40, ax = ax, color=['lime'])
    #ax.invert_yaxis()
    ax.set_title('Monthly variation of NDVI over cropland')
    ax.set_ylabel('NDVI')
    plt.savefig(monthlyndvi_crop, bbox_inches='tight',pad_inches = 0.1, dpi=100)
    r.mask(vector=vectname)
    maps_grace=grass.list_grouped(type=['raster'], pattern="mascon_lwe_thickness*")['grace']
    grace=[]
    grace_dt=[]
    grace_yr=[]
    for i in maps_grace:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = float(stats['mean'])
            yr = i.split('_')[3]
            mm = i.split('_')[4]
            dt = yr + '-' + mm
            grace.append(mean)
            grace_yr.append(yr)
            grace_dt.append(dt)


    dfgrace = pd.DataFrame({'waterlevel': grace, 'date': grace_dt, 'year': grace_yr}, index=grace_yr)

    if studyarea >= 10000:
        grace_fig = os.path.join(newdir, "grace_fig.png")
        fig, ax = plt.subplots()
        dfgrace.plot.line(y = ['waterlevel', 'year'], rot = 40, ax = ax, color=['black'])
        ax.set_title('Change in water storage')
        ax.set_ylabel('Equivalent cm of water')
        plt.savefig(grace_fig, bbox_inches='tight',pad_inches = 0.1, dpi=100)
        gracetable = os.path.join(newdir, "gracetable.csv")
        dfgrace.to_csv(gracetable, index = False)
        print('Saving  grace table')
    else:
        print('No grace data - area is small')
    
    r.mask(flags="r")
    g.region(vector=vectname, res=0.05)
    r.mask(vector=vectname)
    ### Climate change analysis
    ### SSP245
    yearcc1 = list(range(2015,2061))
    yearcc = [str(s) for s in yearcc1]
    maps_tdegssp245 = ["tdegDev_annual_ssp245_" + s for s in yearcc]
    tdegssp245=[]
    for i in maps_tdegssp245:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 1)
            tdegssp245.append(mean)
    print('tdegssp245:')
    print(tdegssp245)

    maps_prssp245 = ["prDev_annual_ssp245_" + s for s in yearcc]
    prssp245=[]
    for i in maps_prssp245:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            prssp245.append(mean)
    print('prssp245:')
    print(prssp245)

    ### SSP585
    maps_tdegssp585 = ["tdegDev_annual_ssp585_" + s for s in yearcc]
    tdegssp585=[]
    for i in maps_tdegssp585:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = round(float(stats['mean']), 1)
            tdegssp585.append(mean)
    print('tdegssp585:')
    print(tdegssp585)

    maps_prssp585 = ["prDev_annual_ssp585_" + s for s in yearcc]
    prssp585=[]
    for i in maps_prssp585:
            stats = grass.parse_command('r.univar', map=i, flags='g')
            mean = int(round(float(stats['mean'])))
            prssp585.append(mean)
    print('prssp585:')
    print(prssp585)
   
    df_cc1 = pd.DataFrame({'Year': yearcc, 'tdegssp245': tdegssp245, 'prssp245': prssp245, 'tdegssp585': tdegssp585, 'prssp585': prssp585}, index=yearcc)

    df_cc1['tdegssp245_mn'] = df_cc1['tdegssp245'].rolling(5).mean()
    df_cc1['tdegssp245_std'] = df_cc1['tdegssp245'].rolling(5).std()
    df_cc1['tdegssp245_un'] = df_cc1['tdegssp245_mn'] - df_cc1['tdegssp245_std']
    df_cc1['tdegssp245_ov'] = df_cc1['tdegssp245_mn'] + df_cc1['tdegssp245_std']

    df_cc1['prssp245_mn'] = df_cc1['prssp245'].rolling(5).mean()
    df_cc1['prssp245_std'] = df_cc1['prssp245'].rolling(5).std()
    df_cc1['prssp245_un'] = df_cc1['prssp245_mn'] - df_cc1['prssp245_std']
    df_cc1['prssp245_ov'] = df_cc1['prssp245_mn'] + df_cc1['prssp245_std']

    df_cc1['tdegssp585_mn'] = df_cc1['tdegssp585'].rolling(5).mean()
    df_cc1['tdegssp585_std'] = df_cc1['tdegssp585'].rolling(5).std()
    df_cc1['tdegssp585_un'] = df_cc1['tdegssp585_mn'] - df_cc1['tdegssp585_std']
    df_cc1['tdegssp585_ov'] = df_cc1['tdegssp585_mn'] + df_cc1['tdegssp585_std']

    df_cc1['prssp585_mn'] = df_cc1['prssp585'].rolling(5).mean()
    df_cc1['prssp585_std'] = df_cc1['prssp585'].rolling(5).std()
    df_cc1['prssp585_un'] = df_cc1['prssp585_mn'] - df_cc1['prssp585_std']
    df_cc1['prssp585_ov'] = df_cc1['prssp585_mn'] + df_cc1['prssp585_std']

    df_cc = df_cc1.dropna()
    mk1 = mk.original_test(df_cc['tdegssp245'])
    mk11 = pd.DataFrame(mk1, columns=['Name'])
    t1 = mk11.loc[0,'Name']
    sl1 = round(float(mk11.loc[7,'Name']),2)
    in1 = round(float(mk11.loc[8,'Name']),2)
    mk2 = mk.original_test(df_cc['prssp245'])
    mk21 = pd.DataFrame(mk2, columns=['Name'])
    t2 = mk21.loc[0,'Name']
    sl2 = round(float(mk21.loc[7,'Name']),2)
    in2 = round(float(mk21.loc[8,'Name']),2)
    mk3 = mk.original_test(df_cc['tdegssp585'])
    mk31 = pd.DataFrame(mk3, columns=['Name'])
    t3 = mk31.loc[0,'Name']
    sl3 = round(float(mk31.loc[7,'Name']),2)
    in3 = round(float(mk31.loc[8,'Name']),2)
    mk4 = mk.original_test(df_cc['prssp585'])
    mk41 = pd.DataFrame(mk4, columns=['Name'])
    t4 = mk41.loc[0,'Name']
    sl4 = round(float(mk41.loc[7,'Name']),2)
    in4 = round(float(mk41.loc[8,'Name']),2)


    figt1 = os.path.join(newdir, "figt1.png")
    fig = plt.figure()
    x = df_cc['Year'].astype(int)
    y = df_cc['tdegssp245_mn']
    plt.plot(x,y, color='green')
    plt.ylabel('Temperature (DegC)')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
#     plt.fill_between(x, df_cc['tdegssp245_un'], df_cc['tdegssp245_ov'], color='b', alpha=.1)
    plt.title('Annual mean Temperature (deviation)') 
    plt.savefig(figt1, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    figt2 = os.path.join(newdir, "figt2.png")
    fig = plt.figure()
    x = df_cc['Year'].astype(int)
    y = df_cc['prssp245_mn']
    plt.plot(x,y)
    plt.ylabel('Precipitation (mm/year)')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
#     plt.fill_between(x, df_cc['prssp245_un'], df_cc['prssp245_ov'], color='b', alpha=.1)
    plt.title('Annual mean Precipitation (deviation)')
    plt.savefig(figt2, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    figt3 = os.path.join(newdir, "figt3.png")
    fig = plt.figure()
    x = df_cc['Year'].astype(int)
    y = df_cc['tdegssp585_mn']
    plt.plot(x,y, color='green')
    plt.ylabel('Temperature (DegC)')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
#     plt.fill_between(x, df_cc['tdegssp585_un'], df_cc['tdegssp585_ov'], color='b', alpha=.1)
    plt.title('Annual mean Temperature (deviation)') 
    plt.savefig(figt3, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    figt4 = os.path.join(newdir, "figt4.png")
    fig = plt.figure()
    x = df_cc['Year'].astype(int)
    y = df_cc['prssp585_mn']
    plt.plot(x,y)
    plt.ylabel('Precipitation (mm/year)')
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--")
#     plt.fill_between(x, df_cc['prssp585_un'], df_cc['prssp585_ov'], color='b', alpha=.1)
    plt.title('Annual mean Precipitation (deviation)')
    plt.savefig(figt4, bbox_inches='tight',pad_inches = 0.1, dpi=100)

    r.mask(flags="r")
    plt.close('all')

    ### Parse statistics to the report
    stats = dict(et=et,pcp=precip,st=start,sp=stop,centx=centX,centy=centY,w=west,e=east,n=north,s=south,area=studyarea,dem_min=dem_min,dem_max=dem_max,lc0=LC0,lc1=LC1,lca0=LCA0,lca1=LCA1,eta=mean_eta_basin,p=mean_pcp_basin,etr=mean_etr_basin,t1=t1,t2=t2,t3=t3,t4=t4,sl1=sl1,sl2=sl2,sl3=sl3,sl4=sl4)
    #etb=mean_etb_basin,etg=mean_etg_basin
    mean = 100

    ## Mimic an empty mapset with WIND file for raster2numpy to work.
    mapdir = os.path.join(settings.GRASS_DB, 'wagen', 'job{}'.format(jobid))
    windsrc = os.path.join(mapdir, 'WIND')
    winddst = os.path.join(newdir, 'WIND')
    shutil.copy2(windsrc, winddst)
    user.close()
    os.mkdir(mapdir)
    shutil.copy2(winddst, windsrc)

    htmlfile1 = render_prod_html(jobid, myarea, stats)
    htmlfile2 = render_pdf_html(jobid, myarea, stats)
    pdffile = render_pdf(htmlfile2, jobid)
    print("Preparing report !")
    base_url = settings.BASE_URL

    sub="Water Accounting Report"
    mess = f"Your requested Water Accounting report is ready. You can access the report using this link: {base_url}/media/{jobid}/index.html"
    

    to=current_user

    attach=pdffile
    #send_mail_attach(sub, mess, to, attach)
    return htmlfile1, pdffile


