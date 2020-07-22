var socket = new WebSocket(`ws://${window.location.host}/ws`);
var result = 0;

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

socket.onmessage = async function(event){
    console.log(event.data)
    result = await eval(event.data)
    socket.send('result: ' + result)
}

// var health_check = window.setInterval(function(){socket.send('result: ' + result)}, 2000);
