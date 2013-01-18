var map;
var iterator = 0;
function initialize() {
    map = L.map('map').setView([23.26, 0], 3);
	L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
      maxZoom: 18
    }).addTo(map);
}
function addMarker(name, val){
    var marker = L.marker([val['lat'], val['lng']]).addTo(map);
	marker.bindPopup('<b>'+locName+'</b>', {closePopupOnClick:true});
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