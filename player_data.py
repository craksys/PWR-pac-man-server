class Data:
    players = {}
    champions = {}

    def add_player(self, player_id, nick, ip, port, state, ready):
        Data.players[player_id] = {
            'nick': nick,
            'ip': ip,
            'port': port,
            'state': state,
            'ready': ready
        }

    def add_champion(self, champion_id, nick, port, characterID):
        Data.champions[champion_id] = {
            'nick': nick,
            'port': port,
            'characterID': characterID
        }

    def check_characterID_in_champions(self, characterID):
        for champion in Data.champions.values():
            if champion['characterID'] == characterID:
                return True
        return False

    def return_player_state(self, port):
        players_c = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                players_c.append(player_id)
                return player_data['state']
        return -1

    def change_player_state(self, port, state):
        players_c = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                players_c.append(player_id)
                player_data['state'] = state

    def change_player_ready(self, port, ready):
        players_c = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                players_c.append(player_id)
                player_data['ready'] = ready

    def remove_player_by_port(self, port):
        players_to_remove = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                players_to_remove.append(player_id)
        for player_id in players_to_remove:
            del Data.players[player_id]

    def remove_champion_by_port(self, port):
        champions_to_remove = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                champions_to_remove.append(player_id)
        for player_id in champions_to_remove:
            del Data.champions[player_id]

    def return_nick_by_port(self, port):
        players_c = []
        for player_id, player_data in Data.players.items():
            if player_data['port'] == port:
                players_c.append(player_id)
                return player_data['nick']