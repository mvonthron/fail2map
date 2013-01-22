var map;
var iterator = 0;
function initialize() {
    map = L.map('map').setView([23.26, 0], 3);
    L.tileLayer("http://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png", {
         maxZoom: 18,
         subdomains: ["otile1", "otile2", "otile3", "otile4"],
         attribution: 'Basemap tiles courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data &copy; <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
  }).addTo(map);
}
function addMarker(name, val){
    var locName = name.replace(/\+/g, ' ');
    var marker = L.marker([val['lat'], val['lng']]).addTo(map);
    marker.bindLabel('<b>'+locName+'</b>');
}
window.onload = function() {
    initialize();
    $.getJSON('places_gps_log.json', function(data) {
        $.each(data, function(name, val) {
            setTimeout(function() {
                if (val['lat'] != null){
                    addMarker(name, val);
                }
            }, iterator * 100);
            iterator++;
        });
    });
}
