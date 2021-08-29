
const localmap = new ol.Map({
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        })
    ],
    target: 'map',
    view: new ol.View({
        center: ol.proj.transform([39.184, 51.672], 'EPSG:4326', 'EPSG:3857'),
        zoom: 8
    })
});

localmap.on('singleclick', function(evt) {
    coords = ol.proj.transform(evt.coordinate, 'EPSG:3857', 'EPSG:4326');
    $('#task-lat').val(coords[1]);
    $('#task-lon').val(coords[0]);
});
