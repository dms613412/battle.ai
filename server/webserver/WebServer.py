import tornado.ioloop
import tornado.websocket
import tornado.web
from server.User import Attendee

from server.Room import Room
from server.playerserver.TurnGameServer import TurnGameServer
import json
from server.m_format import *


class WebServer(tornado.web.RequestHandler):
    def get(self):
        # self.render("sample.html")
        self.render("index.html")


class WebSocketServer(tornado.websocket.WebSocketHandler):

    def initialize(self, web_client_list=dict(), battle_ai_list=dict(), player_server=None):
        self.web_client_list = web_client_list  # dict() - key : conn
        self.battle_ai_list = battle_ai_list  # dict() - key : user_id
        self.player_server = player_server  # PlayerServer

    def open(self, *args, **kwargs):
        new_attendee = Attendee(self)
        self.web_client_list[self] = new_attendee

    def on_message(self, message):
        request = json.loads(message)
        try:
            msg = request[MSG]
            if msg == REQUEST+MATCH:
                self._response_match(request[USERS])
            elif msg == REQUEST+USER_LIST:
                self._response_user_list()
            else:
                pass
        except Exception as e:
            print "wrong message"+e

    def _response_user_list(self):
        self.web_client_list[self].attendee_flag = False

        players = list(self.battle_ai_list.keys())

        msg = {MSG: RESPONSE+USER_LIST, USERS: players}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
        except Exception as e:
            print(e)
            self.web_client_list.pop(self)

    def _response_match(self, pid_list):
        try:
            players = [self.battle_ai_list.pop(pid) for pid in pid_list]
        except Exception as e:
            print e
            return

        for pid in pid_list:
            for attendee in self.web_client_list.values():
                attendee.notice_user_removed(pid)

        room = Room(players, self.web_client_list[self])
        game_server = TurnGameServer(room, self.battle_ai_list, self.web_client_list)

        tornado.ioloop.IOLoop.current().spawn_callback(game_server.game_handler)

        msg = {MSG: RESPONSE+MATCH, ERROR: 0, USERS: pid_list}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
            self.web_client_list[self].room_enter()
        except Exception as e:
            print(e)
            self.web_client_list.pop(self)

    # TODO : find out how to deal with this error (CORS)
    def check_origin(self, origin):
        return True

    def on_close(self):
        self.web_client_list.pop(self)
