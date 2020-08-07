// We will use a post to send the location 
// so we need csrf token and we will grab that csrf token from cookies
// for csrf token - 
// https://bit.ly/33dYPW7
// https://stackoverflow.com/a/13515414/11121579

function getLocation(){
    // This function will be called when we click detect location button
    if(navigator.geolocation){
        // getCurrentPosition requires a function as argument
        // getPosition function will get the location = (latitude and longitude) of the device
        // anyError function will be triggered if there is an error
        // Link below if for geolocation API
        // https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
          }; 
        navigator.geolocation.getCurrentPosition(getPosition, anyError,options);
    }
    else{
        alert('Geolocation service is not supported by your device.');
    }
}

function getPosition(position){
    // Extracting position information
    let location = {
        'latitude':position.coords.latitude,
        'longitude':position.coords.longitude,
    }
    // Send data using AJAX
    send_data(location)
}

function anyError(error){
    // show error
    alert(error.message)
}

function send_data(loc_data){
    let csrftoken = get_csrftoken(document.cookie); // storing csrf token
    let user_pref = user_preferences()
    // sending AJAX request to homepage.
    // we need to set csrf token to the header of request before sending the it.
    xhr = new XMLHttpRequest()
    xhr.open('POST','/wheather/',true)
    xhr.setRequestHeader("X-CSRFToken", csrftoken)
    xhr.send(
        {
            location:loc_data,
            pref:user_pref
        }
    )
    console.log('data sent')
}

function get_csrftoken(cookie){
    // we need csrf token from cookies, so extract it with regexp
    let pat = /csrftoken=(\w+)(?:;?)/gm;
    return pat.exec(cookie)[1];
}

function user_preferences(){
    // All user preferences are taken.
    // Here we dont require city name as we are getting coordinates.
    user_pref = {}
    user_pref['unit'] = $('#unit').val(),
    user_pref['language'] = $('#language').val(),
    user_pref['tz'] = $('#tz').val()
    return user_pref
}
