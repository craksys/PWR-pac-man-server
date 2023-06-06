import socket


def send_message():
    # Utwórz gniazdo (socket)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Podaj adres i port serwera
    server_address = ('localhost', 50001)

    try:
        # Połącz się z serwerem
        s.connect(server_address)

        while True:
            # Wprowadź wiadomość do wysłania
            data = s.recv(1024)
            if data:
                print(data.decode('utf-8'))
            message = input("Wpisz wiadomość (q aby zakończyć): ")

            if message == 'q':
                break

            # Wyślij wiadomość do serwera
            s.sendall(message.encode())

    finally:
        # Zamknij gniazdo po zakończeniu
        s.close()


if __name__ == '__main__':
    send_message()
