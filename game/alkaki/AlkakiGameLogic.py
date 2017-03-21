import sys

from gamebase.game.Phase import Phase
from gamebase.game.TurnGameLogic import TurnGameLogic
import game.debugger as logging

sys.path.insert(0, '../')


class ALKAKIGameLogic(TurnGameLogic):
    def __init__(self, game_server):
        super(ALKAKIGameLogic, self).__init__(game_server)
        # Here init game dependent variable

    def on_ready(self, player_list):
        self._player_list = player_list

        # Here makes dict for multi player init variable
        init_dict = {}
        for i in player_list:
            init_dict[i] = {}

        # Send Server
        self._game_server.on_init_game(init_dict)

    def on_start(self):
        # shared_dict-init out of this class(Phase)
        shared_dict = self.get_shared_dict()

        # Register Phase (phase name free)
        game_phase = ALKAKIGamePhase(self, 'game')
        shared_dict['PHASE_GAME'] = self.append_phase(game_phase)

        # Transfer Phase GameLogic -> GamePhase
        self.change_phase(0)


class ALKAKIGamePhase(Phase):
    def __init__(self, logic_server, message_type):
        super(ALKAKIGamePhase, self).__init__(logic_server, message_type)

        # declare variable
        self.player_list = None
        self.shared_dict = None

    def on_start(self):
        super(ALKAKIGamePhase, self).on_start()

        # Init data
        self.player_list = self.get_player_list()
        self.shared_dict = self.get_shared_dict()

        # Init game independent data

        # Send server msg
        self.change_turn(0)
        self.request_to_server()

    def do_action(self, pid, dict_data):
        # check user decision
        super(ALKAKIGamePhase, self).do_action(pid, dict_data)

        # validate_user
        validate_user = 0
        if pid == self.player_list[0]:
            validate_user = 1
        elif pid == self.player_list[1]:
            validate_user = 2

        # Notify to Observer(Web) game data
        self.notify_to_observer()
        # Requests to Server(Handler) game data
        self.request_to_server()

    def notify_to_observer(self):
        notify_dict = {
            'data': 'test'
        }
        self.notify("game", notify_dict)

    def request_to_server(self):
        request_dict = {
            'data': 'test'
        }
        self.request(self.now_turn(), request_dict)
