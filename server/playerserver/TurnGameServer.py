#-*- coding:utf-8 -*-
import json
from tornado import gen
from gameLogic.baskin.baskinServer import BaskinServer
from gameLogic.baseClass.dummy_game import DiceGame
from server.playerserver.GameServer import GameServer

class TurnGameServer(GameServer):
    def __init__(self, room, battle_ai_list):
        game_logic = DiceGame(self)
        self.room = room
        GameServer.__init__(self, room, battle_ai_list, game_logic)
        self.num = 0

    @gen.coroutine
    def game_handler(self):
        try:
            turn = self.selectTurn(self.room.player_list)
            self.game_logic.onStart(turn)
            print "START"
            for player in turn:
                self.q.put(player)
                self.__player_handler(player)
            yield self.q.join()
        except:
            self.game_logic.onError()
            print "[!] ERROR"
        finally:
            print "END"
            # self.game_logic.onEnd()

    def request(self, player, msg, gameData):
        self.current_msgtype = msg

        data = { "msg" : "game_data", "msg_type" : msg , "game_data" : gameData }
        json_data = json.dumps(data)
        player.send(json_data)

        '''
        for attendee in self.room.attendee_list:
            attendee.send(json_data)
        '''

    @gen.coroutine
    def __player_handler(self, player):
        while True:
            print "Player handler running"
            message = yield player.read()
            res = json.loads(message)
            print res
            if res["msg_type"] == self.current_msgtype:
                recv = self.game_logic.onAction(player, message)
                print recv
                if not recv:
                    raise Exception
                else:
                    pass
                    # for attendee in self.room.attendee_list:
                    #     attendee.send(message)
            elif res["msg_type"] == 0:  ## end는 종료 메세지 타입
                self.q.get()
                self.q.task_done()
                break
            else:
                raise Exception

    def onEnd(self, isValidEnd, result):
        ## isValidEnd
        ## 0. 비정상 종료
        ## 1. 정상 종료
        ## result = {"player_pid" : "승패" ... }

        print "onEnd is running"
        data = { "msg" : "game_result", "msg_type" : "normal", "game_data" : result }

        if isValidEnd == 0:
            data["msg_type"] = "abnormal"

        for player in self.battle_ai_list:
            json_data = json.dumps(data)
            player.send(json_data)

        print "onEnd is end"