google.load("jquery", "1.7.1");
var geocoder;
var map;
var infowindow = new google.maps.InfoWindow();
var marker;

function initialize() {
    geocoder = new google.maps.Geocoder();
    var latlng = new google.maps.LatLng(0, 0);
    var myOptions = {
        zoom: 3,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map"), myOptions);
}

/* You will get a position from an address */
function geocodeAddress(address) {
    geocoder.geocode( { 'address': address }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var coords = results[0].geometry.location
            map.setCenter(coords);
            var marker = new google.maps.Marker({
                map: map,
                position: coords
            });
        }
        return status;
    });
}

function chunk(array, process, context){
    var items = array.concat();   //clone the array
    setTimeout(function(){
        var item = items.shift();
        process.call(context, item);

        if (items.length > 0){
            setTimeout(arguments.callee, 100);
        }
    }, 100);
}

function pausecomp(millis){
  var date = new Date();
  var curDate = null;
  do { curDate = new Date(); }
  while(curDate-date < millis);
}

window.onload = function() {
    initialize();
    var txtFile = new XMLHttpRequest();
    txtFile.open("GET", "locations.txt", true);
    txtFile.onreadystatechange = function() {
        if ( (txtFile.readyState === 4) && (txtFile.status === 200) ) {
            allText = txtFile.responseText;
            locations = txtFile.responseText.split("\n");
            chunk(locations, function(item){
                if (item == '') { return 0; }
                item = item.replace(/ /gi, '+');
                var stats = geocodeAddress(item);
                if ( stats != google.maps.GeocoderStatus.OK) {
                    // Sleep 1s and retry
                    pausecomp(800);
                    geocodeAddress(item);
                }
            });
        }
    }
    txtFile.send(null);
}

