

# NOTE: if a player has not disconnected, do not allow someone else to take
# (on a player disconnect, remove sid from dictionary [set to none?])


class Game():

    def __init__():
        self.code = "AAAA"
        self.players = {}


    def add_player(username, sid):
        if username in self.players.keys():
            if self.players[username] is not None:
                # TODO: error message
                pass
            else:
                self.players[username] = sid
        else:
            self.players[username] = sid
            # TODO: send event to clients?
            
        
