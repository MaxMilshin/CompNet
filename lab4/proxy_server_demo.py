import json
import socket

def load_blacklist():
    with open('blacklist.json', 'r') as f:
        return json.load(f)['blacklist']

def is_blacklisted(url, blacklist):
    for domain in blacklist:
        if domain in url:
            return True
    return False

def proxy_server():
    host = 'localhost'
    port = 8888
    blacklist = load_blacklist()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen()

    print(f"Proxy-server is up on port {port}...")

    while True:
        client_socket, client_address = server_socket.accept()

        try:
            request = client_socket.recv(4096)
        except Exception as e:
            print(f"Error reading request: {e}")
            client_socket.close()
            continue

        method, url, _ = request.split(b'\n')[0].split(b' ')
        url = url.decode()
        if is_blacklisted(url, blacklist):
            response = b"HTTP/1.1 403 Forbidden\r\n\r\nPage is blacklisted by proxy server"
            client_socket.sendall(response)
            client_socket.close()
            continue

        domain = url[1:].split('/')[0]
        url_without_domain = '/' + url[len(domain) + 2:]
        headers = request.decode().split('\r\n')[1:-2]

        data = b''
        if method == b'POST':
            data = request.split(b'\r\n\r\n')[1]

        headers_dict = {}
        for header in headers:
            key, value = header.split(':', 1)
            headers_dict[key] = value.strip()

        new_request_lines = [
            f"{method.decode()} {url_without_domain} HTTP/1.1",
            f"Host: {domain}"
        ]
        for key, value in headers_dict.items():
            new_request_lines.append(f"{key}: {value}")

        new_request_lines.append("")
        new_request_lines.append(data.decode())

        new_request = '\r\n'.join(new_request_lines).encode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as web_socket:
            try:
                web_socket.connect((domain, 80))
                web_socket.sendall(new_request)
                response = web_socket.recv(4096)
            except Exception as e:
                print(f"Error redirecting request on web-server: {e}")
                client_socket.close()
                continue

        log_file = open('proxy_log.txt', 'a')
        try:
            status_code = response.decode().split('\n')[0].split(' ')[1]
            log_file.write(f"{url} {status_code}\n")
        except UnicodeDecodeError:
            log_file.write(f"{url} Unable to decode response\n")
        log_file.close()

        try:
            client_socket.sendall(response)
        except Exception as e:
            print(f"Error sending answer to client: {e}")

        client_socket.close()

if __name__ == '__main__':
    proxy_server()
