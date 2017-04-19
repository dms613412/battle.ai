'''
battle.ai

playground is ai battle framework for
1:1:1:1: ... turn game.
'''

import os.path
import sys
import tornado.ioloop
import tornado.options
import tornado.web
import _thread

sys.path.insert(0, '../')
# TODO : find out how to control path and error
from server.command.supervisor import *
from server.handler.playerhandler import PlayerHandler
from server.handler.observerhandler import ObserverHandler
from server.conf.conf_reader import ConfigReader
from server.handler.webpagehandler import *


player_list = dict()


class Playground(tornado.web.Application):
    def __init__(self):
        # TODO: game_logic selection must be added, tcp_port, web_port, playing game will be argument of playground.py

        global player_list
        self.player_list = player_list
        self.attendee_list = dict()

        self.tcp_server = PlayerHandler(self.attendee_list, self.player_list)

        super(Playground, self).__init__()


def main():

    config = ConfigReader()
    config_value = config.read()

    tcp_port = config_value["tcp_port"]
    web_port = config_value["web_port"]

    tornado.options.parse_command_line()
    tornado.options.parse_config_file("my.conf")
    app = Playground()

    io_loop = tornado.ioloop.IOLoop.current()
    app.tcp_server.listen(tcp_port)
    app.listen(web_port)

    print("******************* Battle.AI operate *******************")
    print("                     ...... Created By GreedyOsori ......\n")

    global player_list
    _thread.start_new_thread(start_commandline, (player_list,))

    io_loop.start()

if __name__ == "__main__":
    main()

