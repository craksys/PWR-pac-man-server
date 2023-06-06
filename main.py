import socket
import threading

HOST = 'localhost'  # Adres IP lub nazwa hosta serwera
PORT = 50001  # Numer portu

players = {}
champions = {}
def add_player(player_id, nick, ip, port):
    players[player_id] = {
        'nick': nick,
        'ip': ip,
        'port': port
    }

def add_champion(champion_id, nick, port, characterID):
    champions[champion_id] = {
        'nick': nick,
        'port': port,
        'characterID' : characterID
    }

def remove_player_by_port(port):
    players_to_remove = []
    for player_id, player_data in players.items():
        if player_data['port'] == port:
            players_to_remove.append(player_id)
    for player_id in players_to_remove:
        del players[player_id]

def handle_client(connection, address):
    try:
        while True:
            data = connection.recv(1024)  # Odbieranie danych z klienta
            if not data:
                break
            message = data.decode('utf-8')  # Dekodowanie danych z bajtów na string
            if message.startswith("SetMyNickname("):
                set_nickname(connection, address, message)
            else:
                response = "Command Not Found!"
                connection.send(response.encode('utf-8'))
    finally:
        remove_player_by_port(address[1])
        connection.close()

def set_nickname(connection, address, message):
    try:
        start_index = message.find("(") + 1
        end_index = message.find(")")
        extracted_nickname = message[start_index:end_index]
        found = any(extracted_nickname == player_data['nick'] for player_data in players.values())
        if found:
            response = "BadNickname(exists);"
            connection.send(response.encode('utf-8'))
        elif len(extracted_nickname) < 3 or len(extracted_nickname) > 20:
            response = "BadNickname(TooLongOrShort);"
            connection.send(response.encode('utf-8'))
        else:
            add_player(len(players), extracted_nickname, address[0], address[1])
            response = "StartCharacterLobby();"
            connection.send(response.encode('utf-8'))
            print(players)
        handle_client(connection, address) #return

    finally:
        remove_player_by_port(address[1])
        connection.close()

def pick_champion(connection, address):
    try:
        while True:
            data = connection.recv(1024)  # Odbieranie danych z klienta
            if not data:
                break

            message = data.decode('utf-8')  # Dekodowanie danych z bajtów na string
            if message.startswith("PickChampion("):




def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Nasłuchiwanie na maksymalnie 5 połączeń

        print('Serwer nasłuchuje na porcie', PORT)

        while True:
            connection, address = server_socket.accept()
            print('Połączono z', address)

            # Tworzenie nowego wątku dla obsługi klienta
            client_thread = threading.Thread(target=handle_client, args=(connection, address))
            client_thread.start()

if __name__ == '__main__':
    start_server()
