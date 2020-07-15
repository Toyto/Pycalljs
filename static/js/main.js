var socket = new WebSocket(`ws://${window.location.host}/ws`);

socket.onopen = function(){
    console.log('Connection is set.')
}

socket.onclose = function(event){
    if (event.wasClean){
        console.log('Connection is closed.')
    } else {
        console.log('Connection is broken.')
    }
}

socket.onmessage = function(event){
    console.log(event.data)
}

var health_check = window.setInterval(function(){socket.send('Test server')}, 5000);
