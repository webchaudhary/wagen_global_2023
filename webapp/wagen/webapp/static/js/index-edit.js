document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId, featuresBox, zoomBox) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            box = document.getElementById(featuresBox),
            zoom = document.getElementsByClassName(zoomBox),
            headerpd = document.getElementById(headerId)

        // Validate that all variables exist
        if (toggle && nav && bodypd && headerpd && box) {
            toggle.addEventListener('click', () => {
                box.classList.toggle('box-pd')
                // console.log(box);
                zoom[0].classList.toggle('box-pd')
                // show navbar
                nav.classList.toggle('show')
                // change icon
                toggle.classList.toggle('bx-x')
                // add padding to body
                // bodypd.classList.toggle('body-pd')
                // add padding to header
                headerpd.classList.toggle('body-pd')


            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header', 'featuresBox', 'ol-zoom')

    /*===== LINK ACTIVE =====*/
    // const linkColor = document.querySelectorAll('.nav_link')

    // function colorLink() {
    //     if (linkColor) {
    //         linkColor.forEach(l => l.classList.remove('active'))
    //         this.classList.add('active')
    //     }
    // }
    // linkColor.forEach(l => l.addEventListener('click', colorLink))

    // Your code to run since DOM is loaded and ready
});
// SIDE MENU JS ENDS---------------------------------------------------------------------------------------------------------------------------

var epsgsrc = 'EPSG:3857'
var espgdest = 'EPSG:4326'
var epsgmoll = 'ESRI:53009'
proj4.defs(
    'ESRI:53009',
    '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +a=6371000 ' +
    '+b=6371000 +units=m +no_defs'
);
var mainBondingBox = turf.polygon([[[-180, -70], [-180, 70], [180, 70], [180, -70], [-180, -70]]], {name: 'main bounding box'})
ol.proj.proj4.register(proj4);
var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var file;
var addid;
//$('.input-daterange').datepicker({
//          format: 'yyyy-mm'
//        });
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
function sleep(milliseconds) {
    var timeStart = new Date().getTime();
    while (true) {
        var elapsedTime = new Date().getTime() - timeStart;
        if (elapsedTime > milliseconds) {
            break;
        }
    }
}
var overlay = new ol.Overlay({
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250,
    },
});

closer.onclick = function () {
  overlay.setPosition(undefined);
  closer.blur();
  bobasource.clear()
  return false;
};
var drawModal = new bootstrap.Modal(document.getElementById('drawModal'), {
    keyboard: false
})

var attribution = new ol.control.Attribution({
    collapsible: true,
});

var otmlayer = new ol.layer.Tile({
    source: new ol.source.OSM({
        url: 'https://{a-c}.tile.opentopomap.org/{z}/{x}/{y}.png'
    })
})

var osmlayer = new ol.layer.Tile({
    source: new ol.source.OSM()
})


/*var sentinellayer = new ol.layer.Image({
  source: new ol.source.ImageWMS({*/

var sentinellayer = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'https://tiles.maps.eox.at/wms?',
        params: { 'LAYERS': 's2cloudless_3857' },
        version: '1.1.1',
        format: 'image/png',
        ratio: 1,
        serverType: 'mapserver',
        attributions: ['Sentinel-2 cloudless - <a href="https://s2maps.eu" target="_blank" title="Sentinel-2 cloudless">https://s2maps.eu</a> by <a href="https://eox.at/" target="_blank" title="Eox Company">EOX IT Services GmbH</a> (Contains modified Copernicus Sentinel data 2016 & 2017)']
    }),
    visible: false
})

var worldcover = new ol.layer.Tile({
    source: new ol.source.TileWMS({
        url: 'https://services.terrascope.be/wms/v2?',
        params: { 'LAYERS': 'WORLDCOVER_2020_MAP', "TILED": "true", "VERSION": "1.1.1" },
        version: '1.1.1',
        format: 'image/png',
        attributions: ['ESA Worldcover 10m <a href="https://esa-worldcover.org/" target="_blank" title="ESA Worldcover 10m">https://esa-worldcover.org/</a>']
    }),
    visible: false
})

var polystyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 0, 0, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#ff0000',
        width: 2,
    }),
    image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({
            color: '#ffcc33',
        }),
    }),
})

var polysource = new ol.source.Vector();
var polyvector = new ol.layer.Vector({
    source: polysource,
    style: polystyle,
    name: 'selected,'
});

//Layer for storing measurement vectors
var measurevector = new ol.layer.Vector({
    source: new ol.source.Vector(),
    name: 'measure'
});

var bobastyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(102, 51, 153, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#663399',
        width: 2,
    }),
    image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({
            color: '#ffcc33',
        }),
    })
})

var bobasource = new ol.source.Vector();
var bobavector = new ol.layer.Vector({
    source: bobasource,
    style: bobastyle,
    name: 'selected,'
});

var areastyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 255, 0, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#ffff00',
        width: 2,
    }),
    image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({
            color: '#ffcc33',
        }),
    })
})

var areahighlight = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(0, 255, 0, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#00ff00',
        width: 3,
    }),
    image: new ol.style.Circle({
        radius: 7,
        fill: new ol.style.Fill({
            color: '#ffcc33',
        }),
    }),
    text: new ol.style.Text({
        font: '12px Calibri,sans-serif',
        fill: new ol.style.Fill({
            color: '#000',
        }),
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3,
        }),
    }),
})

var areasource = new ol.source.Vector();
var areavector = new ol.layer.Vector({
    source: areasource,
    style: areastyle,
    name: 'areas',
});
areavector.setVisible(false);

var basinstyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(0, 115, 207, 0.2)',
    }),
    stroke: new ol.style.Stroke({
        color: '#0073cf',
        width: 1,
    }),
})
var basinhighlight = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(0, 115, 207, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#0073cf',
        width: 3,
    }),
    text: new ol.style.Text({
        font: '12px Calibri,sans-serif',
        fill: new ol.style.Fill({
            color: '#000',
        }),
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3,
        }),
    }),
})
var geoJSONFormat = new ol.format.GeoJSON({});
var wapor_source = [];
var basinvector = new ol.layer.Vector({
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON,
        url: '/static/data/boundaries.geojson'
    }),
    name: 'basins',
    style: basinstyle
});
basinvector.setVisible(false);

var boundstyle = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(100, 100, 100, 0.2)',
    }),
    stroke: new ol.style.Stroke({
        color: '#000000',
        width: 1,
    }),
    text: new ol.style.Text({
        font: '12px Calibri,sans-serif',
        fill: new ol.style.Fill({
            color: '#000',
        }),
        stroke: new ol.style.Stroke({
            color: '#fff',
            width: 3,
        }),
    }),
})
var boundhighlight = new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(100, 100, 100, 0.4)',
    }),
    stroke: new ol.style.Stroke({
        color: '#000000',
        width: 3,
    }),
})

var boundsvector = new ol.layer.Vector({
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON,
        url: '/static/data/boundaries.geojson'
    }),
    name: 'bounds',
    style: boundstyle
});
boundsvector.setVisible(false);



var map = new ol.Map({
    controls: ol.control.defaults({ attributionOptions: { collapsible: true } }).extend(
        [
            new ol.control.ScaleLine({
                bar: false,
                steps: 4,
                text: true,
                minWidth: 100
            })
        ]),
    target: 'map',
    layers: [otmlayer, osmlayer, worldcover, sentinellayer, areavector, polyvector, basinvector, boundsvector, bobavector, measurevector],
    view: new ol.View({
        center: ol.proj.fromLonLat([20, 10]),
        zoom: 2
    }),
    overlays: [overlay]
    //controls: ol.control.defaults({attribution: false}).extend([attribution])
});


//Create overlay for measurement
function createMeasureOverlay() {
    return new ol.Overlay({
        element: document.getElementById("measure_popup"),
        offset: [0, -15],
        positioning: 'bottom-center',
        className: 'ol-tooltip-measure ol-tooltip .ol-tooltip-static'
    });
}

//Meaure Area and Distance
var measuredraw, measureOverlayArrays = [];

function calArea(measure_overlay, overlayPosition, area) {
    var measure_label;
    measure_overlay.setPosition(overlayPosition);
    if (area > 10000) {
        measure_label = Math.round((area / 1000000) * 100) / 100 + ' KM\xB2';
    } else {
        measure_label = Math.round(area * 100) / 100 + ' M\xB2';
    }
    measure_overlay.element.innerHTML = '<b>' + measure_label + '</b>';
}

function calDistance(measure_overlay, overlayPosition, length) {
    var measure_label;
    if (parseInt(length) == 0) {
        measure_overlay.setPosition([0, 0]);
    }
    else {
        measure_overlay.setPosition(overlayPosition);
        if (length > 100) {
            measure_label = Math.round((length / 1000) * 100) / 100 + ' KM';
        } else {
            measure_label = Math.round(length * 100) / 100 + ' M';
        }
        measure_overlay.element.innerHTML = '<b>' + measure_label + '</b>';
    }
}

function addMeasureInteractions(geomType) {
    if (measuredraw) {
        map.removeInteraction(measuredraw);
    }
    measuredraw = new ol.interaction.Draw({
        source: measurevector.getSource(),
        type: geomType,
    });
    measuredraw.on('drawstart', function (event) {
        var that = this;
        var measure_overlay = createMeasureOverlay()
        that.coordinates_length = 0;
        measureOverlayArrays.push(measure_overlay);
        measure_overlay.setPosition([0, 0]);
        measure_overlay.element.style.display = 'block';
        map.addOverlay(measure_overlay);

        event.feature.getGeometry().on('change', function (e) {
            if (e.target.getType() == "Polygon") {
                var geom = e.target.clone();
                area = geom.transform(epsgsrc, epsgmoll).getArea();
                calArea(measure_overlay, e.target.getInteriorPoint().getCoordinates().slice(0, 2), area);
            } else {
                var coordinates = e.target.getCoordinates();
                if (coordinates.length > that.coordinates_length) {
                    that.coordinates_length = coordinates.length;
                    partOverLay = createMeasureOverlay();
                    map.addOverlay(partOverLay);
                    measureOverlayArrays.push(partOverLay);
                }
                else {
                    that.coordinates_length = coordinates.length;
                }

                var partLine = new ol.geom.LineString([coordinates[that.coordinates_length - 2], coordinates[that.coordinates_length - 1]]);
                var p1 = partLine.getCoordinates()[0];
                var p2 = partLine.getCoordinates()[1];
                var midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2];

                var partGeom = partLine.clone();
                calDistance(partOverLay, midPoint, partGeom.transform(epsgsrc, epsgmoll).getLength());

                if (that.coordinates_length > 2 && e.target.getLength() > new ol.geom.LineString([coordinates[0], coordinates[1]]).getLength()) {
                    var geom = e.target.clone();
                    length = geom.transform(epsgsrc, epsgmoll).getLength();
                    calDistance(measure_overlay, e.target.getLastCoordinate(), length);
                }
            }
        });
    });
    map.addInteraction(measuredraw);
}


//Handles Distance Measurement
$("#distance_measurement").click(function (e) {
    $("#area_measurement").removeClass('active');
    if ($(this).hasClass('active')) {
        var geomType = e.target.getAttribute('geomType');
        addMeasureInteractions(geomType);
    } else {
        map.removeInteraction(measuredraw);
        // for(var i = 0; i < measureOverlayArrays.length; i++) {
        //   map.removeOverlay(measureOverlayArrays[i]);
        // }
        // measureOverlayArrays = [];
        // measurevector.getSource().clear();
    }
});

//Handles Area Measurement
$("#area_measurement").click(function (e) {
    $("#distance_measurement").removeClass('active');
    if ($(this).hasClass('active')){
        var geomType = e.target.getAttribute('geomType');
        addMeasureInteractions(geomType);
    } else {
        map.removeInteraction(measuredraw);
        // for(var i = 0; i < measureOverlayArrays.length; i++) {
        //   map.removeOverlay(measureOverlayArrays[i]);
        // }
        // measureOverlayArrays = [];
        // measurevector.getSource().clear();
    }
});

// Switch to full extent
$("#full_extent").click(function () {
    map.setView(
        new ol.View({
            center: ol.proj.fromLonLat([20, 10]),
            zoom: 2
        })
    )
});

// Clear measure interaction, measure features and measure overlays
$("#clear").click(function () {
    $("#area_measurement").removeClass('active');
    $("#distance_measurement").removeClass('active');
    if (measuredraw) {
        map.removeInteraction(measuredraw);
    }
    if (draw) {
        // map.removeInteraction(draw);
        event.target.abortDrawing();
    }
    for (var i = 0; i < measureOverlayArrays.length; i++) {
        map.removeOverlay(measureOverlayArrays[i]);
    }
    measureOverlayArrays = [];
    measurevector.getSource().clear();
});
//Show X,Y coordinates
map.on('pointermove', function (e) {
    var x = ol.proj.toLonLat(e.coordinate)[0];
    $("#x")[0].innerHTML = x.toFixed(5);
    var y = ol.proj.toLonLat(e.coordinate)[1];
    $("#y")[0].innerHTML = y.toFixed(5);
});

$('input[type="radio"]').click(function(){
  if($(this).prop("checked")){
	var layername = $(this).val()
  }
  if (layername == 'otm'){
	$("#esa-legend").css("display", "none");
	worldcover.setVisible(false);
	sentinellayer.setVisible(false);
	osmlayer.setVisible(false);
	otmlayer.setVisible(true);
  } else if (layername == 'osm'){
	$("#esa-legend").css("display", "none");
	worldcover.setVisible(false);
	sentinellayer.setVisible(false);
	osmlayer.setVisible(true);
	otmlayer.setVisible(false);
  } else if (layername == 'sen2'){
	$("#esa-legend").css("display", "none");
	worldcover.setVisible(false);
	sentinellayer.setVisible(true);
	osmlayer.setVisible(false);
	otmlayer.setVisible(false);
  }else if (layername == 'esa'){
	$("#esa-legend").css("display", "block");
	worldcover.setVisible(true);
	sentinellayer.setVisible(false);
	osmlayer.setVisible(false);
	otmlayer.setVisible(false);
  }
})

$('input[type="checkbox"]').click(function(){
  if($(this).prop("checked")){
	var layername = $(this).val()
  }
  if (layername == 'myareas'){
	areavector.setVisible(true);
	basinvector.setVisible(false);
	boundsvector.setVisible(false);
	$('#checkbasins').prop( "checked", false );
	$('#checkbounds').prop( "checked", false );
  } else {
	areavector.setVisible(false);
  }
  if (layername == 'basins'){
	basinvector.setVisible(true);
	areavector.setVisible(false);
	boundsvector.setVisible(false);
	$('#checkbounds').prop( "checked", false );
	$('#checkareas').prop( "checked", false );
  } else {
	basinvector.setVisible(false);
  }
  if (layername == 'boundaries'){
	boundsvector.setVisible(true);
	basinvector.setVisible(false);
	areavector.setVisible(false);
	$('#checkbasins').prop( "checked", false );
	$('#checkareas').prop( "checked", false );
  } else {
	boundsvector.setVisible(false);
  }
})
//var modify = new ol.interaction.Modify({source: polysource});
//map.addInteraction(modify);

var draw, snap; // global so we can remove them later
var typeSelect = document.getElementById('type');
function addInteractions() {
  polysource.clear()
  $('#areaSelect').val('noarea')
  draw = new ol.interaction.Draw({
	source: polysource,
	type: 'Polygon',
  });
  draw.on('drawstart', function (event) {
	event.feature.getGeometry().on('change', function(e){
	  window.event = event;
	});
  });
  draw.on('drawend', function (event) {
	var feat = event.feature;
	areafeat = feat.clone()
	areafeat.getGeometry().transform(epsgsrc, epsgmoll);
	if (feat.getGeometry().getArea() < 20000000){
	  $("#returnText").text("The area is too small, please draw a bigger area");
	  $("#returnModal").modal('show');
	  polysource.clear();
	//} else if (feat.getGeometry().getArea() > 100000000) {
//            	$("#returnText").text("The area is to big, please draw a bigger area");
//              $("#returnModal").modal('show');
//              polysource.clear();
	} else {
	  feat.getGeometry().transform(epsgsrc, espgdest)
	  var geoJsonStr = geoJSONFormat.writeGeometry(feat.getGeometry());
	  $("#featGeom").val(geoJsonStr);
	  drawModal.show()
	}

  });
  map.addInteraction(draw);
  snap = new ol.interaction.Snap({source: polysource});
  map.addInteraction(snap);
}

$('#addarea').click(function () {
  if($(this).hasClass('active')){
	addInteractions();
  } else {
	map.removeInteraction(draw);
	map.removeInteraction(snap);
  }
})
$('#addlayerbtn').click(function () {
  if($(this).hasClass('active')){
	map.removeInteraction(draw);
	map.removeInteraction(snap);
  }
})
$('#infobtn').click(function () {
  console.log('active');
  $("#returnText").text("");
  $("#returnText").text("WaterAccounting.app automatically generates a water balance report over any selected area by the user. The tool make use of remotely sensed datasets to generate various components of water balance laid over to a report in html and pdf format.")
})
var hovered = null;
var newfeat = null;
map.on('pointermove', function (e) {
  if (hovered !== null) {
	hovered.setStyle(undefined);
	hovered = null;
  }

  map.forEachFeatureAtPixel(e.pixel, function (f, l) {
	if(l){
	  if (l.get('name') == 'areas'){
		hovered = f;
		f.setStyle(areahighlight);
		f.getStyle().getText().setText(f.get('name'));
		return true;
	  } else if (l.get('name') == 'basins') {
		hovered = f;
		f.setStyle(areahighlight);
		f.getStyle().getText().setText(f.get('name'));
		return true;
	  } else if (l.get('name') == 'bounds') {
		hovered = f;
		f.setStyle(areahighlight);
		f.getStyle().getText().setText(f.get('name'));
		return true;
	  } else {
		var fid = f.getId();
		if (l.get('name') == 'areas'){
		  var featstyle = areasource.getFeatureById(fid);
		  featstyle.setStyle(areastyle);
		  return true;
		} else if (l.get('name') == 'basins') {
		  var featstyle = areasource.getFeatureById(fid);
		  featstyle.setStyle(basinstyle);
		  return true;
		} else if (l.get('name') == 'bounds') {
		  var featstyle = areasource.getFeatureById(fid);
		  featstyle.setStyle(boundstyle);
		  return true;
		}
	  }
	}
  })
})

function checkDataConstraint() {
  var element = $("#areaSelect").find(':selected')
  if (element.data('geom') === undefined) {
	  $("#getReport").prop("disabled", true);
	  return
	}
  var jsongeom = element.data('geom')
  var multipolys = new ol.geom.MultiPolygon(jsongeom['coordinates']).getPolygons()
  //var olgeom = geoJSONFormat.writeGeometryObject(new ol.geom.MultiPolygon(jsongeom['coordinates']))
  //console.log(olgeom)
  for (let poly in multipolys){
	var geom = geoJSONFormat.writeGeometryObject(multipolys[poly])
	var maincheck = turf.booleanContains(mainBondingBox['geometry'], geom)
	if (maincheck == false) {
		$("#returnText").text("");
		$("#returnText").text("The selected area exceed from general bounding box (-180,-70,180,70) ")
		$("#returnModal").modal('show');
		$("#getReport").prop("disabled", true);
		return
	}
  }

  var precip = $('#precip').val();
  if (precip == "chirps"){
	var precipBoundingBox = turf.polygon([[[-180, -50], [-180, 50], [180, 50], [180, -50], [-180, -50]]], {name: 'precip bounding box'})
	for (let poly in multipolys){
	  var geom = geoJSONFormat.writeGeometryObject(multipolys[poly])
	  var precipcheck = turf.booleanContains(precipBoundingBox['geometry'], geom)
	  if (precipcheck == false) {
		  $("#returnText").text("");
		  $("#returnText").text("The selected area exceed from CHIRPS bounding box (-180, -50, 180, 50) ")
		  $("#returnModal").modal('show');
		  $("#getReport").prop("disabled", true);
		  return
	  }
	}
  } else if (precip == "persiann") {
	var precipBoundingBox = turf.polygon([[[-180, -60], [-180, 60], [180, 60], [180, -60], [-180, -60]]], {name: 'precip bounding box'})
	for (let poly in multipolys){
	  var geom = geoJSONFormat.writeGeometryObject(multipolys[poly])
	  var precipcheck = turf.booleanContains(precipBoundingBox['geometry'], geom)
	  if (precipcheck == false) {
		  $("#returnText").text("");
		  $("#returnText").text("The selected area exceed from PERSIANN bounding box (-180, -60, 180, 60) ")
		  $("#returnModal").modal('show');
		  $("#getReport").prop("disabled", true);
		  return
	  }
	}
  }

  var et = $('#et').val();
  if (et == "wapor") {
	for (let poly in multipolys){
	  var geom = geoJSONFormat.writeGeometryObject(multipolys[poly])
	  for (let wapor in wapor_source) {
		var waporcheck = turf.booleanContains(wapor_source[wapor], geom)
		if (waporcheck == false) {
		  $("#returnText").text("");
		  $("#returnText").text("The selected area exceed from WaPOR bounding box (cover only Africa) ")
		  $("#returnModal").modal('show');
		  $("#getReport").prop("disabled", true);
		  return
		}
	  }

	}
  }
  $("#getReport").prop("disabled", false);
}

function addBB() {
  var geom = newfeat.getGeometry()
  var newgeom = geom.transform(epsgsrc, espgdest)
  var geoJsonStr = geoJSONFormat.writeGeometry(newgeom);
  $("#featGeom").val(geoJsonStr);
  $("#featName").val(newfeat.get('name'));
  var newgeom = geom.transform(espgdest, epsgsrc)
  addFeatures()
}


map.on('click', function (e) {
  var coordinate = e.coordinate;
  map.forEachFeatureAtPixel(e.pixel, function (f, l) {

	polysource.clear()
	bobasource.clear()
	if (newfeat !== null) {
	  var oldid  = newfeat.get('id')
	  newfeat.setStyle(undefined);
	  newfeat = null

	}
	newfeat = f
	if (l.get('name') == 'areas'){
	  $('#areaSelect').val(f.get('id'))
	  $('#areaSelect').change();
	} else {
	  var contenttext = '<h5>'+ f.get('name') +'</h5>';
	  contenttext = contenttext + '<div class="row">'
	  //contenttext = contenttext + '<div class="col-6"><a href="/media" type="button" class="btn btn-primary float-end m-1" title="View report for default values">View report</a></div>'
	  {% if user.is_authenticated %}
	  contenttext = contenttext + '<div class="col-6"><button type="button" class="btn btn-primary m-1"  data-bs-toggle="button" autocomplete="off" title="Add feature to own areas" id="basinbound" onclick="addBB()">Add</button></div>';
	  {% endif %}
	  contenttext = contenttext + '</div>'
	  content.innerHTML = contenttext;

	  var ext = newfeat.getGeometry().getExtent();
	  bobasource.addFeature(newfeat);
	  var center = ol.extent.getCenter(ext);
	  map.getView().fit(ext, map.getSize());
	  overlay.setPosition(coordinate);
	}
  })
})

function getReport() {
  var area = $('#areaSelect').val();
  var start = $('#startdate').val();
  var end = $('#enddate').val();
  var precip = $('#precip').val();
  var et = $('#et').val();

  if (area == 'noarea') {
	$("#returnText").text("");
	$("#returnText").text("Please select an area to get the report")
	$("#returnModal").modal('show');
	return
  }

  $.ajax({
	type: "POST",
	url: "/getreport",
	data: { id: area, start: start, end: end, precip: precip, et: et}
  }).done(function( msg ) {
	$("#returnText").text("");
	$("#returnText").text(msg['result'] +
	"   You will receive an email with link to the report within 5 - 10 minutes, once it is ready.")
	$("#returnModal").modal('show');
	sleep(6000);
	getTasks();
  }).fail(function (msg) {
	$("#returnText").text("");
	$("#returnText").text(msg['result'])
	$("#returnModal").modal('show');
  })
}

$('#et').change(function() {
  checkDataConstraint();
})

$('#precip').change(function() {
  checkDataConstraint();
})

$('#areaSelect').change(function() {
  polysource.clear()
  var element = $(this).find(':selected')
  if (element.data('geom') === undefined) {
	  return
	}
  var geom = element.data('geom')
  var myname = element.text()
  var myid = element.val()
  newfeat = new ol.Feature({geometry: new ol.geom.MultiPolygon(geom['coordinates']).transform(espgdest,epsgsrc), name: myname, myid})
  newfeat.setId(myid)
  var ext = newfeat.getGeometry().getExtent();
  polysource.addFeature(newfeat);
  var center=ol.extent.getCenter(ext);
  map.getView().fit(ext, map.getSize());
  checkDataConstraint();
})

function readFile(input) {
  file = input.files[0];
}

function addLayer() {
  var reader = new FileReader();
  reader.readAsText(file, 'UTF-8');
  reader.onload = shipOff;

  function shipOff(event) {
	var result = event.target.result;
	$.ajax({
	  type: "POST",
	  url: "/addlayer",
	  data: { namecol: $("#customName").val(), file: result}
	}).done(function( msg ) {
	$("#addLayer").modal('hide');
	$("#returnText").text("")
	$("#returnText").text(msg['result']);
	$("#returnModal").modal('show');
	getAreas();
  }).fail(function (msg) {
	$("#addLayer").modal('hide');
	$("#returnText").text("");
	$("#returnText").text(msg.responseJSON['result']);
	$("#returnModal").modal('show');
	getAreas();
  });
  }
}

function addyear(){
  var today = new Date()
  //var thisyear = today.getFullYear()
  var thisyear = 2020
  for (i=2010; i<=thisyear; i++) {
	 if (i == 2010) {
	   $('#startdate').append('<option value="' + i + '" selected>' + i + '</option>')
	 } else {
	   $('#startdate').append('<option value="' + i + '">' + i + '</option>')
	 }
	 if (i == thisyear) {
	   $('#enddate').append('<option value="' + i + '" selected>' + i + '</option>')
	 } else {
	   $('#enddate').append('<option value="' + i + '">' + i + '</option>')
	 }
  }
}

window.addEventListener('resize', checkSize);

$(document).ready(function() {
  osmlayer.setVisible(false);
  otmlayer.setVisible(true);
  window.addFeatures = function() {
	$.ajax({
	  type: "POST",
	  url: "/addfeature",
	  data: { name: $("#featName").val(), geom:  $("#featGeom").val()}
	}).done(function( msg ) {
	  $("#drawModal").modal('hide');
	  $("#returnText").text("");
	  $("#returnText").text(msg['result'])
	  $("#returnModal").modal('show');
	  addid = msg['featid'];
	  getAreas(addid);
	}).fail(function (msg) {
	  $("#drawModal").modal('hide');
	  $("#returnText").text("");
	  $("#returnText").text(msg.responseJSON['result']);
	  $("#returnModal").modal('show');
	  getAreas();
	});
  }

  window.getAreas = function( myid ) {
	$.ajax({
	  type: "GET",
	  url: "/getareas"
	}).done(function( msg ) {
	  $('#areaSelect').find('option').remove().end().append('<option value="noarea" id="noarea">Select an area</option>').val('noarea')
	  areasource.clear()
	  for (i=0; i<msg['features'].length; i++) {
		if ( msg['features'][i]['id'] == myid) {
		  $('#areaSelect').append("<option selected value=" +
		   msg['features'][i]['id'] + " data-geom='" + JSON.stringify(msg['features'][i]['geometry']) + "' class='areatoselect'>" +
		   msg['features'][i]['properties']['name'] + "</option>");
		} else {
		  $('#areaSelect').append("<option value=" +
		   msg['features'][i]['id'] + " data-geom='" + JSON.stringify(msg['features'][i]['geometry']) + "' class='areatoselect'>" +
		   msg['features'][i]['properties']['name'] + "</option>");
		}
		var geom = new ol.geom.MultiPolygon(msg['features'][i]['geometry']['coordinates']).transform(espgdest,epsgsrc)
		var newfeat = new ol.Feature({geometry: geom, name: msg['features'][i]['properties']['name'], id: msg['features'][i]['id']})
		newfeat.setId(msg['features'][i]['id'])
		areasource.addFeature(newfeat);
	  }
	  $('#areaSelect').change();
	})
  }

  window.deleteTaskhistory = function(taskid) {
	$.ajax({
	  type: "GET",
	  url: "/deletetaskhistory/" + taskid
	}).done(function( msg ) {
	  getTasks();
	  $("#returnText").text("");
	  $("#returnText").text(msg['result'])
	  $("#returnModal").modal('show');
	}).fail(function (msg) {
	  $("#returnText").text("");
	  $("#returnText").text(msg['result'])
	  $("#returnModal").modal('show');
	})
  }

  window.getTasks = function () {
	$.ajax({
	  type: "GET",
	  url: "/gettasks"
	}).done(function( msg ) {
	  $("#previoustasks").text("");
	  var tasks = '<h5 class="card-title text-center">Previous task succefully finished</h5>'
	  for (i=0; i<msg['data'].length; i++) {
		tasks += '<div class="row"><div class="col-sm-12 col-lg-5">' + msg['data'][i]['fields']['area'] + "<br>" + msg['data'][i]['fields']['data'].replace('T', ' ').split('.', 1) + '</div>' +
				 '<div class="col-sm-12 col-lg-7"><a href="/media/' + msg['data'][i]['fields']['task'] + '/index.html" target="_blank" class="btn btn-primary m-1">view</a>' +
				 '<a href="/media/' + msg['data'][i]['fields']['task'] + '/report.pdf" target="_blank" class="btn btn-primary m-1">pdf</a>' +
				 '<a onclick="deleteTaskhistory(' + msg['data'][i]['id'] + ')" class="btn btn-primary m-1">delete</a></div></div>'
		if (i != msg['data'].length - 1) {
		  tasks += '<hr>';
		}
	  }
	  $("#previoustasks").append(tasks);
	})
  }
  checkSize();
  getAreas();
  addyear();
  getTasks();
  $.getJSON('/static/data/wapor_bound.geojson', function(data){
	features = data.features;
	for (var i = 0, len = features.length; i < len; i++) {
	  wapor_source.push(features[i]);
	}
  })
})
  </script>
