google.load("jquery", "1.7.1");

var map;
var infowindow = new google.maps.InfoWindow();
var iterator = 0;

function initialize() {
    var latlng = new google.maps.LatLng(23.26, 0);
    var myOptions = {
        zoom: 3,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map"), myOptions);
    google.maps.event.addListener(map, 'click', function() {
        if (infowindow) {
            infowindow.close();
        }
    });
}

function addMarker(name, val){
    var pos = new google.maps.LatLng(val['lat'], val['lng']);
    var locName = name.replace(/\+/g, ' ')
    var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: pos,
        title: locName,
        animation: google.maps.Animation.DROP,
    });
    google.maps.event.addListener(marker, 'click', function() {
        if (infowindow) {
            infowindow.close();
        }
        infowindow = new google.maps.InfoWindow({'content': "<b>"+locName+"</b>"});
        infowindow.open(map, this);
    });
}

window.onload = function() {
    initialize();

    $.getJSON('holiday.json', function(data) {
        $.each(data, function(name, val) {
            setTimeout(function() {
                addMarker(name, val);
            }, iterator * 100);
            iterator++;
        });
    });
}

