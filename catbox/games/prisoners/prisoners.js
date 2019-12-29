function startGame () {
	socket.emit("game msg", {room: room, data: {type: "start"}})
}

function dilemmaInput (decision) {
	socket.emit("game msg", {room: room, data: {type: "decision", cooperate: decision}})
	
	let tagToReplace = document.querySelector("#content")
	if (decision === false) {
		tagToReplace.innerHTML = "You defected!"
	}
	else { 
		tagToReplace.innerHTML = "You cooperated!"
	}
}
