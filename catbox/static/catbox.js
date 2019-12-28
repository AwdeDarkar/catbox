/**
 * catbox
 * ------
 * Core catbox js library
 */

var socket
var connected = false // eslint-disable-line no-unused-vars

function ConnectSocket () {
    socket = io.connect("http://" + document.domain + ":" + location.port)
    socket.on("connect", function () { connected = true })
    // TODO: error handling if connection goes wrong?
}

function ConnectionFormHandler (e) {
    e.preventDefault()
    var code = $("#connection_code").val()
    var username = $("#connection_code").val()
    socket.emit("join", {
        code: code,
        username: username,
    })
}

function OnPageLoad () { // eslint-disable-line no-unused-vars
	console.log("Hello world!");
    ConnectSocket()
    var form = $("connection_form").on("submit", ConnectionFormHandler)
    $("#connection_username").val("").focus()
}

console.log("hello?");
OnPageLoad();
