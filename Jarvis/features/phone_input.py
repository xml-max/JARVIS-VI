import socket

def start(backlog=1):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(backlog)
    print(f"Server Socket is listening on {server_socket.getsockname()}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        try:
            client_socket.sendall(b'Send message')

            data = client_socket.recv(1024).decode()
            #print(data)
            client_socket.sendall(b'ended')
            client_socket.close()
            return data
            #client_socket.sendall("ho")
            # Check for specific phrases in received data
            if any(phrase in data for phrase in ["end connection", "end the connection"]):
                client_socket.sendall(b'ended')
                client_socket.close()
                break  # Exit the loop if end connection phrase is received

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            client_socket.close()
            

    server_socket.close()

