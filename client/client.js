var socket = null;
var isopen = false;
var messages = [];


function sendText(){
    if(isopen){
        socket.send(JSON.stringify({
            'message': input.value,
            'channelName': channelinput.value
        }));
        console.log("message Sent");

    }
    else{
        console.log("Connection not accuried yet")
    }
}

window.onload = function(){
    var input = document.getElementById("input").value;
    var channelinput = document.getElementById("channelinput").value;
    console.log("I have Loaded");
    var name = prompt("Enter Your Name")
    document.getElementById('name').replaceWith("Hi "+name)
    
    socket = new this.WebSocket("ws://127.0.0.1:9000")
    socket.binaryType = "arraybuffer";
    socket.onopen = function(){
        console.log("connected!");
        isopen=true;
        socket.send(name);
    }
    socket.onmessage = function(e){
        messages.push(e.data);
        console.log("The Message Received is : " + e.data);
    }
    socket.onclose=function(){
        console.log("connection closed")
        socket=null;
        isopen=false;
    }
    
    
    
    
}


function Close(){
    socket.close();
    socket=null;
    isopen=false;
    console.log("connection closed");
}
function messagesReceived(){
    for (i=0;i<this.messages.length;i++){
        console.log(messages[i]);
    }
}
