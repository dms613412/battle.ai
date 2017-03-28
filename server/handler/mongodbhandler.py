"""
structure description

all json format var keep convention Camel
ex) findViewById ...

[user]
{
  _id: (string),
  name: (string),
  password: (string),
  imageUrl: (string), -- optional
  gitHubId: (string) -- optional
}
* _id: key value that identifies user in server
* name: name that user choose
* password: password ...

[game_log]
{
  game_id: (string),
  winner: [(string), (string) ..],
  loser: [(string), (string), ..],
  drawer: [(string), (string) ...]
}

* game_id: key value that identifies game in server
* winner: winner's _id list
* loser: loser's _id list
* drawers: drawer's _id list

Copyright by junsu
"""

from server.handler.dbhandler import DBHandler
import pymongo
import pprint

IP = "localhost"
PORT = 9090


class MongoDBHandler(DBHandler):
    def __init__(self):
        super(MongoDBHandler, self).__init__()
        self.conn = pymongo.MongoClient(IP, PORT)
        self.db = self.conn.playgroundDB

    def init_db(self):
        self.users = self.db.users
        self.game_log_list = self.db.game_log_list

    def insert_user(self, user):
        self.users.insert_one(user)

    def update_game_log(self, game_result):
        self.game_log_list.insert_one(game_result)

    def update_user_gamelog(self, game_log):
        """
        ????????
        """
        self.users.update(game_log)

    def search_log(self, userid):
        win_c = 0
        lose_c = 0
        draw_c = 0

        for game in self.game_log_list.find():
            win_c += game.find({'winner': userid})
            lose_c += game.find({'loser': userid})
            draw_c += game.find({'drawer': userid})
        print('win:' + win_c + ', lose: ' + lose_c + ', draw:' + draw_c)

    def putout(self):
        """
        for counting game logs
        """
        pass