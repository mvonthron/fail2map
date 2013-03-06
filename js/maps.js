var map;

function addLabel(feature, layer) {
    if (feature.properties && feature.properties.name) {
        layer.bindLabel('<b>'+feature.properties.name+'</b>')
    }
}

function show(feature, layer){
    return feature.properties.show_on_map;
}

function addFeature(feature){
   L.geoJson(feature, {
        onEachFeature: addLabel,
        filter: show,
    }).addTo(map);
}
window.onload = function() {
    map = L.map('map').setView([23.26, 0], 3);
    L.tileLayer("http://{s}.tiles.mapbox.com/v3/examples.map-4l7djmvo/{z}/{x}/{y}.png", {
         maxZoom: 18,
         subdomains: ["a", "b", "c", "d"],
         attribution: '<a href="http://mapbox.com/about/maps">Terms & Feedback</a>'
    }).addTo(map);

   $.getJSON('places.geojson', function(data) {
        $.each(data.features, function(i, feat) {
            addFeature(feat);
        });
    });
}
