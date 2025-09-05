import socket

def execute_remote_command(host, port, command):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the remote server
        s.connect((host, port))

        # Send the command to the server
        s.sendall(command.encode())

        # Receive and print the output
        print("Command Output:")
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode())

    finally:
        # Close the socket
        s.close()


