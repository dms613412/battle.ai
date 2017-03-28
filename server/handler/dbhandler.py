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

import json


class DBHandler(object):
    def __init__(self):
        self.conn = None
        self.db = None

        self.users = None
        self.game_log_list = []


    def insert_user(self, user):
        raise Exception

    def update_user_info(self):
        pass

    def update_game_log(self, game_result, user):
        raise Exception

    def update_user_gamelog(self, game_log):
        raise Exception

    def search_log(self):
        pass


    def putout(self):
        """
        for counting game logs
        """
        pass

dbh = DBHandler()
print(json.dumps(dbh.__dict__))


