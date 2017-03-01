import json
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
from server.gameobject.room import Room

from server.handler.turngamehandler import TurnGameHandler
from server.string import *
from server.gameobject.user import Observer


class ObserverHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, observer_list=dict(), player_list=dict(), database=None):
        '''

        :param observer_list:
        :param player_list:
        :param gamehandler:
        '''
        self.observer_list = observer_list  # dict() - key : conn
        self.player_list = player_list  # dict() - key : user_id\
        self.database = database

        logging.debug("Web soscket initialization is done")

    def open(self, *args, **kwargs):
        '''
        open websocket
        '''
        new_observer = Observer(self)
        self.observer_list[self] = new_observer

    def on_message(self, message):
        '''
        When receive message from Observer, this function runs.
        :param message: message from Observer
        '''
        logging.debug(message)
        request = json.loads(message)
        try:
            msg = request[MSG]
            if msg == REQUEST+MATCH:
                self._response_match(request[DATA])
            elif msg == REQUEST+USER_LIST:
                self._response_user_list()
            else:
                pass
        except Exception:
            pass

    def _response_user_list(self):
        self.observer_list[self].observer_flag = False

        players = list(self.player_list.keys())

        msg = {MSG: RESPONSE_ + USER_LIST, USERS: players}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
        except Exception as e:
            logging.error("error in response_user_list")
            self.observer_list.pop(self)

    def _response_match(self, data):
        try:
            players = [self.player_list.pop(pid) for pid in data[USERS]]
            logging.error(type(data[USERS][0]))
        except Exception as e:
            logging.error(e)
            return
        for pid in data[USERS]:
            for observer in self.observer_list.values():
                observer.notice_user_removed(pid)
        try:
            room = Room(players, self.observer_list[self])
            # TODO: factory design is needed in here
            game_server = TurnGameHandler(room, self.player_list, self.observer_list, int(data[SPEED]))
        except Exception as e:
            logging.error(e)
            logging.error("During making room, error is occured")
            return

        # run game
        tornado.ioloop.IOLoop.current().spawn_callback(game_server.run)
        speed_list = [0.5, 0.3, 0.1, 0.05, 0]
        msg = {MSG: RESPONSE_ + MATCH, DATA: {USERS: data[USERS], ERROR: 0, SPEED: speed_list[int(data[SPEED])]}}
        json_msg = json.dumps(msg)

        try:
            self.write_message(json_msg)
            self.observer_list[self].room_enter()
        except Exception as e:
            logging.error(e)
            self.observer_list.pop(self)

    # TODO : find out how to deal with this error (CORS)
    def check_origin(self, origin):
        return True

    def on_close(self):
        self.observer_list.pop(self)
