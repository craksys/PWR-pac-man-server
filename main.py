import socket
import threading
from player_data import Data
from player_lobby import Lobby
HOST = 'localhost'  # Adres IP lub nazwa hosta serwera
PORT = 50001  # Numer portu

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Nasłuchiwanie na maksymalnie 5 połączeń

        print('Serwer nasłuchuje na porcie', PORT)

        while True:
            connection, address = server_socket.accept()
            print('Połączono z', address)

            # Tworzenie nowego wątku dla obsługi klienta
            client_thread = threading.Thread(target=lobby.handle_client, args=(connection, address))
            client_thread.start()

if __name__ == '__main__':
    data = Data()
    lobby = Lobby(data)
    start_server()
