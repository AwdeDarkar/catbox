function startGame () {
	socket.emit("game msg", {room: room, data: {type: "start"}}
}


function dilemmaInput (decision) {
	socket.emit("game msg", {room: room, data: {type: "decision", cooperate: decision}}
}
