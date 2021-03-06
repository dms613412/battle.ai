# -*- coding: utf-8 -*-

import functools
import json
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.tcpserver
import tornado.web
import tornado.websocket
from tornado import gen

from server.string import *
from server.gameobject.user import Player


class PlayerHandler(tornado.tcpserver.TCPServer):
    def __init__(self, attendee_list, player_list):
        tornado.tcpserver.TCPServer.__init__(self)
        self.player_list = player_list
        self.attendee_list = attendee_list

    def handle_stream(self, stream, address):
        """
        when ai client connect to server this function is run
        and spawn_callback (__accept handler)
        :param stream: ai client's stream
        :param address:  ai client's ip address
        """
        tornado.ioloop.IOLoop.current().spawn_callback(self.__accept_handler, stream)

    @gen.coroutine
    def __accept_handler(self, stream):
        '''
        this function accept user_id
        receive protocol is
            msg = {"msg" : "user_info", "msg_type" : "init", "data" : {"username" : userid }}
        if user_id is valid - return y
        else - return n

        :param stream:  player's stream
        '''
        # TODO : set protocol of user_info, and handle exception of every case
        # TODO: overall correction is needed in nearby this.
        player = Player(None, stream)
        try:
            while True:
                message = yield player.read()
                message = json.loads(message)

                username = message[DATA]["username"]

                if username in self.player_list.keys():
                    msg = {MSG: USER_INFO, MSG_TYPE: INIT, DATA: {RESPONSE: NO}}
                    json_data = json.dumps(msg)
                    stream.write(json_data.encode())
                    continue
                else:
                    break

            player = Player(username, stream)
            message = {MSG: USER_INFO, MSG_TYPE: INIT, DATA: {RESPONSE: OK}}
            message = json.dumps(message)
            player.send(message)
            logging.info(username + " enter BATTLE.AI")

            self.player_list[username] = player
            for attendee in self.attendee_list.values():
                logging.debug("user notify added");
                attendee.notice_user_added(username)

            on_close_func = functools.partial(self._on_close, username)
            stream.set_close_callback(on_close_func)
        except Exception as e:
            logging.error(e)
            msg = {MSG: USER_INFO, MSG_TYPE: INIT, DATA: {RESPONSE: NO}}
            json_data = json.dumps(msg)
            stream.write(json_data.encode())

    def _on_close(self, username):
        '''
        when stream is closed this funciton is run
        :param username: ai client user name
        '''
        logging.info(str(username)+" out from BATTLE.AI")
        try:
            self.player_list.pop(username)
        except Exception:
            pass

        for attendee in self.attendee_list.values():
            attendee.notice_user_removed(username)
