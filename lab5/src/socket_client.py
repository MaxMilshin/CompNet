import socket
import ssl
import base64
import sys

def send_email(sender_email, receiver_email, message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((smtp_server, smtp_port))
        response = client_socket.recv(1024)
        print(response.decode())

        client_socket.sendall(b"EHLO example.com\r\n")
        response = client_socket.recv(1024)
        print(response.decode())

        client_socket.sendall(b"STARTTLS\r\n")
        response = client_socket.recv(1024)
        print(response.decode())

        with ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLS) as ssl_socket:
            ssl_socket.write(b"EHLO example.com\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(b"AUTH LOGIN\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write((base64.b64encode(bytes(sender_email, "utf-8")) + b"\r\n"))
            response = ssl_socket.read(1024)
            print(response.decode())

            # вместо password нужно указать пароль доступа для незащищенных приложений для вашего аккаунта
            ssl_socket.write((base64.b64encode(bytes("password", "utf-8")) + b"\r\n"))
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(b"MAIL FROM:<" + bytes(sender_email, "utf-8") + b">\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(b"RCPT TO:<" + bytes(receiver_email, "utf-8") + b">\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(b"DATA\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(bytes(message, "utf-8"))
            ssl_socket.write(b"\r\n.\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

            ssl_socket.write(b"QUIT\r\n")
            response = ssl_socket.read(1024)
            print(response.decode())

if __name__ == '__main__':
    from_user = 'адрес отправителя'
    to_user = sys.argv[1]
    message_file_name = sys.argv[2]
    with open(message_file_name, 'r') as f:
        message = f.read()

    send_email(from_user, to_user, message)