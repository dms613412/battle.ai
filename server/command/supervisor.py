import tornado.ioloop
import game.omok.OMOKPlayer
import random

from server.gameobject.room import Room
from server.handler.turngamehandler import TurnGameHandler
from gamebase.client.Player import Player, play
from game.omok.CustomOMOKLogic import CustomOMOKLogic
from multiprocessing import Process

MATCH = "match"
VIEW = "view"
CREATE = "create"
USER = "user"
PROCESS = "process"
KILL = "kill"
ALL = "all"
players = None

WRONG_COMMAND = "WRONG COMMAND"



controled_process = []

def start_commandline(player_list=None):
    global players
    players = player_list
    while True:
        try:
            command = input(">> ")
            parsed_command = command.split(' ')

            main_command = parsed_command[0]
            args_command = parsed_command[1:]

            if main_command == VIEW:
                view(*args_command)
            elif main_command == MATCH:
                match(*args_command)
            elif main_command == CREATE:
                create_player()
            elif main_command == KILL:
                kill(*args_command)
        except Exception as e:
            print(str(e))


def kill(*args):
    sub_command = args[0]
    if sub_command == ALL:
        for p in controled_process:
            p.terminate()
        controled_process.clear()
    else:
        print(WRONG_COMMAND)


def match(*args):
    if len(players) < 2:
        print("There is no enough players")
        return
    if len(args) == 0:
        player_list = list(players.values())
        match_list = []
        while len(match_list) != 2:
            random_index = random.randrange(0, len(player_list))
            pick_me_up = player_list[random_index]
            if pick_me_up.playing is False:
                pick_me_up.room_enter()
                match_list.append(pick_me_up)

        print(match_list)
        room = Room(match_list)
        game_server = TurnGameHandler(room, [], [])
        tornado.ioloop.IOLoop.current().spawn_callback(game_server.run)
    else:
        first_index = args[0]
        second_index = args[1]

        player_list = list(players.values())
        room = Room([player_list[first_index], player_list[second_index]])
        game_server = TurnGameHandler(room, [], [])
        tornado.ioloop.IOLoop.current().spawn_callback(game_server.run)


def view(*args):
    sub_command = args[0]
    if sub_command == USER:
        view_all_users()
    elif sub_command == PROCESS:
        view_all_process()
    else:
        print(WRONG_COMMAND)

def view_all_users():
    global players
    count = 0
    for pid in players.keys():
        print(str(count) + ": " + pid)
        count += 1

def view_all_process():
    for p in controled_process:
        print(p)

def create_player():
    # make new process and run player
    game_logic = CustomOMOKLogic()
    p = Process(target=play, args=(game_logic, ))
    p.start()
    controled_process.append(p)
    pass

if __name__ == "__main__":
    start_commandline()

