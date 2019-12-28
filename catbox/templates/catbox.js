var socket;
var connected = false;


function ConnectSocket()
{
	socket = io.connect('http://' + document.domain + ':' + location.port);
	socket.on("connect", function() { connected = true; });
	// TODO: error handling if connection goes wrong?
}


function ConnectionFormHandler(e)
{
	e.preventDefault();
	code = $("#connection_code").val();
	username = $("#connection_code").val();
	socket.emit("join", {
		code: code,
		username: username 
	});
}


function OnPageLoad()
{
	ConnectSocket();
	var form = $("connection_form").on("submit", ConnectionFormHandler);
	$("#connection_username").val("").focus();
}
