
"""
_id : Server give identifier to player
name : Player's ID
password : Player's ID
"""

class Player(object):
    def __init__(self, _id, name, password):
        self._id = _id
        self.name = name
        self.password = password
    pass
