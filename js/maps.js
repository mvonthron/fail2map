var map;
var markersLayer;
var heatmapDataset = [];

function addLabel(feature, layer) {
    if (feature.properties && feature.properties.name) {
        layer.bindLabel('<b>'+feature.properties.name+'</b>');
    }
}

function show(feature, layer){
    return feature.properties.show_on_map;
}

function addFeature(feature){
    markersLayer.addLayer(L.geoJson(feature, {
        onEachFeature: addLabel,
        filter: show
    }));

    heatmapDataset.push({
        lon: feature.geometry.coordinates[0],
        lat: feature.geometry.coordinates[1]
    });
}

function finishInit(){
    heatmapLayer.setData(heatmapDataset);
    markersLayer.addTo(map);

    overlays = {
        "Markers": markersLayer,
        "Heatmap": heatmapLayer
    };

    L.control.layers(overlays, null, {collapsed: false})
        .setPosition("bottomleft")
        .addTo(map);
}

window.onload = function() {
    map = L.map('map').setView([23.26, 0], 3);
    
    // list of tile providers can be seen here: http://leaflet-extras.github.io/leaflet-providers/preview/
    baseLayer = L.tileLayer.provider('Thunderforest.Landscape', {
        // write options and credentials here
        // id: 'MAPBOX_ID',
        // accessToken: 'MAPBOX_TOKEN'
    }).addTo(map);

    markersLayer = L.geoJson();

    heatmapLayer = L.TileLayer.heatMap({
        radius: { value: 40, absolute: false },
        opacity: 1,
        gradient: {
            0.45: "rgb(0,0,255)",
            0.55: "rgb(0,255,255)",
            0.65: "rgb(0,255,0)",
            0.95: "rgb(255,0,0)"
        }
    });

    $.getJSON('places.geojson', function(data) {
        $.each(data.features, function(i, feat) {
            addFeature(feat);
        });
        finishInit();
    });

}
