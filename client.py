import socket

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_message(sock):
    data = sock.recv(1024)
    return data.decode()

def main():
    # Utwórz gniazdo (socket) TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Połącz się z lokalnym hostem i portem
    server_address = ('localhost', 50001)
    print('Łączenie z', server_address)
    sock.connect(server_address)

    try:
        while True:
            # Wysyłanie wiadomości
            message = input("Wpisz wiadomość do wysłania: ")
            send_message(sock, message)

            # Odbieranie odpowiedzi
            response = receive_message(sock)
            print('Odpowiedź:', response)

            # Zakończ, jeśli otrzymano polecenie zakończenia
            if response == 'exit':
                break

    finally:
        # Zamknij gniazdo
        print('Zamykanie gniazda')
        sock.close()

if __name__ == '__main__':
    main()
