function startGame () {
	socket.emit("game msg", {room: room, data: {type: "start"}}
}

function dilemmaInput (decision) {
	socket.emit("game msg", {room: room, data: {type: "decision", decision: decision}})
	
	let tagToReplace = document.querySelector("#content")
	if (decision == "defect") {
		tagToReplace.innerHTML = "You defected!"
	}
	else { 
		tagToReplace.innerHTML = "You cooperated!"
	}
}
