import socket
import sys
# import time
import threading
import os


def serve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 8080)
    print('Starting up on %s port %s' % server_address)
    sock.bind(server_address)

    sock.listen(concurrency_level)

    while True:
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        print('Connection from', client_address)

        semaphore.acquire()

        t = threading.Thread(target=handle_connection, args=(connection,))
        t.start()


def handle_connection(connection):
    try:
        request = connection.recv(1024)

        requested_file = request.decode().split()[1][1:]

        if os.path.isfile(requested_file):
            # time.sleep(5)

            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
            with open(requested_file, 'r') as file:
                response += file.read()
        else:
            response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
            response += '<html><body><h1>404 Not Found</h1></body></html>'

        connection.sendall(response.encode())
    finally:
        connection.close()
        semaphore.release()

if __name__ == '__main__':
    concurrency_level = int(sys.argv[1])
    semaphore = threading.Semaphore(concurrency_level)
    serve()
