console.log("Our Script is running")
function initMap() {
    console.log("Initializing Map")
    // initialize our geocoder
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': document.getElementById("location").innerHTML }, function (results, status) {
        if (status == 'OK') {
            console.log(results)
            const map = new google.maps.Map(document.getElementById("map"), {
                zoom: 4,
                center: results[0].geometry.location,
            });
            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location,
                zoom: 8
            });
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}