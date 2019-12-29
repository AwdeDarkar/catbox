/**
 * catbox
 * ------
 * Core catbox js library
 */

var socket
var connected = false // eslint-disable-line no-unused-vars
var room = ""
var user = ""

function ConnectSocket () {
    socket = io.connect("http://" + document.domain + ":" + location.port)
    socket.on("connect", function () { connected = true })
    // TODO: error handling if connection goes wrong?
	
	socket.on("clear page", ClearPage)
	socket.on("display", DisplayHTML)
	socket.on("load js", AddJS)
	socket.on("load css", AddCSS)

	socket.on('reconnect', ()=>{ 
		socket.emit("join", {
			code: room,
			username: user,
		})
	});
}

function ConnectionFormHandler () {
	console.log("FORM SUBMISSION")
    var code = $("#connection_code").val()
    var username = $("#connection_username").val()
    socket.emit("join", {
        code: code,
        username: username,
    })
	room = code
	user = username
}

function OnPageLoad () { // eslint-disable-line no-unused-vars
	console.log("Hello world!");
    ConnectSocket()
    //$("#connection_form").on("submit", ConnectionFormHandler)
    $("#connection_username").val("").focus()
}

function ClearPage () {
	console.log("Clearing page")
	document.body.innerHTML = ""
	//$("link[href='fileToRemove.css']").remove();
	$("link").remove();
	
	var contentDiv = document.createElement("div");
	contentDiv.id = "content";
	document.body.appendChild(contentDiv);
	
	var audioDiv = document.createElement("div");
	audioDiv.id = "audio";
	document.body.appendChild(audioDiv);
}

function AddJS (data) {
	let url = data.url
	console.log("Adding js at '" + url + "'")
	var script = document.createElement('script');
	script.type = 'text/javascript';
	script.src = url;    
	document.head.appendChild(script);
}

function AddCSS (data) {
	let url = data.url
	console.log("Adding css at '" + url + "'")
	var stylesheet = document.createElement('link');
	stylesheet.type = 'text/css';
	stylesheet.href = url;    
	stylesheet.rel = "stylesheet"
	document.head.appendChild(stylesheet);
}

function DisplayHTML (data) {
	console.log(data)

	let tagToReplace = document.querySelector(data.replace)
	console.log("Replacing content of:");
	console.log(tagToReplace);
	
	//document.body.innerHTML = data.html
	tagToReplace.innerHTML = data.html
}

console.log("hello?");
OnPageLoad();
localStorage.debug = true;
localStorage.debug = '*';
