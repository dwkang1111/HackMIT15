

var locRequest = new XMLHttpRequest();
locRequest.open("POST", "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCAkuONPpkcHqvjlhdbss2ZtzfURWffji8", false);
locRequest.send();

var loc =  locRequest.response;
var locJson = JSON.parse(loc);
var lati = locJson.location.lat;
var lngi = locJson.location.lng;
var radius = locJson.accuracy;

var addrRequest = new XMLHttpRequest();
var url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lati+","+lngi+"&key=AIzaSyCAkuONPpkcHqvjlhdbss2ZtzfURWffji8";
addrRequest.open("POST", url, false);
addrRequest.send();

var addr = addrRequest.response;
var addrJson = JSON.parse(addr);
var address = addrJson.results[0].formatted_address;



