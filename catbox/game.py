

# NOTE: if a player has not disconnected, do not allow someone else to take
# (on a player disconnect, remove sid from dictionary [set to none?])


class Game():

    def __init__(self, server):
        self.server = server
        
        self.code = "AAAA"
        self.players = {}

        # TODO: queue for each player if they disconnect (add to queue if username sid is none, then send all when it is no longer onone)


    def add_player(self, username, sid):
        if username in self.players.keys():
            if self.players[username] is not None:
                # TODO: error message
                pass
            else:
                self.players[username] = sid
        else:
            self.players[username] = sid
            # TODO: send event to clients?
            
        
