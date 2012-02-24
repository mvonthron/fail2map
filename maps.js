google.load("jquery", "1.7.1");

var map;
var infowindow = new google.maps.InfoWindow();
var marker;


function initialize() {
    var latlng = new google.maps.LatLng(0, 0);
    var myOptions = {
        zoom: 3,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map"), myOptions);
}

window.onload = function() {
    initialize();

    $.getJSON('holiday.json', function(data) {
        $.each(data, function(key, val) {
            var pos = new google.maps.LatLng(val['lat'], val['lng']);
            map.setCenter(pos);
            var marker = new google.maps.Marker({
                map: map,
                position: pos
            });
       });
    });
}

