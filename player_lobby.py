class Lobby:
    def __init__(self, data):
        self.data = data



    def handle_client(self, connection, address):
        try:
            while True:
                data = connection.recv(1024)  # Odbieranie danych z klienta
                if not data:
                    break
                message = data.decode('utf-8')  # Dekodowanie danych z bajtów na string
                if message.startswith("SetMyNickname(") and self.data.return_player_state(address[1]) == -1 and len(self.data.players) <= 4:
                    self.set_nickname(connection, address, message)
                elif message.startswith("PickChampion(") and self.data.return_player_state(address[1]) == 0:
                    self.pick_champion(connection, address, message)
                elif message.startswith("SetReady()") and self.data.return_player_state(address[1]) == 1:
                    self.set_ready(connection, address, message)
                elif message.startswith("SetNotReady()") and self.data.return_player_state(address[1]) == 1:
                    self.set_not_ready(connection, address, message)
                elif message.startswith("isStarted()") and self.data.return_player_state(address[1]) == 1 and self.data.check_players_ready():
                    response = "Started()"
                    connection.send(response.encode('utf-8'))
                    self.data.change_player_state(address[1], 2)
                elif message.startswith("isStarted()") and self.data.return_player_state(address[1]) == 1 and not self.data.check_players_ready():
                    response = "NotStarted()"
                    connection.send(response.encode('utf-8'))
                else:
                    response = "Command Not Found!"
                    connection.send(response.encode('utf-8'))
                print(self.data.players)
                print(self.data.champions)
        finally:
            self.data.remove_player_by_port(address[1])
            connection.close()

    def set_nickname(self, connection, address, message):
        try:
            start_index = message.find("(") + 1
            end_index = message.find(")")
            extracted_nickname = message[start_index:end_index]
            found = any(extracted_nickname == player_data['nick'] for player_data in self.data.players.values())
            if found:
                response = "BadNickname(exists);"
                connection.send(response.encode('utf-8'))
            elif len(extracted_nickname) < 3 or len(extracted_nickname) > 20:
                response = "BadNickname(TooLongOrShort);"
                connection.send(response.encode('utf-8'))
            else:
                self.data.add_player(len(self.data.players), extracted_nickname, address[0], address[1], 0)
                response = "StartCharacterLobby();"
                connection.send(response.encode('utf-8'))
                print(self.data.players)
            self.handle_client(connection, address)  # return

        finally:
            self.data.remove_player_by_port(address[1])
            connection.close()

    def pick_champion(self, connection, address, message):
        try:
            start_index = message.find("(") + 1
            end_index = message.find(")")
            extracted_champion = message[start_index:end_index]
            # found = any(extracted_champion == champion_data['characterID'] for champion_data in champions.values())
            if self.data.check_characterID_in_champions(extracted_champion):
                response = "BadChampion(exists);"
                connection.send(response.encode('utf-8'))
            elif extracted_champion not in {"pac", "gh1", "gh2", "gh3", "gh4"}:
                response = "BadChampion(invalidChampion);"
                connection.send(response.encode('utf-8'))
            else:
                response = "StartReadyLobby();"
                self.data.add_champion(len(self.data.champions), self.data.return_nick_by_port(address[1]), address[1], extracted_champion, False)
                connection.send(response.encode('utf-8'))
                self.data.change_player_state(address[1], 1)
                print(self.data.players)
            print(self.data.champions)
            self.handle_client(connection, address)  # return
        finally:
            self.data.remove_player_by_port(address[1])
            self.data.remove_champion_by_port(address[1])
            connection.close()

    def set_ready(self, connection, address, message):
        try:
            response = "Ready();"
            connection.send(response.encode('utf-8'))
            self.data.change_champion_ready(address[1],True)
            print(self.data.players)
            print(self.data.champions)
            self.handle_client(connection, address)  # return
        finally:
            self.data.remove_player_by_port(address[1])
            self.data.remove_champion_by_port(address[1])
            connection.close()

    def set_not_ready(self, connection, address, message):
        try:
            response = "NotReady();"
            connection.send(response.encode('utf-8'))
            self.data.change_champion_ready(address[1],False)
            print(self.data.players)
            self.handle_client(connection, address)  # return
        finally:
            self.data.remove_player_by_port(address[1])
            self.data.remove_champion_by_port(address[1])
            connection.close()



