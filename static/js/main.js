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

socket.onmessage = async function(event){
    var result = await eval(event.data)
    socket.send(result)
    console.log(result)
}

// var health_check = window.setInterval(function(){socket.send('Test server')}, 10000);
